#!/usr/bin/env python3
"""Check the LIVE hub and every resource it links to (stdlib only).

For https://tkunst.github.io/ and each card link on it:
  - responds 200 over HTTPS,
  - has a <title>,
  - resource pages link back to the hub,
  - (optional) the hub's served copy matches this commit's index.html, so a
    push that never deployed is caught. Pass --expect-current to require it;
    it retries for a few minutes while Pages finishes deploying.

Usage: python3 scripts/live_check.py [--expect-current]
"""
import hashlib
import re
import sys
import time
import urllib.request
from urllib.parse import urljoin
from html.parser import HTMLParser

HUB = "https://tkunst.github.io/"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and "card" in (a.get("class") or "").split() and a.get("href"):
            self.cards.append(a["href"])


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "tklearn-live-check", "Cache-Control": "no-cache"})
    with urllib.request.urlopen(req, timeout=30) as r:  # nosec B310 - fixed https URLs only
        return r.status, r.read().decode("utf-8", "replace")


def main():
    expect_current = "--expect-current" in sys.argv
    problems = []

    if expect_current:
        want = hashlib.sha256(open("index.html", "rb").read()).hexdigest()
        for _ in range(20):
            _, body = get(HUB + f"?v={int(time.time())}")
            if hashlib.sha256(body.encode("utf-8")).hexdigest() == want:
                break
            time.sleep(30)
        else:
            problems.append("live hub never matched this commit's index.html (Pages deploy failed or stuck?)")

    status, hub = get(HUB)
    if status != 200:
        problems.append(f"{HUB}: HTTP {status}")
    p = Links()
    p.feed(hub)
    if not p.cards:
        problems.append(f"{HUB}: no resource cards found")

    for href in p.cards:
        url = urljoin(HUB, href)
        if not url.startswith(HUB):
            continue  # only our own resources
        try:
            status, body = get(url)
        except Exception as e:  # HTTPError, timeouts
            problems.append(f"{url}: {e}")
            continue
        if status != 200:
            problems.append(f"{url}: HTTP {status}")
        if not re.search(r"<title>\s*\S", body, re.I):
            problems.append(f"{url}: no <title>")
        if not re.search(r'<a\b[^>]*href=["\']/["\']', body):
            problems.append(f"{url}: no link back to the hub")
        print(f"checked {url}")

    if problems:
        print("live_check: FAILED")
        for x in problems:
            print("  - " + x)
        return 1
    print(f"live_check: ok ({len(p.cards)} resource(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
