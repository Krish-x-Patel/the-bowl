# The Bowl

Ramen, poke and Korean bowls, blending Korean, Japanese and American flavors.
369 Cobb Pkwy S, Marietta, GA 30060 · (770) 702-1129

To change a price or menu item, edit the `MENU` list in `tools/build.py`, then run `python3 tools/build.py` from this folder. It rebuilds `index.html`, so prices stay the same everywhere on the page.

To check the site: run `python3 -m http.server 8765` in this folder, then `node tools/check.js` (needs Playwright).

The site is unlisted: `<meta name="robots" content="noindex, nofollow">` keeps search engines from listing it. Remove that line from `tools/template.html` and `legal.html` when the owner is ready to go public.
