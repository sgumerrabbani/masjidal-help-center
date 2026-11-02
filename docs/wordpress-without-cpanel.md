# Preview upload through WordPress, without cPanel

This alternative preserves the current WordPress Knowledge Base. It uses the normal plugin ZIP uploader to place the static help center in a separate folder. It does not import/replace articles, update menus or redirects, modify the database, change the theme, or rewrite the server configuration.

## Package

Run `python scripts/package_wordpress_preview.py` to build `artifacts/masjidal-help-center-wordpress-preview.zip`. Use this WordPress package in the plugin uploader; the original static upload ZIP is not a plugin.

The archive contains a small PHP plugin and the complete tested site under its own `site/` directory. The plugin only adds a Tools menu item and an Open preview shortcut for administrators. It does not download or execute code from GitHub.

## Prerequisites

- A working WordPress administrator account with permission to install plugins.
- A verified backup of the WordPress files and database before installation/cutover.
- A maximum upload size large enough for the package (about 60 MB), and a host that permits normal plugin installation. The uploader displays its limit. If permissions, upload limits, filesystem access, or a host policy prevent installation, recover hosting access or ask the hosting administrator; do not work around security restrictions.

## Install for parallel review

1. In WordPress, open Plugins > Add New > Upload Plugin.
2. Select `masjidal-help-center-wordpress-preview.zip`, then Install Now.
3. Activate Masjidal Help Center Preview.
4. Open Tools > Masjidal Help Preview > Open new help center.
5. Test the preview while logged out on desktop and a phone. Confirm existing `/help/` and old article addresses still work.

The preview address is normally:

`https://help.masjidal.com/wp-content/plugins/masjidal-help-center-preview/site/index.html`

Use the actual URL shown by the plugin: WordPress can have a custom content/plugin path. This alternative does not create `/help-v2/`. The files in this folder are public; the name preview does not make them private. Deactivation removes the admin shortcut but does not hide static files.

## Cutover and archive

After checking the installed preview, follow the existing `wordpress-rollout.md` menu-switch and old-article redirect steps, using the actual preview base URL instead of `/help-v2/`. The existing redirect CSV targets `/help-v2/` and must be regenerated/reviewed for this base; do not install those mappings unchanged.

Keep the old Knowledge Base installed and its content available during review. Save the old menu destinations before changing them. A rollback can restore those menu links and disable only the new redirects. Do not restore the whole WordPress database merely to undo a Help menu change.

The example widget page uses a frontend key that authorizes its own hosts. If you test that example on help.masjidal.com, authorize that hostname in the widget's Masjidal API-key settings. This is separate from help-center article/image rendering.

Article editing remains in the repository. Future static updates can be distributed as an updated plugin ZIP with a new version, retaining the same plugin directory. An installed preview must be checked on the actual host before any production navigation switch.

Reference: https://wordpress.org/documentation/article/manage-plugins/
