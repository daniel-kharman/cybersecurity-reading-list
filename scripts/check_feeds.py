#!/usr/bin/env python3
"""Check every feed in feeds.opml and report the ones that need attention.

Each feed ends up in one of five states:

  ok       loads, parses as RSS or Atom, and has a post inside the quiet window
  broken   HTTP error, timeout, or the response is not a feed
  moved    loads, but through a permanent redirect, so the URL should be updated
  quiet    loads, but has no post inside the quiet window
  blocked  fails from here, but is listed in known-blocked.txt because the site
           refuses automated fetchers while working in a real feed reader

The script only reports. It never edits feeds.opml.

It also keeps the feed tables in README.md in step with feeds.opml:
  --update-readme   rewrite the tables between the feed markers
  --check-readme    exit 1 if the tables are out of date

Exit codes: 0 the run completed, 1 feeds.opml or README.md is invalid,
2 feeds need attention (only with --fail-on-problems).
"""

from __future__ import annotations

import argparse
import calendar
import gzip
import os
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = (
    "Mozilla/5.0 (compatible; cybersecurity-reading-list-feed-check/1.0; "
    "+https://github.com/daniel-kharman/cybersecurity-reading-list)"
)
ACCEPT = "application/atom+xml, application/rss+xml, application/xml;q=0.9, text/xml;q=0.8, */*;q=0.5"
TIMEOUT_SECONDS = 30
MAX_BYTES = 10 * 1024 * 1024
ATTEMPTS = 3
RETRY_STATUSES = {408, 425, 429, 500, 502, 503, 504}
PERMANENT_REDIRECTS = {301, 308}
README_START = "<!-- feeds:start -->"
README_END = "<!-- feeds:end -->"
NEEDS_ATTENTION = ("broken", "moved", "quiet")


@dataclass
class Feed:
    folder: str
    name: str
    url: str
    site: str
    description: str


@dataclass
class Result:
    feed: Feed
    state: str
    detail: str
    newest: datetime | None = None


@dataclass
class Fetched:
    body: bytes
    final_url: str
    hops: list[tuple[int, str]] = field(default_factory=list)


class RedirectRecorder(urllib.request.HTTPRedirectHandler):
    """Follow redirects as usual, but remember each hop's status code."""

    def __init__(self) -> None:
        self.hops: list[tuple[int, str]] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme not in ("http", "https"):
            raise urllib.error.HTTPError(newurl, code, "redirect to a non-HTTP URL", headers, fp)
        self.hops.append((code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


# --------------------------------------------------------------------------- OPML


def load_opml(path: Path) -> tuple[list[Feed], list[str]]:
    """Return the feeds in the file and a list of problems with the file itself."""
    errors: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [], [f"{path.name} could not be read as XML: {exc}"]

    body = root.find("body")
    if root.tag != "opml" or body is None:
        return [], [f"{path.name} is not an OPML file (no <opml><body>)"]

    feeds: list[Feed] = []
    seen_urls: dict[str, str] = {}
    for folder in body:
        folder_name = (folder.get("text") or "").strip()
        if folder.get("xmlUrl"):
            errors.append(f"'{folder_name}' sits outside a folder; put every feed inside one")
            continue
        if not folder_name:
            errors.append("a folder has no text attribute")
        for item in folder:
            name = (item.get("text") or "").strip()
            url = (item.get("xmlUrl") or "").strip()
            label = name or url or "(unnamed outline)"
            if len(item):
                errors.append(f"'{label}' has nested outlines; folders can only be one level deep")
            if not name:
                errors.append(f"'{label}' has no text attribute")
            if not url:
                errors.append(f"'{label}' has no xmlUrl attribute")
                continue
            parts = urlsplit(url)
            if parts.scheme != "https" or not parts.netloc:
                errors.append(f"'{label}' must use an https:// URL, got {url}")
            if url in seen_urls:
                errors.append(f"'{label}' repeats the URL already used by '{seen_urls[url]}'")
            seen_urls[url] = label
            if not (item.get("description") or "").strip():
                errors.append(f"'{label}' has no description attribute")
            feeds.append(
                Feed(
                    folder=folder_name,
                    name=name,
                    url=url,
                    site=(item.get("htmlUrl") or "").strip(),
                    description=(item.get("description") or "").strip(),
                )
            )
    if not feeds and not errors:
        errors.append(f"{path.name} contains no feeds")
    return feeds, errors


def load_known_blocked(path: Path) -> set[str]:
    if not path.exists():
        return set()
    urls = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            urls.add(line)
    return urls


# ------------------------------------------------------------------------- README


def cell(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def render_feed_tables(feeds: list[Feed]) -> str:
    lines: list[str] = []
    current = None
    for feed in feeds:
        if feed.folder != current:
            if current is not None:
                lines.append("")
            current = feed.folder
            lines += [f"### {feed.folder}", "", "| Feed | Why it's here |", "|---|---|"]
        title = f"[{cell(feed.name)}]({feed.site})" if feed.site else cell(feed.name)
        lines.append(f"| {title} ([feed]({feed.url})) | {cell(feed.description)} |")
    return "\n".join(lines)


def readme_with_tables(readme: str, tables: str) -> str | None:
    """Return the README with the feed tables replaced, or None if the markers are missing."""
    start = readme.find(README_START)
    end = readme.find(README_END)
    if start == -1 or end == -1 or end < start:
        return None
    return readme[: start + len(README_START)] + "\n" + tables + "\n" + readme[end:]


# ----------------------------------------------------------------------- fetching


def fetch(url: str) -> Fetched:
    """Fetch a URL, retrying transient failures. Raises on the final failure."""
    last_error: Exception | None = None
    for attempt in range(ATTEMPTS):
        if attempt:
            time.sleep(3 * attempt)
        recorder = RedirectRecorder()
        opener = urllib.request.build_opener(recorder)
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": ACCEPT})
        try:
            with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
                body = response.read(MAX_BYTES + 1)
                if len(body) > MAX_BYTES:
                    raise ValueError(f"response is larger than {MAX_BYTES // (1024 * 1024)} MB")
                if response.headers.get("Content-Encoding", "").lower() == "gzip":
                    body = gzip.decompress(body)
                return Fetched(body=body, final_url=response.geturl(), hops=recorder.hops)
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in RETRY_STATUSES:
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            last_error = exc
        except ValueError as exc:
            last_error = exc
            break
    assert last_error is not None
    raise last_error


def describe_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        if 300 <= exc.code < 400:
            return f"HTTP {exc.code}: {exc.reason}"
        return f"HTTP {exc.code}"
    if isinstance(exc, urllib.error.URLError):
        return f"connection failed: {exc.reason}"
    if isinstance(exc, TimeoutError):
        return f"timed out after {TIMEOUT_SECONDS} seconds"
    return str(exc) or exc.__class__.__name__


def newest_entry_date(parsed) -> datetime | None:
    newest = None
    for entry in parsed.entries:
        for key in ("published_parsed", "updated_parsed", "created_parsed"):
            stamp = entry.get(key)
            if stamp:
                when = datetime.fromtimestamp(calendar.timegm(stamp), tz=timezone.utc)
                if newest is None or when > newest:
                    newest = when
    return newest


def check_feed(feed: Feed, quiet_days: int, known_blocked: set[str], now: datetime) -> Result:
    import feedparser

    try:
        fetched = fetch(feed.url)
    except Exception as exc:  # noqa: BLE001 - every failure becomes a reported state
        detail = describe_error(exc)
        if feed.url in known_blocked:
            return Result(feed, "blocked", f"{detail}; listed in known-blocked.txt")
        return Result(feed, "broken", detail)

    parsed = feedparser.parse(fetched.body)
    if not parsed.get("version") and not parsed.entries:
        if feed.url in known_blocked:
            return Result(feed, "blocked", "response is not a feed; listed in known-blocked.txt")
        return Result(feed, "broken", "response is not an RSS or Atom feed")

    newest = newest_entry_date(parsed)
    if newest:
        age_days = max((now - newest).days, 0)
        last_post = f"last post {newest:%Y-%m-%d}"
    else:
        age_days = None
        last_post = "no dated posts" if parsed.entries else "no posts"

    moved = fetched.final_url != feed.url and any(code in PERMANENT_REDIRECTS for code, _ in fetched.hops)
    if moved:
        return Result(feed, "moved", f"now at {fetched.final_url} ({last_post})", newest)
    if not parsed.entries:
        return Result(feed, "quiet", "feed is valid but has no posts", newest)
    if age_days is not None and age_days > quiet_days:
        return Result(feed, "quiet", f"{last_post}, {age_days} days ago", newest)
    return Result(feed, "ok", last_post, newest)


# ------------------------------------------------------------------------- report


def render_report(results: list[Result], quiet_days: int, now: datetime) -> str:
    problems = [r for r in results if r.state in NEEDS_ATTENTION]
    blocked = [r for r in results if r.state == "blocked"]
    total = len(results)

    def table(rows: list[Result]) -> list[str]:
        lines = ["| State | Feed | Folder | Detail |", "|---|---|---|---|"]
        for r in rows:
            lines.append(
                f"| {r.state} | [{cell(r.feed.name)}]({r.feed.url}) | {cell(r.feed.folder)} | {cell(r.detail)} |"
            )
        return lines

    if problems:
        noun = "feed needs" if len(problems) == 1 else "feeds need"
        lines = [f"## {len(problems)} of {total} {noun} attention", ""]
        order = {state: index for index, state in enumerate(NEEDS_ATTENTION)}
        lines += table(sorted(problems, key=lambda r: (order[r.state], r.feed.folder, r.feed.name)))
        lines += [
            "",
            "- **broken**: the URL returned an error or something that is not a feed. "
            "Find the new feed URL, or remove the feed.",
            "- **moved**: the feed redirects permanently. Update `xmlUrl` in `feeds.opml` to the new address.",
            f"- **quiet**: no post in the last {quiet_days} days. Decide whether the source is finished or resting.",
        ]
    else:
        lines = [f"## All {total} feeds passed"]

    if blocked:
        lines += ["", f"{len(blocked)} feed(s) failed from this runner but are listed in `scripts/known-blocked.txt`:", ""]
        lines += table(blocked)

    lines += ["", "<details><summary>Every feed</summary>", ""]
    lines += table(results)
    lines += ["", "</details>", "", f"Checked {now:%Y-%m-%d %H:%M} UTC."]
    return "\n".join(lines) + "\n"


def write_github_output(name: str, value: object) -> None:
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(f"{name}={value}\n")


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--opml", type=Path, default=REPO_ROOT / "feeds.opml")
    parser.add_argument("--known-blocked", type=Path, default=REPO_ROOT / "scripts" / "known-blocked.txt")
    parser.add_argument("--readme", type=Path, default=REPO_ROOT / "README.md")
    parser.add_argument("--quiet-days", type=int, default=365, help="days without a post before a feed is quiet")
    parser.add_argument("--report", type=Path, help="write the Markdown report to this file")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--update-readme", action="store_true", help="rewrite the feed tables in the README")
    parser.add_argument("--check-readme", action="store_true", help="fail if the README feed tables are out of date")
    parser.add_argument("--validate-only", action="store_true", help="check the files without fetching any feed")
    parser.add_argument("--fail-on-problems", action="store_true", help="exit 2 if any feed needs attention")
    args = parser.parse_args()

    feeds, errors = load_opml(args.opml)
    known_blocked = load_known_blocked(args.known_blocked)
    for url in sorted(known_blocked - {feed.url for feed in feeds}):
        errors.append(f"known-blocked.txt lists {url}, which is not in {args.opml.name}")

    if not errors and (args.update_readme or args.check_readme):
        readme = args.readme.read_text(encoding="utf-8")
        updated = readme_with_tables(readme, render_feed_tables(feeds))
        if updated is None:
            errors.append(f"{args.readme.name} is missing the {README_START} and {README_END} markers")
        elif args.update_readme:
            if updated != readme:
                args.readme.write_text(updated, encoding="utf-8")
                print(f"Updated the feed tables in {args.readme.name}")
        elif updated != readme:
            errors.append(
                f"the feed tables in {args.readme.name} are out of date; "
                "run: python scripts/check_feeds.py --update-readme --validate-only"
            )

    if errors:
        print("Problems with the files:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        summary = os.environ.get("GITHUB_STEP_SUMMARY")
        if summary:
            with open(summary, "a", encoding="utf-8") as handle:
                handle.write("## The files need fixing\n\n" + "\n".join(f"- {e}" for e in errors) + "\n")
        return 1

    print(f"{args.opml.name}: {len(feeds)} feeds in {len({f.folder for f in feeds})} folders")
    if args.validate_only:
        return 0

    now = datetime.now(timezone.utc)
    with ThreadPoolExecutor(max_workers=max(args.workers, 1)) as pool:
        results = list(pool.map(lambda feed: check_feed(feed, args.quiet_days, known_blocked, now), feeds))

    for result in results:
        print(f"{result.state:8} {result.feed.name}: {result.detail}")

    report = render_report(results, args.quiet_days, now)
    if args.report:
        args.report.write_text(report, encoding="utf-8")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(report)

    problems = sum(1 for r in results if r.state in NEEDS_ATTENTION)
    write_github_output("problems", problems)
    write_github_output("total", len(results))
    print(f"\n{problems} of {len(results)} feeds need attention")
    return 2 if problems and args.fail_on_problems else 0


if __name__ == "__main__":
    sys.exit(main())
