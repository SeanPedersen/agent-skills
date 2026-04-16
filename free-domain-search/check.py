#!/usr/bin/env python3
"""Check domain availability via HTTP probing and WHOIS lookup."""
# /// script
# requires-python = ">=3.10"
# dependencies = ["niquests", "python-whois"]
# ///

import argparse
import logging
import sys

import niquests
import whois

# Suppress noisy connection errors from HTTP probes
logging.getLogger("niquests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


DEFAULT_TLDS = ["com", "net", "org", "io", "dev", "app"]


def _format_date(d) -> str:
    if d is None:
        return ""
    if isinstance(d, list):
        d = d[0]
    try:
        return d.strftime("%Y-%m-%d")
    except Exception:
        return str(d)


def check_whois(domain: str) -> dict:
    """Check WHOIS for domain registration. Returns dict with availability info."""
    try:
        w = whois.whois(domain)
        if w.domain_name is None:
            return {"available": True, "method": "whois"}
        return {
            "available": False,
            "method": "whois",
            "registrar": w.registrar or "",
            "expiration": _format_date(w.expiration_date),
        }
    except Exception as e:
        err_str = str(e).lower()
        if any(kw in err_str for kw in ("no match", "not found", "no entries", "status: free", "free\n")):
            return {"available": True, "method": "whois"}
        return {"available": None, "method": "whois", "error": str(e)}


def check_http(domain: str) -> bool:
    """Quick HTTP probe. Returns True if domain responds (likely taken)."""
    import warnings
    warnings.filterwarnings("ignore")
    for scheme in ["https", "http"]:
        try:
            resp = niquests.head(
                f"{scheme}://{domain}",
                timeout=5,
                allow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            if resp.status_code < 500:
                return True
        except Exception:
            continue
    return False


def check_domain(domain: str) -> dict:
    """Combined HTTP + WHOIS check for a single domain."""
    http_alive = check_http(domain)
    whois_result = check_whois(domain)

    if whois_result.get("available") is True and not http_alive:
        status = "AVAILABLE"
    elif whois_result.get("available") is True and http_alive:
        status = "LIKELY TAKEN (responds to HTTP but no WHOIS record)"
    elif whois_result.get("available") is False:
        status = "TAKEN"
    else:
        status = "UNKNOWN"

    return {
        "domain": domain,
        "status": status,
        "http_alive": http_alive,
        **whois_result,
    }


def main():
    parser = argparse.ArgumentParser(description="Check domain name availability")
    parser.add_argument("name", help="Domain name (without TLD) or full domain")
    parser.add_argument(
        "--tlds",
        nargs="+",
        default=None,
        help=f"TLDs to check (default: {' '.join(DEFAULT_TLDS)})",
    )
    args = parser.parse_args()

    name = args.name.lower().strip()
    tlds = args.tlds or DEFAULT_TLDS

    # If name already has a TLD, check just that one
    if "." in name:
        domains = [name]
    else:
        domains = [f"{name}.{tld}" for tld in tlds]

    for domain in domains:
        result = check_domain(domain)
        status = result["status"]
        marker = "+" if "AVAILABLE" in status else "-" if "TAKEN" in status else "?"
        print(f"[{marker}] {result['domain']} - {status}")
        if result.get("registrar"):
            print(f"    Registrar: {result['registrar']}")
        if result.get("expiration"):
            print(f"    Expires: {result['expiration']}")
        if result.get("error"):
            print(f"    Error: {result['error']}")


if __name__ == "__main__":
    main()
