<?php
/* Staff login: one shared password (bcrypt hash in config.php), throttled attempts, session cookie only for staff. */
require_once __DIR__ . '/db.php';

function staff_start(): void
{
    if (session_status() !== PHP_SESSION_NONE) return;
    session_set_cookie_params(['httponly' => true, 'secure' => !empty($_SERVER['HTTPS']), 'samesite' => 'Lax', 'path' => '/']);
    session_name('jolt_staff');
    session_start();
}
function staff_logged_in(): bool { staff_start(); return !empty($_SESSION['ok']) && ($_SESSION['ua'] ?? '') === md5($_SERVER['HTTP_USER_AGENT'] ?? ''); }
function staff_try_login(string $pw): bool
{
    global $config;
    $key = 'fail_' . substr(hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? '') . date('YmdH')), 0, 20);
    $fails = (int) (setting_get($key) ?? 0);
    if ($fails >= 10) { sleep(2); return false; }          // 10 wrong attempts per hour per connection
    if (password_verify($pw, $config['staff_password_hash'])) {
        staff_start(); session_regenerate_id(true);
        $_SESSION['ok'] = 1; $_SESSION['ua'] = md5($_SERVER['HTTP_USER_AGENT'] ?? '');
        return true;
    }
    setting_set($key, (string) ($fails + 1)); usleep(600000);
    return false;
}
function staff_logout(): void { staff_start(); $_SESSION = []; session_destroy(); setcookie('jolt_staff', '', time() - 3600, '/'); }
function e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8'); }
