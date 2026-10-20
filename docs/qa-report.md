# Help-center QA report

Reviewed October 20, 2026. This audit covers the static help-center website and its public documentation, not a live masjid's account or device configuration. WordPress was not edited.

## Result

- 54 guides, 9 categories, and 66 distinct local routes reviewed.
- 594 browser/page/viewport cases passed: Chromium at 1440, 1280, 1024, 900, 768, 390, and 320px; Firefox at 1440 and 390px.
- 200 distinct link targets inspected for valid local routes or documented external destinations.
- Every category tile clicked in both engines; contextual breadcrumb and category-return destinations checked.
- Every article's return link and browser Back/Forward exercised in Chromium. Shared search, no-results state, mobile menu, Products disclosure, Escape/close controls, and email choices checked in both engines.
- Visible email links checked for correct recipients and Gmail/Outlook compose destinations. Clipboard copying and focus restoration were separately checked in Chromium. No email was sent.
- All rendered image requests and local font requests succeeded. No page-wide horizontal overflow, browser runtime errors, or failing local HTTP resources remained in the full run.
- Poppins loading and computed article/body fonts checked on every route. Code examples retain monospace formatting intentionally.
- Desktop and mobile screenshots captured for all guides. Contact sheets covering all 54 desktop guides visually reviewed, with larger mobile checks of Screen Size, Widgets, Themes, and the legacy WordPress guide.
- The packaged upload was also checked under /help-v2/ in Chromium and Firefox, including font/image loading, relative links, and restored Get Started buttons.

Reproducible browser results and screenshots are generated under the ignored artifacts/full-audit directory by scripts/audit_site.py. The completed full matrix recorded 594 passing cases, zero runtime errors, and zero failing local resources.

## Repairs made

1. Removed the article-body system-font override. Article text now inherits Poppins consistently, alongside the existing blue headings, notes, tables, buttons, and code styling.
2. Corrected imported heading treatment so long explanatory paragraphs are not rendered as oversized headings. Reworked Screen Size into five numbered steps with the corresponding five screenshots.
3. Restored omitted source text, including the WordPress plugin-installation paragraph, zone instructions, and update reminders. The initial comparison identified 341 missing source word tokens, before adding the three additional guides.
4. Added linked guides missing from the original category-only import: Slideshow, Sponsor an Iftar Campaign, and Zakat ul-Fitr Campaign. They are now accessible through All Other Topics and search.
5. Preserved all 265 screenshot occurrences in the 45 published source guides. The complete site has 276 article-image occurrences after authored Widgets screenshots and derived TV guides are included. Import checks now assert source screenshot counts as well as complete source text coverage.
6. Recovered the two Get Started Learn More links stored in Divi's separate link-options data. They now navigate to Salah and Iqamah guides locally.
7. Routed equivalent help references to the new local guides/categories. Repaired the outdated masjid-information destination and used the working portal entry URL instead of deep links that returned 404.
8. Preserved the category context in guide URLs so returning from a guide opened within All Other Topics returns there, even when that guide is also listed in a product category.
9. Added intrinsic image dimensions to reserve screenshot space before lazy loading. This reduces layout shifts around article controls and navigation.
10. Added shared asset-revision URLs to all four entry pages, preventing different pages from retaining incompatible cached CSS/JavaScript versions after deployment.
11. Clearly labeled the older WordPress plugin/shortcode guide as legacy and linked new installations to the current Widgets method. Retained the legacy instructions and shortcode reference.
12. Replaced old add-to-cart trial destinations with the current informational pricing page. Trial availability is no longer presented as an action that adds a product to a cart.
13. Removed the stale Coming Soon label for Athan Clock content, which the current product page describes as available. Reframed an old app version number as an example rather than claiming it is the latest release.

## Content verification

- Compared all 45 published source article bodies with the importer output. All source text tokens were preserved before documented editorial updates, and all source screenshots were accounted for. Snapshots and comparison output are generated under tmp/content-audit.
- The revised Screen Size guide preserves the source's Settings → Display → HDMI → Screen Zoom → arrow-adjustment sequence and all five images.
- The Widgets guide was checked against the supplied editor and installation screenshots, including Publish, separate prayer/announcement embeds, frontend keys, and the Professional requirement for extra colors/theme options.
- All four API request examples were compared directly with the supplied PDF and matched. Endpoint parameters, version Accept header, x-api-key usage, server/frontend key distinction, rotation/disable guidance, and troubleshooting are retained.
- The update pipeline now handles bare text containers, nested screenshot wrappers, and Divi's out-of-line button destinations. Source link checks do not execute state-changing URLs.

Sources include the [published help directory](https://help.masjidal.com/help/), [Screen Size instructions](https://help.masjidal.com/knowledge-base/screen-size/), [legacy WordPress plugin instructions](https://help.masjidal.com/knowledge-base/wordpress/), the supplied Masjidal Server Key Guide PDF, and the user's Widgets screenshots. Current Athan Clock availability was cross-checked against the [official product page](https://mymasjidal.com/products/athan-frame).

## External services and limits

The final external-link check found 26 informational/resource URLs responding with HTTP 200, plus the Amazon Appstore URL. Amazon returned HTTP 500 to the Python checker, while a browser reached an HTTP 200 Amazon page. The original app-store destination is retained; listing availability, regional access, and any human verification/sign-in need manual confirmation with Amazon.

The source comparison verifies that documented information and images were preserved; it cannot independently prove protected portal behavior, billing eligibility, installed-device menus, app-store installation, or successful live API requests. Those require the relevant account/device. No live masjid settings, payments, subscriptions, API keys, WordPress content, DNS, or email delivery were changed or tested by making real transactions.

## WordPress deliverables

- docs/wordpress-rollout.md: 54 numbered steps covering backup, archive, upload, preview checks, menu cutover, optional stable /help/ URL, exact redirects, privacy, rollback, and future updates.
- docs/redirect-map.csv: 53 proposed exact old-to-new URL mappings, initially using temporary 302 redirects and the /help-v2/ destination. No rules have been installed.
- artifacts/masjidal-help-center-upload.zip: static-only upload package, built by scripts/package_site.py and tested in a subfolder. It is not a WordPress theme/plugin installer.
