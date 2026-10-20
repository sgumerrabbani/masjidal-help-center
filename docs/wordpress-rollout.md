# Introduce the new help center while keeping the WordPress version

These are manual instructions only. No WordPress content, hosting configuration, plugins, or DNS was changed as part of the repository update.

The dashboard screenshot shows Pages, Knowledge Base, Media, Divi-related tools, WooCommerce, WP Rocket, and All-in-One WP Migration. The public site root is a broader Masjidal page; the current help-topic directory is at /help/. Keep this rollout scoped to help content.

## 1. Save a rollback copy

1. Ask the hosting administrator to take a full backup of both the WordPress database and files and confirm how to restore it. A WordPress content export alone is not a full backup.
2. Your dashboard includes All-in-One WP Migration. If you use it, open its Export screen, choose File, download the completed export, and keep it off the hosting server. Verify any restore limits or paid-extension requirements before relying on it; a hosting backup is another option.
3. Record the current Help navigation destination, currently /help/, and take screenshots of the old help landing page and menus.
4. Do not deactivate Divi, the Knowledge Base plugin, WooCommerce, or other shared plugins to hide the old help pages. The dashboard contains active commerce features, so avoid replacing the whole WordPress installation.

Reference: https://developer.wordpress.org/advanced-administration/security/backup/

## 2. Upload a separate preview

The repository is a standalone static website. Upload it through your hosting file manager or SFTP, not WordPress Media, Themes, or Plugins. WordPress dashboard access by itself does not provide the file access needed for this approach.

1. Download the current repository using GitHub → Code → Download ZIP, then extract it on your computer.
2. Sign in to the hosting control panel for help.masjidal.com, or ask its administrator for SFTP access. Do not share hosting passwords in chat.
3. Identify the document root for help.masjidal.com. Its existing WordPress installation will contain wp-admin, wp-content, wp-includes, and index.php.
4. Create a NEW folder inside that document root named help-v2. Do not replace index.php or upload into wp-admin or wp-includes.
5. Upload index.html and the assets, category, article, and al-iqamah folders into help-v2. Keep their directory structure. The other repository files and development scripts are not needed to serve the site.
6. Visit https://help.masjidal.com/help-v2/. Check the homepage, search, category tiles, screenshots, and several guides on desktop and phone. Confirm the Widgets guide includes the new editor, library script, Publish step, and Professional-plan note.
7. Leave the current /help/ page and /knowledge-base/ articles untouched while testing. A separate folder does not change their content.

The /help-v2/ preview is public unless the host adds access protection. For a private review, ask the host to password-protect that folder.

## 3. Direct visitors to the new version when ready

1. In WordPress, open Appearance → Menus if your theme exposes that screen. Select the menu that contains the Help link and record its current URL. If Divi Theme Builder owns the header instead, edit that header's menu or button destination.
2. Change only the Help destination to https://help.masjidal.com/help-v2/ and save. Do not change Settings → General's WordPress Address or Site Address.
3. Clear WP Rocket's page cache and any hosting/CDN cache, then test the header and footer Help links while logged out.
4. Existing direct links to /help/ and /knowledge-base/... still reach the old version. Updating a menu is not a redirect or a full archive. Keep them live until you have planned equivalent destinations for bookmarked article URLs.

This method leaves the WordPress homepage, store, and dashboard in place. Making the entire help.masjidal.com root serve the new site is a separate hosting migration; do not accomplish it by overwriting the WordPress root index files or changing Settings → Reading to a static HTML file.

## 4. Preserve or temporarily hide the old help center

Choose one of these after the new version has been tested:

### Keep it as a public legacy version

- Remove its menu link and keep /help/ available for existing bookmarks. Internally label it as the legacy help page if useful.
- Keep old article URLs working until you map them individually to new guides.

### Hide the old landing page but retain it for administrators

1. In Pages → All Pages, locate the page whose permalink is /help/.
2. Open Quick Edit or Edit. Use Private visibility, or change its status to Draft, then save. Do not delete it.
3. Clear WP Rocket and hosting/CDN caches and test /help/ in a private browser window.
4. This hides only the landing page. It does not hide the separate Knowledge Base articles or their media files.
5. If you also need to hide old articles, first map their URLs. Then use the Knowledge Base plugin's supported article visibility/access controls. Where its article editor provides normal WordPress status/visibility, use Private or Draft on the specific legacy articles. Test both direct article URLs and plugin search while logged out. Do not disable the whole plugin as an archiving shortcut.
6. For a full private archive of the whole old installation, have the host clone it to a password-protected staging site before any eventual cutover. Verify that clone works before removing public access to anything.

Private visibility is intended for permitted logged-in administrators/editors. Merely renaming a page or removing a menu link does not make it private. WordPress core does not provide a universal Archive toggle for an entire existing help system.

Reference: https://wordpress.org/documentation/article/content-visibility-classic-editor/

## 5. Roll back

1. Restore the Help menu destination to its recorded old URL.
2. If you made the old page or articles Private/Draft, restore their original Published/Public status.
3. Clear caches and verify the old page, search, and article links while logged out.
4. Leave help-v2 available for further testing, or ask the host to restrict access to that folder.

## If you only want to update the existing WordPress Widgets article

This does not install the new help center. It changes only the article in the old Knowledge Base.

1. In Knowledge Base, locate the current Widget/Website Integration article and open it for editing. Keep its permalink unless you are intentionally adding redirects.
2. Before changing it, save a draft copy of its text/layout or export the Divi layout if that article uses Divi. WordPress revisions can help, but should not be your only backup.
3. The new article source is assets/content/widget.html. Recreate its headings, lists, notes, and code examples in the article's existing editor. Use Code blocks or escaped HTML for the script and custom-element EXAMPLES so they are displayed rather than executed. Do not paste a whole site or its application JavaScript into the article editor.
4. Upload assets/images/widgets/editor-overview.png and publish-settings.png through Media → Add New. Insert them in the relevant steps with descriptive alternative text.
5. Preview the draft on phone and desktop. Confirm that the article says extra colors and theme options require Professional, and that examples contain YOUR_WIDGET_ID and YOUR_FRONTEND_KEY instead of a real account's values.
6. Click Update only when you are ready. Clear WP Rocket's cache and check the public article.

## Updating the new static version later

Edit assets/content/widget.html and run python scripts/content_overrides.py to refresh the site's content data. Commit and push to main to update GitHub Pages. A manually uploaded help-v2 copy must also be uploaded again unless your host is separately configured to deploy from GitHub; the GitHub Pages workflow does not update WordPress hosting.
