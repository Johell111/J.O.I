# Quality assurance and release notes

**Revision:** 24 October 2026
**Format:** Static HTML, CSS and JavaScript. No runtime package install is required.

## Checks performed

| Check | Result |
| --- | --- |
| Source smoke checks | **PASS** - `python tests/smoke.py` checked all 8 pages, 291 local references, page structure, identity, contact flow, JavaScript syntax and responsive/reduced-motion hooks. |
| Clean publish folder | **PASS** - `python scripts/prepare-publish.py` generated 32 files under `publish/`; the folder excludes archives, tests, previews, unreferenced artwork and development documents. `J.O.I.-Portfolio-Publish.zip` contains those same files with `index.html` at its root. |
| Raster and vector assets | **PASS** - the OG card, portrait, school capture and supplied portrait decode; all 14 local SVG files parse as XML. The school capture is 1440 x 1200 WebP (243 KB), the portrait derivative is 800 x 800 WebP (22 KB), and the share card is 1200 x 630 PNG (331 KB). |
| Share metadata | **PASS** - all 8 HTML pages reference the branded absolute OG/Twitter image URL and provide image dimensions and alt text. Social-platform crawler rendering was not checked. |
| Project evidence | **IMPROVED** - both case studies show live interfaces captured in October 2026. The Caleb page includes its homepage and Property Finder with a goal preselected. The published homepage hero is labeled as a concept illustration. The case page documents role, scope, implementation choices and enquiry flow; no conversion metrics were supplied. |
| Desktop/mobile browser rendering | **PASS IN CHROME PREVIEW** - the homepage was captured at 1280 x 800 desktop and emulated mobile widths of 320, 360 and 390 px. The name and intro remain readable, and all three mobile widths have no horizontal overflow. The homepage contains exactly the Caleb and school project cards. See the desktop and mobile captures in `preview/`. Other pages were not visually rechecked in this revision. |
| Clipboard and email-app behavior | **NOT VERIFIED IN A BROWSER** - the copy button has Clipboard API and legacy copy fallbacks; JavaScript syntax passed, but copy behavior and mailto handoff were not interactively tested. |
| Hero motion and fallback | **PASS IN CHROME PREVIEW** - the six atmospheric bands move automatically with 18/22/26 second CSS loops. No line-animation SVG or motion control remains. Emulated reduced-motion disables all band animations and keeps their transforms still. CSS motion also works without JavaScript. Performance on physical devices was not measured. |
| Domain connection | **NEEDS CONFIGURATION** - public A and NS lookups for `odukoyajoel.name.ng` returned DNS failure on 24 October 2026. The user identified Truehost Nigeria as the registrar. Hosting account access is not connected in this session. |
| Live deployment | **NOT PERFORMED** - the upload package is ready; no hosting or DNS was changed. |

## Image notes

The Caleb homepage capture shows the published interface and includes a property hero labeled as a concept illustration. Services artwork remains conceptual illustration. The Now Foundation School case page also shows a real capture of its published homepage. No business conversion or enquiry metrics were supplied for either case study.

The supplied About portrait remains in the editable source folder as `assets/joel.jpg` (400 x 400, 23 KB). The site uses `assets/joel-enhanced.webp` (800 x 800, 22 KB), which is a conventional resize and light tonal adjustment. Upscaling cannot add source detail.

## Preview

From the project folder, run:

    python -m http.server 8080

Open http://localhost:8080. The five PNG screenshots in `preview/` show the current hero at desktop and 320, 360 and 390 px mobile widths, plus its static reduced-motion composition. The preview files are excluded from the publish folder and source ZIP. Physical device performance remains to be checked.
