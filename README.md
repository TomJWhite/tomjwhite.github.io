# Tom White portfolio

Static portfolio and CV site published at [tomjwhite.github.io](https://tomjwhite.github.io/).

## Structure

- `index.html` contains the site's content and page structure.
- `css/styles.css` contains the bundled Bootstrap Resume theme and local overrides.
- `js/scripts.js` provides dependency-free navigation behaviour.
- `cv/build_cv.py` is the reproducible source for the two-page, ATS-readable CV PDF.
- `assets/` contains the CV, portfolio reports, notebook export, and images.

The site has no package manager or build step. It can be previewed with any local static-file server.

Run `node tests/site-check.mjs` before submitting changes. The same dependency-free check runs automatically on pull requests.

Rebuild the CV with `python cv/build_cv.py` from the repository root. The script writes the published file to `assets/Tom_White_C.V.pdf`.

## Publishing

GitHub Pages publishes the repository root from the `master` branch. Work should be reviewed on a feature branch before it is merged into `master`, because a merge to the publishing branch updates the live site.

Google Analytics is configured through a single Google tag using measurement ID `G-73MPK6YJRW`. Its external endpoints and inline initialiser are restricted by the Content Security Policy and verified by `tests/site-check.mjs`.
