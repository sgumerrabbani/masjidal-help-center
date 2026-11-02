<?php
/**
 * Plugin Name: Masjidal Help Center Preview
 * Description: Adds a separate static help-center preview and an admin shortcut. Existing pages, articles, and menus are preserved.
 * Version: 2026.11.02
 * Requires at least: 5.8
 * Requires PHP: 7.4
 * Update URI: https://github.com/sgumerrabbani/masjidal-help-center
 */

if (!defined('ABSPATH')) {
    exit;
}

function masjidal_help_center_preview_admin_page() {
    if (!current_user_can('manage_options')) {
        return;
    }
    $preview_url = plugins_url('site/index.html', __FILE__);
    echo '<div class="wrap"><h1>Masjidal Help Center Preview</h1>';
    echo '<p>The new help center is installed alongside your existing Knowledge Base. This plugin does not update articles, menus, redirects, or WordPress settings.</p>';
    echo '<p><a class="button button-primary" target="_blank" rel="noopener noreferrer" href="' . esc_url($preview_url) . '">Open new help center</a></p>';
    echo '<p>Preview address: <code>' . esc_html($preview_url) . '</code></p>';
    echo '<h2>Before switching Help links</h2><p>Check the preview while logged out, including articles, pictures, search, mobile navigation, and back links. Keep the existing Knowledge Base available during review.</p>';
    echo '<p>Article edits for this version are made in the project repository. Changes to the old WordPress Knowledge Base do not automatically update this static preview.</p>';
    echo '<p>This is a public preview. Deactivating the plugin removes its admin shortcut but does not restrict access to the static HTML files. Keep the plugin files installed while any Help links point to this version.</p></div>';
}

add_action('admin_menu', function () {
    add_management_page('Masjidal Help Center Preview', 'Masjidal Help Preview', 'manage_options', 'masjidal-help-center-preview', 'masjidal_help_center_preview_admin_page');
});

add_filter('plugin_action_links_' . plugin_basename(__FILE__), function ($links) {
    if (current_user_can('manage_options')) {
        array_unshift($links, '<a target="_blank" rel="noopener noreferrer" href="' . esc_url(plugins_url('site/index.html', __FILE__)) . '">Open preview</a>');
    }
    return $links;
});
