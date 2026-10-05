# Cybersecurity Reading List

[![Check feeds](https://github.com/daniel-kharman/cybersecurity-reading-list/actions/workflows/check-feeds.yml/badge.svg)](https://github.com/daniel-kharman/cybersecurity-reading-list/actions/workflows/check-feeds.yml)

A small RSS feed list for staying current in security. A weekly job tests that every feed still works.

Most security news reports incidents after they happen. This list leans toward the sources upstream of that: the researchers who publish new techniques and the practitioners who turn them into detections.

## Use it

1. Download [`feeds.opml`](https://raw.githubusercontent.com/daniel-kharman/cybersecurity-reading-list/main/feeds.opml).
2. Import it into any feed reader, such as Inoreader, Feedly, NetNewsWire or Miniflux. Look for "Import OPML" in the reader's settings.
3. Start with the **00 Weekly Digests** folder. Reading only that folder each week still keeps you well informed.

## How it's organised

The folders fall into three tiers, so that familiar topics don't take over the whole list.

| Tier | Share of reading | What it's for |
|---|---|---|
| **Core** | about 40% | Keeping current in the areas you already work in. Here that means cloud and Kubernetes, identity, and detection and DFIR. |
| **Growth** | about 40% | Areas where demand is heading: AI security, software supply chain, offensive and vulnerability research, and threat intelligence. |
| **Horizon** | about 20% | Early topics worth watching: post-quantum cryptography, OT and ICS, and policy and regulation. |

The core tier reflects one person's work. Fork the list and swap those folders for your own.

## How to read it

- **Triage for about 20 minutes a day.** Skim headlines and save what deserves a proper read.
- **Go deeper by folder.** The digests tell you what happened. The other folders are for the topics that catch your eye.
- **Prune monthly.** Remove any feed you keep skipping.
- **Reproduce what you read.** Pick one technique a fortnight, run it in a lab and write the detection.

## The feeds

These tables are generated from `feeds.opml`.

<!-- feeds:start -->
### 00 Weekly Digests

| Feed | Why it's here |
|---|---|
| [tl;dr sec](https://tldrsec.com) ([feed](https://rss.beehiiv.com/feeds/xgTKUmMmUm.xml)) | Weekly digest of new security research, tools and talks. Strongest on cloud, AppSec and AI. |
| [Risky Business (podcast)](https://risky.biz) ([feed](https://risky.biz/feeds/risky-business/)) | Weekly news podcast that explains which stories matter and why. |
| [Risky Bulletin](https://news.risky.biz) ([feed](https://news.risky.biz/rss/)) | Short news briefings several times a week, covering incidents, policy and threat actors. |
| [CloudSecList](https://cloudseclist.com) ([feed](https://cloudseclist.com/feed.xml)) | Weekly roundup of cloud security research across AWS, GCP, Azure and Kubernetes. |
| [Detection Engineering Weekly](https://www.detectionengineering.net) ([feed](https://www.detectionengineering.net/feed)) | Weekly picks of detection research, rules and tooling. |
| [This Week in 4n6](https://thisweekin4n6.com) ([feed](https://thisweekin4n6.com/feed/)) | Weekly index of DFIR posts, tools and malware analysis. |
| [Unsupervised Learning (Daniel Miessler)](https://danielmiessler.com) ([feed](https://danielmiessler.com/feed.rss)) | Commentary on security and AI from Daniel Miessler. |

### Core - Cloud & Kubernetes

| Feed | Why it's here |
|---|---|
| [Wiz Blog](https://www.wiz.io/blog) ([feed](https://www.wiz.io/feed/rss.xml)) | Cloud vulnerability research and incident write-ups, mixed with product posts. |
| [Datadog Security Labs](https://securitylabs.datadoghq.com) ([feed](https://securitylabs.datadoghq.com/rss/feed.xml)) | Cloud attack techniques and threat research, often with open-source tooling. |
| [Google Cloud - Identity & Security](https://cloud.google.com/blog/products/identity-security) ([feed](https://cloudblog.withgoogle.com/products/identity-security/rss/)) | Google Cloud's security product and feature announcements. |
| [Kubernetes Blog](https://kubernetes.io/blog/) ([feed](https://kubernetes.io/feed.xml)) | Release notes and feature write-ups, including security changes. |

### Core - Identity

| Feed | Why it's here |
|---|---|
| [SpecterOps](https://specterops.io/blog/) ([feed](https://specterops.io/feed/)) | Active Directory and Entra ID attack-path research from the BloodHound team. |
| [Dirk-jan Mollema](https://dirkjanm.io) ([feed](https://dirkjanm.io/feed.xml)) | Deep Entra ID and hybrid identity research. Posts are rare and worth reading. |
| [Active Directory Security (Sean Metcalf)](https://adsecurity.org) ([feed](https://adsecurity.org/?feed=rss2)) | Active Directory attack and defence reference posts. Posts are rare. |
| [Push Security](https://pushsecurity.com/blog) ([feed](https://pushsecurity.com/rss.xml)) | SaaS identity attacks: phishing kits that defeat MFA, OAuth abuse, session theft. Vendor blog. |

### Core - Detection & DFIR

| Feed | Why it's here |
|---|---|
| [The DFIR Report](https://thedfirreport.com) ([feed](https://thedfirreport.com/feed/)) | Full intrusion case studies, from initial access to impact, with timelines and indicators. |
| [SANS Internet Storm Center](https://isc.sans.edu) ([feed](https://isc.sans.edu/rssfeed_full.xml)) | Daily handler diaries on what is being seen in the wild. |
| [Red Canary](https://redcanary.com/blog/) ([feed](https://redcanary.com/blog/feed/)) | Detection-focused threat research and technique analysis. |
| [Elastic Security Labs](https://www.elastic.co/security-labs) ([feed](https://www.elastic.co/security-labs/rss/feed.xml)) | Malware analysis and detection research, with published rules. |

### Growth - AI Security

| Feed | Why it's here |
|---|---|
| [Simon Willison - Prompt Injection](https://simonwillison.net/tags/prompt-injection/) ([feed](https://simonwillison.net/tags/prompt-injection.atom)) | Running commentary on prompt injection and the security of LLM agents. |
| [Embrace The Red (Johann Rehberger)](https://embracethered.com/blog/) ([feed](https://embracethered.com/blog/index.xml)) | Practical exploits against AI assistants and agents, with disclosure write-ups. |
| [Trail of Bits](https://blog.trailofbits.com) ([feed](https://blog.trailofbits.com/index.xml)) | Security engineering research across AI and ML, cryptography and software assurance. |
| [NVIDIA Technical Blog - Cybersecurity](https://developer.nvidia.com/blog/category/cybersecurity/) ([feed](https://developer.nvidia.com/blog/category/cybersecurity/feed/)) | Includes the NVIDIA AI red team's posts on securing ML systems. |

### Growth - Software Supply Chain

| Feed | Why it's here |
|---|---|
| [Socket](https://socket.dev/blog) ([feed](https://socket.dev/api/blog/feed.atom)) | Malicious package discoveries across npm, PyPI and other registries. |
| [OpenSSF](https://openssf.org/blog/) ([feed](https://openssf.org/feed/)) | Open-source security standards and tooling, such as Sigstore, SLSA and Scorecard. |
| [StepSecurity](https://www.stepsecurity.io/blog) ([feed](https://www.stepsecurity.io/blog/rss.xml)) | Analysis of CI/CD and GitHub Actions compromises. |

### Growth - Offensive & Vuln Research

| Feed | Why it's here |
|---|---|
| [Google Project Zero](https://projectzero.google) ([feed](https://projectzero.google/feed.xml)) | In-depth vulnerability and exploit research. |
| [watchTowr Labs](https://labs.watchtowr.com) ([feed](https://labs.watchtowr.com/rss/)) | Fast teardowns of vulnerabilities in edge devices and enterprise appliances. |
| [PortSwigger Research](https://portswigger.net/research) ([feed](https://portswigger.net/research/rss)) | New web attack classes and techniques. |

### Growth - Threat Intel

| Feed | Why it's here |
|---|---|
| [Google Threat Intelligence](https://cloud.google.com/blog/topics/threat-intelligence) ([feed](https://cloudblog.withgoogle.com/topics/threat-intelligence/rss/)) | Threat actor tracking and incident research from Mandiant and Google. |
| [Microsoft Threat Intelligence](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/) ([feed](https://www.microsoft.com/en-us/security/blog/topic/threat-intelligence/feed/)) | Threat actor reporting and technique analysis from Microsoft. |
| [Unit 42](https://unit42.paloaltonetworks.com) ([feed](https://unit42.paloaltonetworks.com/feed/)) | Threat research and malware analysis from Palo Alto Networks. |
| [Cisco Talos](https://blog.talosintelligence.com) ([feed](https://blog.talosintelligence.com/rss/)) | Threat research, malware analysis and vulnerability disclosures. |
| [The Record](https://therecord.media) ([feed](https://therecord.media/feed)) | Security news reporting on nation-state activity, crime and policy. |
| [Krebs on Security](https://krebsonsecurity.com) ([feed](https://krebsonsecurity.com/feed/)) | Investigative reporting on cybercrime. |

### Horizon - Post-Quantum Crypto

| Feed | Why it's here |
|---|---|
| [Cloudflare - Post-Quantum](https://blog.cloudflare.com/tag/post-quantum/) ([feed](https://blog.cloudflare.com/tag/post-quantum/rss/)) | Writing on post-quantum cryptography from a team deploying it at scale. |
| [NIST Cybersecurity Insights](https://www.nist.gov/blogs/cybersecurity-insights) ([feed](https://www.nist.gov/blogs/cybersecurity-insights/rss.xml)) | NIST staff posts on standards and guidance, including cryptography. |

### Horizon - OT & ICS

| Feed | Why it's here |
|---|---|
| [Industrial Cyber](https://industrialcyber.co) ([feed](https://industrialcyber.co/feed/)) | News on OT, ICS and critical infrastructure security. |

### Horizon - Policy & Regulation

| Feed | Why it's here |
|---|---|
| [CyberScoop](https://cyberscoop.com) ([feed](https://cyberscoop.com/feed/)) | US reporting on cyber policy, government and enforcement. |
| [iTnews - Security](https://www.itnews.com.au/news/security) ([feed](https://www.itnews.com.au/RSS/rss.ashx?type=Category&ID=32)) | Australian security news, including government and regulatory developments. |
<!-- feeds:end -->

## Left out

Some sources belong here but can't be followed by RSS.

- **CISA advisories**: the feeds refuse automated fetchers. Subscribe to CISA's email alerts, or pull the Known Exploited Vulnerabilities catalogue as JSON.
- **Dragos**: the blog has no feed.
- **ASD's ACSC**: the [alerts](https://www.cyber.gov.au/rss/alerts) and [advisories](https://www.cyber.gov.au/rss/advisories) feeds time out for cloud-hosted fetchers, so they may fail in a hosted reader. Try them if your reader runs on your own machine.
- **Lawfare**: the site's feeds currently return no posts.

## How the list stays current

[`scripts/check_feeds.py`](scripts/check_feeds.py) fetches every feed and sorts it into one of these states:

| State | Meaning |
|---|---|
| ok | Loads, parses as RSS or Atom, and has a post in the last 12 months. |
| broken | Returns an error, times out, or returns something that isn't a feed. |
| moved | Loads through a permanent redirect, so the URL should be updated. |
| quiet | Loads but has had no post in the last 12 months. |
| blocked | Fails from the runner, but is listed in [`scripts/known-blocked.txt`](scripts/known-blocked.txt) because the site refuses automated fetchers. |

A [GitHub Action](.github/workflows/check-feeds.yml) runs the script every week. If any feed is broken, moved or quiet, it opens an issue listing them, and closes the issue once every feed passes. The script never edits the list.

To run it yourself:

```sh
pip install --require-hashes -r scripts/requirements.txt
python scripts/check_feeds.py
```

## Suggest a change

Open an issue or a pull request. A feed is a good fit if it:

- publishes original research or analysis, not rewritten news
- has a working RSS or Atom feed
- adds something the list doesn't already cover

The list is meant to stay small, so a new feed usually replaces an existing one.

To change the list, edit `feeds.opml`, giving each feed a `description`, then regenerate the tables above:

```sh
python scripts/check_feeds.py --update-readme --validate-only
```

## Licence

[MIT](LICENSE)
