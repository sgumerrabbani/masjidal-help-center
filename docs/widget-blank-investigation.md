# Widget blank-state investigation - November 2, 2026

## What was verified

The public loader https://widgets.masjidal.com/timetable/v0/widget.js returned HTTP 200 as JavaScript (318,877 bytes). The script was executed unchanged in Chromium and Firefox with controlled API responses. No real frontend/server keys, signed-in portal access, or masjid accounts were used. This isolates rendering behavior; it does not identify the failing configuration of any customer's page.

Library SHA-256: 15cfc4834780f3f14897acf6618bfffe5800a818d602775a912d661476801293

28 scenario/browser cases passed using scripts/audit_widget_runtime.py. Reproducible results and the downloaded snapshot are under ignored tmp/widget-investigation/.

## Confirmed behavior

| Scenario | Current result |
|---|---|
| Valid settings and non-empty prayer timings, premium flag true | Prayer widget renders |
| Valid settings and non-empty prayer timings, premium flag false | Prayer widget renders with basic styling |
| Valid settings, premium flag true, announcement data | Announcements render |
| Valid settings, premium flag false, announcement data | Entire announcement widget is blank |
| Settings endpoint HTTP 403 or 500 | Entire widget is blank |
| Settings response succeeds but omits data.settings | Entire widget is blank |
| Settings request blocked at network layer | Entire widget is blank |
| Prayer timings request fails | Prayer widget is blank |
| Prayer timings response contains an empty data.timings array | Prayer widget is blank |
| Unsupported type=announcements (plural) | Widget is blank |
| Missing frontend key | Widget is blank |
| Custom element attached before required attributes, then attributes set afterward | Widget stays blank; no retry when attributes change |
| Announcements request fails but settings are valid and premium-enabled | Renders No announcements at this time, masking the data-fetch failure |

The runtime requires a successful widgets response containing data.settings before either component is displayed. Its settings failure handler clears the readiness state and the render path returns null. Prayer rendering additionally requires at least one timings entry. The announcement render branch additionally requires settings.isPremium to be truthy. These are confirmed code conditions, not an inference that a particular customer needs a plan upgrade.

Separate unauthenticated GET probes to the actual widgets and timings endpoints both returned HTTP 401 with Missing or invalid API key and Access-Control-Allow-Origin: *. No authenticated API behavior or allowed-domain matching rules were tested.

## Customer diagnosis

Obtain one affected public page URL. Inspect the actual published page's script and custom element, then the /widgets, /timings, and /announcements responses. Check the response message before attributing a 401/403 to a specific cause. Check exact hostname, active frontend key, saved widget ID/configuration, content availability, account entitlement, blocked requests, and delayed execution. For an account believed to have premium access, a false isPremium flag requires a backend/account investigation rather than simply telling the customer to upgrade.

The supplied examples use the correct script endpoint and singular types. The library can work with these snippets when its inputs/API responses are valid. No customer-specific root cause can yet be confirmed because an affected page URL has not been supplied.

## Guide changes

Added premium-entitlement behavior, hostname checks, WP Rocket delay troubleshooting, a request/response diagnostic table, empty prayer-data checks, and the dynamic attribute-insertion case to assets/content/widget.html. These guide changes passed eight Chromium/Firefox viewport cases (1440, 768, 390, 320), image/font loading, heading, overflow, and runtime checks. Rebuilt the hosting ZIP. WordPress, API service, and remote widget code were not modified.

WP Rocket reference: https://docs.wp-rocket.me/article/1349-delay-javascript-execution (delays scripts and supports URL/keyword exclusions).

## Recommended changes for the widget service owner

- Show distinct loading/error states for missing/invalid configuration, authentication/permission errors, missing saved settings, API/network failures, and empty timing data.
- Show an eligibility message for an unavailable announcement widget instead of returning an empty element.
- Keep empty announcement data separate from a failed announcement request.
- Validate type, widget ID, and key early with an actionable message.
- Reinitialize when required attributes arrive/change; make connection/disconnection handling safe for page builders.

Those require changes in the widget/API codebase. This help-center repository cannot fix the hosted library or account entitlements.
