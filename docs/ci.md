# CI for the tklearn study hub

The hub (`tkunst.github.io`) and every resource repo it links to share one CI setup. It was set up on 2026-10-16. Flying Fish was the minimum (the privacy pre-push hook only), and arbor-hills-monitor was the most to borrow from. This doc covers the hub; each resource repo has its own `docs/ci.md`.

## What runs

| Check | When | What it does |
|---|---|---|
| **ci: site-guard** (all repos) | every push / PR | `scripts/site_guard.py` fails the build on: an em-dash; anything loaded from another site (fonts, scripts, images, CSS `url()`, `fetch()`); any email address except the published contact; an AP mention without the College Board trademark notice; missing `lang`, `<title>`, viewport meta, or image alt text. In resource repos it also requires the link back to the hub. |
| **ci: smoke** (resource repos with interactive pages) | every push / PR | A headless-Chromium run of the page as a student would use it, at laptop and phone sizes, failing on any JavaScript error. See the resource repo's `docs/ci.md`. |
| **ci: links** (hub) | every push / PR | lychee link check of the hub's HTML and Markdown. Root-relative card links (`/ap-world-regions-quiz/`) point at other repos, so they are checked by `live` instead. |
| **live** (hub) | every push + Mondays ~7 AM Eastern + manual | `scripts/live_check.py`: on a push, waits until the published hub matches the commit (catches a Pages deploy that never landed); then opens every resource card and requires HTTP 200, a `<title>`, and a link back to the hub. The weekly run catches a resource that broke or went private. |
| **secrets** (all repos) | every push / PR | gitleaks over the full git history (same pinned, checksum-verified setup as arbor-hills-monitor). |
| **Dependabot** (all repos) | monthly | Bumps the workflow actions (and Playwright in repos with a smoke test). |

## Verified when set up

- The site guard flagged all 11 rule types on a deliberately bad sample page.
- The quiz smoke test failed when answer grading was broken and when page JavaScript was broken.
- Every check passed on its first GitHub run. The first Dependabot update (Playwright 1.60 to 1.63) passed CI and was merged.

## Deliberately not included

- **Bandit SAST and markdownlint:** there is no Python on the pages and almost no Markdown.
- **Monitor's data and scraper jobs:** nothing here to scrape or store.
- **Branch protection / required checks:** it would block direct pushes to `main`. Failed checks email the owner instead.
- **Privacy terms in CI:** the private term list stays in the local pre-push hook (`~/.config/privacy-gate/terms.txt`). Putting it in CI would mean storing the very names it protects on GitHub. Same decision as arbor-hills-monitor.

## Residual risk

The pre-push hook blocks only the terms in the local list. Other identifying details (teacher names, school names or initials, course specifics) are not blocked by any check, so every new resource needs a human read before its first push.

## Adding a resource repo

1. Copy `scripts/site_guard.py` from this repo unchanged. All copies must stay identical; if you change one, change them all.
2. Copy `.github/workflows/ci.yml` and `secrets.yml` and `.github/dependabot.yml` from an existing resource repo (for example `ap-world-regions-quiz`). Add a smoke test if the page is interactive.
3. Copy the privacy hook (`.githooks/pre-push`, `scripts/privacy_scan.sh`, `scripts/install-hooks.sh`) and run `scripts/install-hooks.sh`.
4. Add a card to the hub's `index.html`. The next `live` run checks it automatically.

## Running locally

```sh
python3 scripts/site_guard.py
python3 scripts/live_check.py              # checks the published site
python3 scripts/live_check.py --expect-current   # also waits for this commit to deploy
```
