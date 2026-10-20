# WordPress replacement: detailed upload, archive, cutover, and rollback guide

This is a manual deployment guide. No WordPress content, hosting configuration, DNS, plugins, or redirects have been changed by this project.

The new help center is a standalone HTML/CSS/JavaScript site. Its articles are edited in the repository, not in the WordPress dashboard. Your screenshot shows a WordPress installation with Knowledge Base, Divi-related tools, WooCommerce/subscriptions, WP Rocket, and All-in-One WP Migration. Preserve that installation while testing and replacing the help section.

## Choose the destination first

| Stage | New help center | Existing WordPress content |
|---|---|---|
| Review | https://help.masjidal.com/help-v2/ | Unchanged at /help/ and /knowledge-base/... |
| Simple launch | Keep /help-v2/; update Help navigation | Retained for bookmarks or made private after redirects |
| Stable-path launch | https://help.masjidal.com/help/ | Old landing page retained as /help-legacy/; old article URLs redirected individually |

Recommended: test in /help-v2/, then choose the simple launch or the stable /help/ path. Replacing the entire help.masjidal.com root is a different migration; see the final section before considering that option.

## Phase 1: prepare access and a rollback record

1. Sign in to WordPress at the normal administrator address. Open the public site in a separate private/incognito browser window so you can compare the logged-out experience.
2. Open Pages → All Pages. Find the page whose permalink is /help/. Record its title, permalink, visibility, and publication status. Do not edit it yet.
3. Open Appearance → Menus if present. Find the Help link in the menu used by the public header; record its complete destination and menu name. Check the footer and mobile menus too. If the header is built in Divi Theme Builder, record that header template and which menu its Menu module uses.
4. Open Knowledge Base and record its existing article URLs and any configured landing page. The supplied docs/redirect-map.csv covers the imported guides; review it against the site's current URL list. It is a proposed mapping, not an installed redirect configuration.
5. Confirm you have hosting file-manager or SFTP access for help.masjidal.com. WordPress administrator access alone does not provide the file access required to upload this static site. If you only have WordPress access, give this guide and the ZIP to the hosting administrator.
6. Make a small rollback note containing the old Help URLs, current page status, current menu assignments, and backup location. Save screenshots of the old landing page and menu configuration.

## Phase 2: back up the existing version

7. Use your host's backup tool to create a full backup of BOTH the WordPress database and files. Download a copy or confirm the off-server backup location and restore procedure. A WordPress Tools → Export content file is not a complete installation backup.
8. Your screenshot also shows All-in-One WP Migration. If using it, choose All-in-One WP Migration → Export, choose File, wait for the export to finish, and download the resulting backup. Verify restore/import limits for the installed version before relying on that file. Do not open Import on production as part of uploading the new static help center.
9. For a browsable private archive, ask the host to clone the existing installation to a separate staging/legacy location and password-protect it. Have the host use its staging safeguards for scheduled tasks, payments, and email. Open that archive and verify several old articles and screenshots before treating it as your rollback copy.
10. Keep the original production WordPress installation, database, plugin settings, and media in place during the preview. An exported backup preserves a point in time; it does not contain orders or edits made after that export.

Why both files and database matter: [WordPress backup documentation](https://developer.wordpress.org/advanced-administration/security/backup/).

## Phase 3: get the upload files

11. Use the supplied masjidal-help-center-upload.zip. It contains only the website files required for hosting. It is NOT a WordPress theme/plugin installation ZIP.
12. Alternatively, visit the GitHub repository, choose Code → Download ZIP, extract it, and select only index.html and these four folders: assets, category, article, al-iqamah.
13. The upload root must look like this:

```text
help-v2/
  index.html
  assets/
    css/
    fonts/
    images/
    js/
    ...
  category/
    index.html
  article/
    index.html
  al-iqamah/
    index.html
```

Do not nest the GitHub repository folder inside help-v2. The homepage must be help-v2/index.html, not help-v2/masjidal-help-center-main/index.html. Do not upload .git, scripts, tmp, or development screenshots. With the prepared ZIP, extract its CONTENTS directly into help-v2.

## Phase 4: upload a parallel preview without replacing WordPress

14. Open your host's file manager or connect over SFTP. Select the website/document root specifically assigned to help.masjidal.com. Do not assume it is the account's main public_html folder: a subdomain can have its own document root.
15. The current WordPress root normally contains wp-admin, wp-content, wp-includes, and index.php. Confirm with the host that this is the correct location. Do not overwrite or rename those files/directories.
16. Create a NEW folder named help-v2 inside that document root. Check that a real folder or WordPress route with that name is not already used for something else.
17. Upload the prepared ZIP into help-v2 and use the host's Extract action, or upload the extracted files/folders over SFTP. Once extraction succeeds, remove the uploaded ZIP from the public server folder; keep your local copy.
18. Confirm the file layout above. The assets directory must contain the local font files, screenshots, CSS, and JavaScript. Copying only index.html produces an empty or unstyled page.
19. Open https://help.masjidal.com/help-v2/. Keep the address ending with a slash. The new site's relative links work in this subfolder; no WordPress installation or database import is needed.
20. For a private review, ask the host to password-protect help-v2. A folder named preview or legacy is not private by itself. Do not apply a site-wide login restriction to the production WordPress installation.

If a physical file exists but the preview displays a WordPress 404, ask the host to check the document root and rewrite rules so existing static files/directories are served correctly. Do not replace the WordPress .htaccess file with an unverified snippet. If you see an index-of-files listing, verify index.html is directly in help-v2 and that the host serves it as a directory index.

## Phase 5: acceptance checks before changing any links

21. In a private browser window, verify the new landing page, all category tiles, and a long article. Confirm All Other Topics is last.
22. Open Screen Size and Website Widgets. Their normal text should use Poppins, headings should share the blue styling, and screenshots should load. On the Widgets guide, confirm the Professional note applies to extra colors and theme options.
23. Use the category back link, breadcrumb, browser Back, and browser Forward. Check an article opened from All Other Topics returns there, rather than jumping to a different category.
24. Search for screen size, widgets, API, and an unmatched phrase. Confirm useful results and the no-results message. Try mobile Menu, Products, and Escape/close behavior.
25. Click Contact us and Contact support. Confirm the email chooser shows info@masjidal.com and masjidsupport@masjidal.com respectively. Try Copy email address. Gmail/Outlook options open their compose interfaces; mail-app launch still depends on the visitor's default email configuration. Do not send test emails unless you intend to contact that recipient.
26. Check desktop, tablet, and a real phone. Scroll long pages, view code examples, and confirm no page-wide horizontal overflow. Code examples may scroll within their own boxes.
27. Check the original /help/, a known /knowledge-base/... article, the WordPress admin, and any existing account/store routes. They should be unchanged by the parallel upload.
28. If the preview was access-protected, remove only that folder's protection before directing public visitors or redirecting old URLs to it. Check again while logged out.

## Phase 6A: simplest launch, keeping the /help-v2/ URL

29. In WordPress, open Appearance → Menus. Select the menu recorded in Phase 1, expand the Help item, and change its destination to https://help.masjidal.com/help-v2/. Save the menu. If it is a WordPress Page item without an editable URL, add a Custom Link with that URL and the same Help label, place it in the same position, then remove the OLD MENU ITEM only. Removing a menu item does not delete its page.
30. If a Divi Theme Builder header owns navigation, open that header and identify its Menu module. Update the menu selected by that module through Appearance → Menus. If Help is a separate Button/Link module, update that module's link instead. Save the header layout and Theme Builder changes. Repeat for any separate mobile header or footer Help button. Theme Builder/Menu-module details depend on the installed Divi version; do not rebuild the header unnecessarily.
31. Clear caches: Settings → WP Rocket → Dashboard → Clear cache / Clear and preload cache, or the equivalent WP Rocket admin-toolbar action. Then clear the hosting/CDN cache if one is configured. Static files may be outside WP Rocket's cache; a hard refresh of the browser can also be necessary.
32. Test the public header, mobile menu, footer, and Help buttons in an incognito window. They should land on the new help center. WordPress Address, Site Address, homepage settings, and DNS remain unchanged.

References: [Divi global header workflow](https://www.elegantthemes.com/blog/divi-resources/how-to-build-a-global-header-with-divis-fullwidth-menu-module), [WP Rocket cache clearing](https://docs.wp-rocket.me/article/53-clear-wp-rocket-cache).

## Phase 6B: optional stable /help/ URL instead

Do this INSTEAD of 6A if you want the new help center to use /help/. Have the hosting administrator available because this requires a directory and an existing WordPress page to stop competing for the same route.

29. Keep /help-v2/ working while you prepare the cutover. In Pages → All Pages, open the old Help landing page. Record its ID and current URL. Change its slug to help-legacy and retain the page; do not delete its content. Verify its legacy URL and check whether the Knowledge Base plugin or any header button still points to its page ID.
30. Through hosting file manager/SFTP, copy the TESTED static files into a new physical help directory in the same document root. Do not overwrite the WordPress root index.php. The new homepage should be help/index.html. Keeping help-v2 as the tested source gives you a quick fallback during cutover.
31. Open https://help.masjidal.com/help/ in an incognito window. Confirm the new site is served. If WordPress or a redirect plugin sends it to help-legacy, ask the host to inspect route precedence and existing redirects. Do not keep adding competing redirect rules until it happens to work.
32. Repeat Phase 5 checks under /help/, then update the public Help menu links to https://help.masjidal.com/help/ as described in 6A. Keep the old WordPress Help page private or published as a legacy entry according to Phase 8.
33. For this stable-path option, change /help-v2/ to /help/ in the DESTINATION column of docs/redirect-map.csv before applying any rules. Remove any row whose old and new destinations would be identical, especially /help/ → /help/, to avoid redirect loops.
34. Clear caches and test the new Help URL, old legacy page, WordPress admin, and any existing account/store paths. Leave help-v2 in place until you are satisfied with the cutover.

## Phase 7: preserve bookmarked article URLs with exact redirects

35. Review docs/redirect-map.csv with the hosting administrator. It contains the old landing/category/article paths and their proposed new destinations. The provided map defaults to /help-v2/; adjust it first if using /help/.
36. Verify each destination exists on your HOSTED domain. The query string is important: article/index.html?topic=screen-size is different from article/index.html without a topic. Do not accidentally send public visitors to localhost or a password-protected preview.
37. Configure individual URL redirects through the host's supported redirect system or an already approved WordPress redirect tool. The CSV is a review/planning sheet, not guaranteed to be directly importable into a particular plugin.
38. Start with temporary 302 redirects so the launch can be reversed easily. Match the old paths exactly and make an explicit trailing-slash policy. Match or discard unrelated OLD query strings intentionally; retain the new destination's topic query. Avoid broad rules that redirect /wp-admin, /wp-json, /wp-content, checkout/account routes, or all old articles to the homepage.
39. Test several old article URLs, including Widgets, Screen Size, a prayer-timings article, and an API-relevant link if one existed. Each should land on the corresponding new article in one deliberate redirect without a loop. Confirm the address bar keeps the expected topic query.
40. Once the switch is accepted and stable, decide whether to make those specific redirects permanent (301). Leave them temporary while you still expect a rollback. Do not configure a redirect for the root / unless you have separately planned a full-site migration.

## Phase 8: archive or temporarily disable the old version

Choose the level of preservation you want:

### A. Retain the old version publicly

41. Keep its page and Knowledge Base articles Published. Remove the old entry from public navigation and optionally label the old landing page Legacy Help Center. Existing bookmarks still work unless you configured redirects. This is a public legacy version, not a private archive.

### B. Hide selected old content without deleting it

41. After new destinations and any needed redirects are tested, open Pages → All Pages → the OLD Help page. Set Visibility to Private or change Status to Draft, then save. Confirm you are editing the old WordPress page, not trying to edit the static folder.
42. For old articles, use Knowledge Base → the relevant article's editor. If it supports normal WordPress status/visibility controls, make that article Private or Draft. If its plugin controls public access separately, use the plugin's documented access controls and test while logged out. Do not assume page privacy covers its articles.
43. Clear WordPress/hosting caches. Test the legacy landing page, direct old article URLs, the Knowledge Base search, and the new static guide. Verify public visitors either reach the intended redirect or cannot view the archived content.
44. Retain media files needed by the old installation and archive. Making pages private does not protect direct image/PDF URLs. Use a password-protected staging clone if the entire archived site, including its media, must be inaccessible to the public.
45. Do not deactivate the Knowledge Base plugin, Divi, WooCommerce, or subscriptions to archive a few help pages. Deactivation can remove functionality beyond the help section.

WordPress page/post visibility: [official documentation](https://wordpress.org/documentation/article/content-visibility-classic-editor/). There is no universal WordPress Archive switch for this whole mixed installation.

### C. Keep a private, browsable copy of the entire old installation

41. Use the host-created staging/legacy clone from Phase 2. Confirm that its database URLs, theme assets, and media resolve correctly at the legacy location and that the host protects it with authentication. Simply renaming the old WordPress directory is not a complete migration.
42. Verify a small set of archived pages while authenticated, then confirm access is blocked in a separate logged-out browser. Keep the downloadable backup as well.

## Phase 9: rollback without restoring the whole database

46. First disable ONLY the new help redirects you added. Otherwise they can keep sending old Help URLs back to the new site.
47. If you used 6A, restore the recorded old Help destination in the header, footer, and mobile menus.
48. If you used 6B, ask the host to rename the new PHYSICAL help folder to a clearly named temporary holding folder, so WordPress can handle /help/ again. Restore the old WordPress page slug to help and its original status/visibility. Remove any conflicting old-slug redirect. Keep the static files, rather than deleting them.
49. Restore any legacy articles you made Private/Draft to their original publication state. Clear caches and verify the old landing page, a few articles, and account/store routes while logged out.
50. Use a full database restore only if the targeted rollback cannot recover the previous configuration and the host has accounted for newer orders/edits. Restoring an older production database can remove records created since the backup. Normal menu/page/redirect rollback should not require it.

## Phase 10: updating the new help center later

51. Keep article updates in the repository. Most imported text is stored in assets/content-sources.json and generated assets/js/data.js; authored Widgets content is in assets/content/widget.html. Run the relevant content-generation scripts before publishing. Python scripts/content_overrides.py updates the authored guide and stamps a shared asset revision.
52. Run python scripts/audit_site.py against the local preview, review any failures, and run python scripts/package_site.py to create a fresh upload ZIP. The package script also regenerates the proposed redirect map.
53. Upload the updated static files to the same live help folder, keeping their paths. For a larger change, prepare a separate version folder and have the host switch directories atomically instead of mixing old/new JavaScript during an upload. Clear the host/CDN cache and test.
54. Pushing to main updates the GitHub Pages preview automatically. It does NOT update WordPress hosting unless that host is separately connected to the repository for deployment.

## If you want the whole subdomain root replaced

This guide's safe cutover changes the HELP SECTION. It does not retire WordPress, migrate WooCommerce/subscriptions, or move the whole subdomain to GitHub Pages. Your screenshot contains active commerce features, and the public root is broader than the help directory.

For a full-root replacement, give the host this request:

> Keep a verified, password-protected copy of the current WordPress site. Inventory the production homepage, help article URLs, administrator/account/store routes, payment callbacks, scheduled jobs, and media before changing the document root. Confirm which WordPress-backed endpoints must remain operational. Stage the static help center separately, plan exact legacy redirects and backend routing, confirm TLS and rollback, then propose a cutover that preserves required services.

The exact clicks and server configuration depend on your hosting provider, which has not been identified. Do not point help.masjidal.com at a different host, overwrite index.php, change WordPress Address/Site Address, or assume a new homepage setting performs this migration.

## If you want WordPress dashboard editing for the new articles

That requires converting the standalone site into a WordPress theme/plugin or migrating the content into WordPress-native article types and templates. Uploading the ZIP as a theme, pasting index.html into Divi, or using an iframe does not provide the same native editing experience. It is a separate implementation choice; the tested upload steps above preserve the current standalone design.
