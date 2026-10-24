# J.O.I. Cinematic Portfolio

A static HTML, CSS and JavaScript portfolio for Odukoya Joel, a software developer in Lagos, Nigeria. Project enquiries go directly to Joel.

The site has eight HTML pages, no runtime package dependencies and a CSS light-field hero. It works on a static host. The upload helper only prepares a clean copy; it does not add a framework or runtime build requirement.

## Run locally

From the project folder, run:

    python -m http.server 8080

Open http://localhost:8080. A local server mirrors a static deployment. Google Fonts are optional; system font fallbacks are included.

## Pages

- index.html - portfolio home, selected projects, technologies and ambient CSS light field
- projects.html - project list
- project-caleb.html, project-school.html - individual project pages
- about.html - profile and portrait
- services.html - Joel's services and quote requests
- contact.html - direct contact and email draft form
- 404.html - not-found page

The home hero keeps three staggered pairs of broad violet, coral and teal CSS gradient bands with soft trails and subtle texture. These atmospheric bands travel across the hero in 18, 22 and 26 second loops.

CSS starts the bands automatically, including when JavaScript is disabled. No interaction is required, and no library or external image asset is loaded for the effect. The system's reduced-motion setting shows a still light field.

## Project evidence

- Caleb NiceOne Property: the public source repository documents a seven-page static site, a goal-based property brief and a visitor-reviewed WhatsApp enquiry handoff. The live homepage and Property Finder were captured on 22 October 2026 and are shown in the case study. The homepage capture documents the published interface; its property hero is labeled as a concept illustration. No enquiry or conversion metrics were supplied.
- Now Foundation School: the case page uses a viewport screenshot of the live homepage captured in October 2026. The case page describes its programme pages and admission/contact routes. No traffic or admission metrics were supplied.

The Services concept artwork is labeled as illustration. The technology note maps HTML, CSS and JavaScript to the two published sites. The other listed tools are broader toolkit experience without a public case-study mapping yet.

## Images and identity

The About page uses the supplied portrait. `assets/joel-enhanced.webp` is an 800 x 800 WebP display copy made from the original 400 x 400 `assets/joel.jpg`; it uses a conventional resize and light tonal adjustment, not generative editing. The WebP is about 22 KB; the supplied original is retained in the editable source folder. Upscaling cannot restore detail absent from the original.

`assets/og-portfolio.png` is a 1200 x 630 branded Open Graph and Twitter preview image. Social metadata on each page points to it using the configured domain `odukoyajoel.name.ng`.

## Contact and quote workflow

Quote requests and the contact form prepare an email draft for `ODUKOYAJOEL@ZOHOMAIL.COM`; the visitor sends it from their email app. The direct email is also copyable on the Services and Contact pages, and the phone link remains visible. The site has no server-side form endpoint and does not collect or store messages. No WhatsApp destination is listed for Joel because a public WhatsApp number was not verified.

## Prepare a clean deploy folder

Run:

    python scripts/prepare-publish.py

Upload the contents of `publish/` to the selected static host. The folder includes only the HTML pages, CSS, JavaScript, favicon, robots.txt, sitemap.xml and assets referenced by the site. It excludes the ZIP archive, tests, scripts and development documents. The script can be run again after edits to refresh the folder.

For an upload ZIP, run `python scripts/build-publish-archive.py` after preparing the folder. `J.O.I.-Portfolio-Publish.zip` contains the same site files with `index.html` at the archive root. Extract it into the host's document root or upload it through a host that accepts ZIP deployments.

Refresh the editable source bundle separately with `python scripts/build-source-archive.py`. It includes the source documents and the current `publish/` folder, and omits ZIP files and generated `preview/` captures.

The source pages keep navigation and footer markup in HTML so links remain available if JavaScript is disabled. Keep those shared elements consistent across pages when editing. The stylesheet has been reformatted and obsolete selectors from earlier page designs have been removed.

To use `odukoyajoel.name.ng`, configure that domain and its DNS with the selected host. No hosting or DNS was changed as part of this revision. Use `J.O.I.-Portfolio-Publish.zip` for upload; `J.O.I.-Cinematic-Portfolio-Revision.zip` is the editable source bundle.

For Truehost with an active cPanel hosting plan, open the hosting service in the client area and enter cPanel. Under Domains, find the document root for `odukoyajoel.name.ng`. Open that directory in File Manager, upload `J.O.I.-Portfolio-Publish.zip`, and extract it there so `index.html` sits directly in the document root (usually `public_html` for the main domain). Use the DNS/nameservers supplied by that hosting service. See [Truehost's upload guide](https://truehost.com/support/knowledge-base/how-to-upload-a-website-to-your-cpanel-2/).

## Checks

Run the offline source checks with:

    python tests/smoke.py

See `QA_REPORT.md` for checks performed and browser-verification limits.
