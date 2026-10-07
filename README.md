# Masjidal Help Center

Static, responsive help center styled to match https://mymasjidal.ca/.

## Content and branding

- Nine help categories and 51 guides, including API documentation based on the supplied Masjidal Server Key Guide.
- Official logo, product imagery, and article screenshots stored locally. Every guide tile includes an image and a specific description.
- Poppins fonts stored locally; official blue (#0047AB), masjid green, white, and light gray palette.
- Article source links retained. Videos and the interactive website widget generator open the official resource.
- Search covers titles and article text. Mobile navigation and product menus support keyboard interaction.

## Preview

Run `python -m http.server 4173` from this directory, then visit http://localhost:4173/.

## Refresh content

Install `requests`, `beautifulsoup4`, and `pypdf`, then run `python scripts/import_content.py`.
The enrichment script adds descriptions, repairs legacy screenshot URLs, and builds API guides from `assets/docs/Masjidal-Server-Key-Guide.pdf`.

The import manifest, original source URLs, and asset mappings are in `assets/content-sources.json`. Imported on October 7, 2026.

## Validation

Install Python Playwright and its Chromium browser, then run `python scripts/verify.py` while the preview server is running. This checks every article at desktop, tablet, and mobile widths, image loads, horizontal overflow, mobile navigation, and search. Screenshots are saved in `artifacts/`.
