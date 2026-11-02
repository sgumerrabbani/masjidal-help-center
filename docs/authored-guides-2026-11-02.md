# QR-code and DST guides - November 2, 2026

Added qr-codes and daylight-saving-time through assets/content/authored-guides.json. The shared content override loader preserves these articles when imported WordPress content is refreshed. The site now has 59 guides.

QR workflow and Professional-plan scope were supplied by the user. Five existing screenshots support the Image option, QR Code tile/editor, and compatible theme selection. Published references: https://help.masjidal.com/knowledge-base/displaying-images/ and https://help.masjidal.com/knowledge-base/qr-code-on-timing-screen/.

DST coverage follows the user's distinction between account information for Salah/Iqamah and the player's own clock. Existing screenshots verify Account > Masjid Info > Timezone and the bottom-right Masjidal logo leading to a screen with Android Settings. The date/time submenu is described with device-version variation, rather than asserting an unverified Setup menu.

Sources: https://help.masjidal.com/knowledge-base/masjid-information/, https://help.masjidal.com/knowledge-base/settings/, https://help.masjidal.com/knowledge-base/salah/, https://help.masjidal.com/knowledge-base/iqamah/, https://help.masjidal.com/knowledge-base/time-sync/, and https://support.google.com/android/answer/12461729?hl=en plus https://support.google.com/android/answer/2841106?hl=en. No signed-in portal settings or physical devices were changed/tested.

Both articles passed 16 Chromium/Firefox article/viewport cases at 1440, 768, 390, and 320px. Checked decoded image loading, fonts, horizontal overflow, headings, category return destinations, search discovery, and runtime errors. Both extraction regression tests and JavaScript syntax checks passed. Published-inventory coverage remains complete for all 49 public WordPress articles.

Rebuilt artifacts/masjidal-help-center-upload.zip with both guides. GitHub CLI is signed out; commits are local until authentication is restored. The live preview has not received these two guides yet. WordPress was not edited.
