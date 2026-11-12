<?php
/*
 * Cookie-free website stats, counted on our own server.
 * Nothing is stored on the visitor's device and no IP address is kept: a daily visitor key is a hash of
 * IP + browser + a random salt that is replaced every day, so a person counts once per day and can never be traced.
 */
require_once __DIR__ . '/db.php';

const STATS_EVENTS = [
    'page_view'      => 'Page views',
    'click'          => 'Clicks (any link or button)',
    'app_click'      => 'App store / open app taps',
    'whatsapp_click' => 'WhatsApp taps',
    'form_view'      => 'Saw the quote form',
    'form_step'      => 'Quote form steps',
    'form_error'     => 'Quote form errors',
    'lead'           => 'Quote forms sent',
    'scroll'         => 'Scroll depth',
    'engaged'        => 'Stayed 30s+',
    'design_switch'  => 'Showcase design switched',
];

function stats_source(string $ref, string $own, string $utm, string $clid): array
{
    if ($utm !== '') return [strtolower(substr(preg_replace('/[^\w.-]/', '', $utm), 0, 40)), ''];
    if ($clid === 'gclid') return ['google', 'cpc'];
    if ($clid === 'fbclid') return ['facebook', 'paid-social'];
    $host = strtolower((string) parse_url($ref, PHP_URL_HOST));
    $own = preg_replace('/^www\./', '', $own);
    if ($host === '') return ['direct', ''];
    if ($own !== '' && str_ends_with($host, $own)) return ['internal', ''];
    foreach (['google' => ['google', 'organic'], 'bing' => ['bing', 'organic'], 'duckduckgo' => ['duckduckgo', 'organic'], 'yahoo' => ['yahoo', 'organic'],
              'instagram' => ['instagram', 'social'], 'facebook' => ['facebook', 'social'], 'fb.' => ['facebook', 'social'], 'tiktok' => ['tiktok', 'social'],
              'linkedin' => ['linkedin', 'social'], 'whatsapp' => ['whatsapp', 'social'], 't.co' => ['x', 'social'], 'chatgpt' => ['chatgpt', 'ai'],
              'perplexity' => ['perplexity', 'ai'], 'joltireland' => ['joltireland.com', 'referral']] as $needle => $res) {
        if (str_contains($host, $needle)) return $res;
    }
    return [substr(preg_replace('/^www\./', '', $host), 0, 40), 'referral'];
}
function stats_is_bot(string $ua): bool { return $ua === '' || (bool) preg_match('/bot|crawl|spider|slurp|preview|monitor|curl|wget|python|headless|lighthouse|facebookexternalhit/i', $ua); }
function stats_device(string $ua): string { if (preg_match('/ipad|tablet/i', $ua)) return 'tablet'; return preg_match('/mobi|iphone|android/i', $ua) ? 'phone' : 'desktop'; }
function stats_visitor(string $ip, string $ua): string
{
    $day = date('Y-m-d');
    $salt = setting_get('salt_' . $day);
    if (!$salt) {
        $salt = bin2hex(random_bytes(16));
        setting_set('salt_' . $day, $salt);
        db_run("DELETE FROM settings WHERE name LIKE 'salt_%' AND name <> ?", ['salt_' . $day]);   // old salts are thrown away
    }
    return substr(hash('sha256', $salt . '|' . $ip . '|' . $ua), 0, 32);
}
function clean(string $s, int $n): string { return mb_substr(trim(strip_tags($s)), 0, $n); }

function stats_record(array $in, string $ua, string $ip, string $host): void
{
    $event = (string) ($in['e'] ?? '');
    if (!isset(STATS_EVENTS[$event]) || stats_is_bot($ua)) return;
    [$source, $medium] = stats_source((string) ($in['ref'] ?? ''), $host, (string) ($in['us'] ?? ''), (string) ($in['clid'] ?? ''));
    if (($in['um'] ?? '') !== '') $medium = clean((string) $in['um'], 40);
    db_run('INSERT INTO events(day, created_at, event, page, label, detail, source, medium, campaign, device, tz, visitor) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)', [
        date('Y-m-d'), date('Y-m-d H:i:s'), $event,
        clean(preg_replace('/[?#].*$/', '', (string) ($in['p'] ?? '')), 120),
        clean((string) ($in['l'] ?? ''), 120), clean((string) ($in['d'] ?? ''), 200),
        $source, $medium, clean((string) ($in['uc'] ?? ''), 80),
        stats_device($ua), clean((string) ($in['tz'] ?? ''), 40), stats_visitor($ip, $ua),
    ]);
}
