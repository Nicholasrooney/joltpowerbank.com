<?php
/* Jolt staff dashboard: website analytics from our own cookie-free tracker. */
require_once __DIR__ . '/../includes/auth.php';
require_once __DIR__ . '/../includes/stats.php';
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');

$err = '';
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST' && isset($_POST['password'])) {
    if (staff_try_login((string) $_POST['password'])) { header('Location: /staff/'); exit; }
    $err = 'Wrong password.';
}
if (!staff_logged_in()) { ?>
<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Jolt staff</title><link rel="stylesheet" href="/staff/staff.css"></head><body class="login">
<form method="post" class="login-card"><div class="logo">JOLT <span>staff</span></div>
<label>Password<input type="password" name="password" autofocus autocomplete="current-password" required></label>
<?php if ($err): ?><p class="err"><?= e($err) ?></p><?php endif; ?>
<button type="submit">Log in</button></form></body></html>
<?php exit; }

$range = in_array($_GET['r'] ?? '', ['1', '7', '30', '90', '365'], true) ? (int) $_GET['r'] : 30;
$to = date('Y-m-d'); $from = date('Y-m-d', strtotime('-' . ($range - 1) . ' days'));
$W = 'day >= ? AND day <= ?'; $P = [$from, $to];
$uv = fn(string $where = '1', array $p = []) => (int) db_val("SELECT COUNT(DISTINCT day || visitor) FROM events WHERE $W AND $where", array_merge($P, $p));
$n  = fn(string $where = '1', array $p = []) => (int) db_val("SELECT COUNT(*) FROM events WHERE $W AND $where", array_merge($P, $p));
$top = fn(string $col, string $where, array $p = [], int $lim = 10) => db_all("SELECT COALESCE(NULLIF($col,''),'(none)') AS k, COUNT(*) AS n, COUNT(DISTINCT day || visitor) AS u FROM events WHERE $W AND $where GROUP BY k ORDER BY n DESC LIMIT $lim", array_merge($P, $p));

$visitors = $uv("event = 'page_view'"); $views = $n("event = 'page_view'"); $leads = $n("event = 'lead'");
$appTaps = $n("event = 'app_click'"); $wa = $n("event = 'whatsapp_click'");
$funnel = [
    ['Visited the site', $visitors],
    ['Saw the quote form', $uv("event = 'form_view'")],
    ['1 · Picked a market', $uv("event = 'form_step' AND label = '1 · market'")],
    ['2 · Picked venues', $uv("event = 'form_step' AND label = '2 · venues'")],
    ['3 · Set customers', $uv("event = 'form_step' AND label = '3 · customers'")],
    ['4 · Started contact details', $uv("event = 'form_step' AND label = '4 · contact started'")],
    ['Tried to send with gaps', $uv("event = 'form_error'")],
    ['Sent the form', $uv("event = 'lead'")],
];
$daily = db_all("SELECT day, SUM(event='page_view') AS v, COUNT(DISTINCT CASE WHEN event='page_view' THEN visitor END) AS u, SUM(event='lead') AS l FROM events WHERE $W GROUP BY day", $P);
$byDay = array_column($daily, null, 'day'); $series = [];
for ($d = $from; $d <= $to; $d = date('Y-m-d', strtotime("$d +1 day"))) $series[] = ['d' => $d, 'v' => (int) ($byDay[$d]['v'] ?? 0), 'u' => (int) ($byDay[$d]['u'] ?? 0), 'l' => (int) ($byDay[$d]['l'] ?? 0)];
$max = max(1, ...array_column($series, 'v'));
$pct = fn($a, $b) => $b ? round($a / $b * 100, 1) . '%' : '–';
$live = db_all("SELECT created_at, event, page, label, detail, source, device FROM events ORDER BY id DESC LIMIT 60");
$names = STATS_EVENTS;
function bars(array $rows, string $title, string $hint = ''): void { $sum = max(1, array_sum(array_column($rows, 'n'))); ?>
<section class="card"><h2><?= e($title) ?></h2><?php if ($hint): ?><p class="hint"><?= e($hint) ?></p><?php endif; ?>
<?php foreach ($rows as $r): ?><div class="hbar"><span title="<?= e($r['k']) ?>"><?= e($r['k']) ?></span><b><?= (int) $r['n'] ?></b><i style="width:<?= round($r['n'] / $sum * 100) ?>%"></i></div><?php endforeach; ?>
<?php if (!$rows): ?><p class="muted">No data yet.</p><?php endif; ?></section>
<?php }
?><!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">
<title>Jolt · Website analytics</title><link rel="stylesheet" href="/staff/staff.css"></head><body>
<header class="top"><div class="logo">JOLT <span>staff</span></div><nav><?php foreach ([1 => 'Today', 7 => '7 days', 30 => '30 days', 90 => '90 days', 365 => '12 months'] as $r => $t): ?><a class="<?= $range === $r ? 'on' : '' ?>" href="?r=<?= $r ?>"><?= $t ?></a><?php endforeach; ?></nav><a class="out" href="/staff/logout.php">Log out</a></header>
<main>
<h1>Website analytics <small><?= e(date('j M', strtotime($from))) ?> – <?= e(date('j M Y', strtotime($to))) ?></small></h1>
<div class="kpis">
<div class="kpi"><b><?= number_format($visitors) ?></b><span>visitors</span></div>
<div class="kpi"><b><?= number_format($views) ?></b><span>page views</span></div>
<div class="kpi hl"><b><?= $leads ?></b><span>quote forms sent</span></div>
<div class="kpi"><b><?= $pct($uv("event = 'lead'"), $visitors) ?></b><span>visitors who sent a form</span></div>
<div class="kpi"><b><?= $appTaps ?></b><span>app download / open taps</span></div>
<div class="kpi"><b><?= $wa ?></b><span>WhatsApp taps</span></div>
</div>

<section class="card"><h2>Visits per day</h2><p class="hint">Bar = page views · green dot = a quote form sent that day</p>
<div class="chart"><?php foreach ($series as $s): ?><div class="col" style="height:<?= round($s['v'] / $max * 100) ?>%" title="<?= e(date('D j M', strtotime($s['d']))) ?>: <?= $s['v'] ?> views, <?= $s['u'] ?> visitors, <?= $s['l'] ?> forms"><?php if ($s['l']): ?><em><?= $s['l'] ?></em><?php endif; ?></div><?php endforeach; ?></div></section>

<section class="card"><h2>Quote form funnel</h2><p class="hint">Unique visitors reaching each step · % of visitors · drop from previous step</p>
<?php $prev = null; foreach ($funnel as [$label, $v]): ?>
<div class="fun"><span><?= e($label) ?></span><div class="fbar"><i style="width:<?= $visitors ? max(1, round($v / $visitors * 100)) : 0 ?>%"></i></div><b><?= $v ?></b><small><?= $pct($v, $visitors) ?><?php if ($prev !== null && $label !== 'Tried to send with gaps'): ?> · <?= $prev ? '-' . round((1 - $v / max(1, $prev)) * 100) . '%' : '' ?><?php endif; ?></small></div>
<?php if ($label !== 'Tried to send with gaps') $prev = $v; endforeach; ?></section>

<div class="grid">
<?php bars($top('source', "event = 'page_view' AND source <> 'internal'"), 'How people find the site', 'Search engine, social, ad (utm/gclid) or link'); ?>
<?php bars($top("source || ' / ' || COALESCE(NULLIF(medium,''),'-')", "event = 'page_view' AND source <> 'internal'"), 'Source / medium', 'Arrivals only (not clicks between our own pages)'); ?>
<?php bars($top('campaign', "event = 'page_view' AND campaign <> ''"), 'Ad & email campaigns', 'From utm_campaign links'); ?>
<?php bars($top('source', "event = 'lead'"), 'Forms sent, by source', 'Source of the page the form was sent from (internal = they browsed first)'); ?>
<?php bars($top('label', "event = 'lead'"), 'Forms sent, by market', 'IE / UK active leads, EU priority list, international waitlist'); ?>
<?php bars($top('page', "event = 'lead'"), 'Forms sent, by page'); ?>
<?php bars($top('page', "event = 'page_view'", [], 15), 'Top pages'); ?>
<?php bars($top('page', "event = 'page_view' AND source <> 'internal'"), 'Landing pages (first page people saw)'); ?>
<?php bars($top('label', "event = 'click'", [], 15), 'Most clicked links & buttons'); ?>
<?php bars($top("label || ' · ' || detail", "event = 'app_click'"), 'App taps: platform · where', 'iOS → App Store, Android → Google Play, desktop → store chooser'); ?>
<?php bars($top('detail', "event = 'form_step' AND label = '1 · market'"), 'Form step 1: market chosen'); ?>
<?php bars($top('detail', "event = 'form_step' AND label = '2 · venues'"), 'Form step 2: venues chosen'); ?>
<?php bars($top('label', "event = 'form_step' AND label LIKE '4 · filled%'"), 'Contact fields filled in'); ?>
<?php bars($top('label', "event = 'form_error'"), 'Fields missing when sending'); ?>
<?php bars($top('label', "event = 'scroll'"), 'How far people scroll'); ?>
<?php bars($top('device', "event = 'page_view'"), 'Devices'); ?>
<?php bars($top('tz', "event = 'page_view'"), 'Visitor time zone (rough location)'); ?>
<?php bars($top('label', "event = 'design_switch'"), 'Showcase designs viewed (preview bar)'); ?>
</div>

<section class="card"><h2>Live feed <small>last 60 events, newest first</small></h2>
<div class="tablewrap"><table><tr><th>Time</th><th>What</th><th>Page</th><th>Detail</th><th>Source</th><th>Device</th></tr>
<?php foreach ($live as $r): ?><tr><td><?= e(date('j M H:i', strtotime($r['created_at']))) ?></td><td><b><?= e($names[$r['event']] ?? $r['event']) ?></b><?php if ($r['label']): ?><br><small><?= e($r['label']) ?></small><?php endif; ?></td><td><?= e($r['page']) ?></td><td><small><?= e($r['detail']) ?></small></td><td><?= e($r['source']) ?></td><td><?= e($r['device']) ?></td></tr><?php endforeach; ?>
<?php if (!$live): ?><tr><td colspan="6" class="muted">No events yet. Visit the site in another browser (not logged in here) to see them arrive.</td></tr><?php endif; ?></table></div></section>
<p class="foot muted">Counted on our own server: no cookies, nothing stored on visitors' devices, no IP addresses kept. Your own visits are not counted while you're logged in here. Google Analytics (consenting visitors only) lives in your GA4 account.</p>
</main></body></html>
