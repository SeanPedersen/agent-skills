---
name: free-domain-search
description: Check domain name availability using HTTP probing and WHOIS lookup. Use when brainstorming project names or checking if domains are free.
---

# Free Domain Search

Check domain name availability via HTTP probing and WHOIS lookup. No API key required.

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/). Also requires the `whois` command line tool.

On macOS:
```bash
brew install whois
```

On Debian/Ubuntu:
```bash
sudo apt install whois
```

## Usage

```bash
# Check a name across default TLDs (com, net, org, io, dev, app)
uv run {baseDir}/check.py myproject

# Check specific TLDs
uv run {baseDir}/check.py myproject --tlds com io dev

# Check a specific full domain
uv run {baseDir}/check.py myproject.com
```

## Output Format

```
[+] myproject.dev - AVAILABLE
[-] myproject.com - TAKEN
    Registrar: GoDaddy.com, LLC
    Expires: 2025-08-15
[?] myproject.io - UNKNOWN
    Error: WHOIS lookup timed out
```

Markers:
- `[+]` = Available
- `[-]` = Taken
- `[?]` = Unknown (check failed)

## When to Use

- Brainstorming names for new projects or products
- Checking if a domain is available before purchasing
- Bulk-checking a name across multiple TLDs
