# tklearn

Hub page for free, self-contained study resources by Trisha Kunst.

Live: https://tkunst.github.io/

Each resource is its own GitHub Pages repo under `tkunst`, served at `https://tkunst.github.io/<repo>/`, and gets a card in `index.html`.

| Resource | Repo | Live |
|---|---|---|
| AP World Regions Map Quiz | [ap-world-regions-quiz](https://github.com/tkunst/ap-world-regions-quiz) | https://tkunst.github.io/ap-world-regions-quiz/ |

## Adding a resource

1. Create a public repo with a self-contained `index.html` and enable Pages (branch `main`, path `/`).
2. Add a "← All study resources" link to `/` at the top of its page.
3. Install the privacy hook in it (below).
4. Add a card to `index.html` here and a row to the table above.

Everything here is public. Keep pages generic: no student names, school or district names, teacher names, or anything that identifies a particular student.

## Privacy pre-push hook

`.githooks/pre-push` runs `scripts/privacy_scan.sh` and blocks a push if any locally configured private term appears in the pushed commits. Activate it once per clone:

```sh
scripts/install-hooks.sh
```

The term list lives outside the repo at `~/.config/privacy-gate/terms.txt`. The hook is fail-closed: with no term list, pushes are blocked.

## License

Content: CC BY-NC 4.0. Code: MIT. Third-party maps and images are excluded.
