# Standalone widget example - November 2, 2026

The new widget-demo/index.html page embeds the user's supplied frontend prayer and announcement snippets, with the current widget.js library in its head. It uses live Masjidal content and no mock prayer data. The example account differs from the Augusta screenshot; the page and email instruct other masjids to use their own portal embeds.

## Confirmed domain restriction

Before the user changed allowed domains, browser requests originating from https://sgumerrabbani.github.io returned HTTP 403 with Origin not allowed for this API key for settings, timings, and announcements. After the user added the preview hostname, the identical snippets returned HTTP 200, with saved settings, seven days of timings, and an announcements response. Both widgets rendered. The announcement list is currently empty, so the widget displays its normal no-announcements message.

## Implementation

- A single downloadable HTML file includes both embeds, the library, page styling, and a status check. Images/fonts use the existing public help-center assets.
- The status check reads the settings endpoint and observes actual widget content; an API rejection is explained rather than appearing as an unexplained blank area.
- The client-visible msj_pk_ key is embedded as intended for a website frontend. No server key is used.
- The static deployment workflow and upload packager include widget-demo/.
- The Widgets help article now makes domain authorization its own numbered Step 2, before library installation, with actual/staging/www hostname guidance and a link to the example.
- A ready-to-send email is saved locally in ignored artifacts/masjidal-widget-email.txt. No email was sent and no WordPress pages were edited.

## Validation

Using the real widget library and API from the allowed GitHub preview origin: Chromium and Firefox at 1440, 768, 390, and 320px (eight page/browser/viewport cases), both live widget contents, HTTP 200 responses, loaded fonts, zero horizontal overflow/runtime errors, and successful HTML downloads. The updated guide passed eight equivalent layout checks. Both content-extraction tests, published-inventory coverage, and JavaScript syntax checks passed. Desktop/mobile example screenshots and response summaries are in ignored tmp/widget-live-example/.

The current published Augusta page was previously found to contain only its legacy iframe and neither the new custom element nor its library. Its own frontend-key/domain configuration still needs a separate check after the new installation is published.
