# Masjidal Help Center

Static, responsive help center styled to match https://mymasjidal.ca/.

## Content and branding

- Nine help categories and 54 guides, including API documentation based on the supplied Masjidal Server Key Guide.
- Official logo, product imagery, and article screenshots stored locally. Every guide tile includes an image and a specific description.
- Poppins fonts stored locally; official blue (#0047AB), masjid green, white, and light gray palette.
- The Widgets guide documents the current portal editor and installation flow. Legacy WordPress plugin instructions are clearly labeled.
- Search covers titles and article text. Mobile navigation and product menus support keyboard interaction.

## Preview

Run `python -m http.server 4173` from this directory, then visit http://localhost:4173/.

## Refresh content

Install `requests`, `beautifulsoup4`, `pypdf`, and `pillow`, then run `python scripts/import_content.py`.
The enrichment script adds descriptions, repairs legacy screenshot URLs, and builds API guides from `assets/docs/Masjidal-Server-Key-Guide.pdf`.

The import manifest, original source URLs, and asset mappings are in `assets/content-sources.json`. Originally imported on October 7, 2026; all source guides re-audited on October 20, 2026.

## Validation

Install Python Playwright and its Chromium browser, then run `python scripts/verify.py` while the preview server is running. This checks every article at desktop, tablet, and mobile widths, image loads, horizontal overflow, mobile navigation, and search. Screenshots are saved in `artifacts/`.

## Hosted preview

The GitHub Actions workflow in `.github/workflows/pages.yml` deploys the static site to GitHub Pages whenever `main` is updated. Enable GitHub Pages with GitHub Actions as its source.

Expected preview URL: https://sgumerrabbani.github.io/masjidal-help-center/

## WordPress rollout

See [the manual WordPress rollout and rollback instructions](docs/wordpress-rollout.md) for hosting the new help center alongside the existing site. No WordPress changes are made by the deployment workflow.

The current Widgets guide is maintained in `assets/content/widget.html`. Run `python scripts/content_overrides.py` after editing it; imports also apply this override automatically.

## Full audit and upload package

See [the audit report](docs/qa-report.md) for coverage, fixes, and verification limits. With the local server running, `python scripts/audit_site.py` checks every route in Chromium and Firefox, including fonts, resources, navigation, search, and email options. Install both engines with `python -m playwright install chromium firefox`.

`python scripts/audit_sources.py --refresh` audits/reimports published guide text and screenshots using ignored local snapshots, then `python scripts/enrich_content.py` applies authored content and presentation changes. `python scripts/audit_links.py` checks external informational links without executing state-changing URLs.

`python scripts/package_site.py` builds `artifacts/masjidal-help-center-upload.zip` and `docs/redirect-map.csv`. The ZIP contains the static site only. The redirect map is a proposal for manual review, not installed configuration.
