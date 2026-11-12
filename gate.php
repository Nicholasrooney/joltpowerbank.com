<?php
// Site-wide password gate. The .htaccess sends every request here until the visitor has the jolt_gate cookie.
const GATE_PASSWORD = '0000';
const GATE_TOKEN = '8a5f583463b8bda299b4cb071dc5b5bd';   // must match the cookie value in .htaccess
header('X-Robots-Tag: noindex, nofollow');
header('Cache-Control: no-store');
$uri = $_SERVER['REQUEST_URI'] ?? '/';
if (!preg_match('#^/[^\s]*$#', $uri) || str_starts_with($uri, '//') || str_starts_with($uri, '/gate.php')) $uri = '/';
$error = false;
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST') {
    if (hash_equals(GATE_PASSWORD, (string)($_POST['password'] ?? ''))) {
        setcookie('jolt_gate', GATE_TOKEN, ['expires' => time() + 60 * 60 * 24 * 30, 'path' => '/', 'secure' => !empty($_SERVER['HTTPS']), 'httponly' => true, 'samesite' => 'Lax']);
        header('Location: ' . $uri, true, 303);
        exit;
    }
    usleep(800000);
    $error = true;
}
http_response_code(401);
?><!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex, nofollow">
<title>Jolt</title>
<style>
@font-face{font-family:Archivo;font-weight:900;src:url(/assets/fonts/archivo-latin-900-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:400;src:url(/assets/fonts/inter-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:Inter;font-weight:600;src:url(/assets/fonts/inter-latin-600-normal.woff2) format("woff2")}
*{box-sizing:border-box}html,body{height:100%;margin:0}
body{background:radial-gradient(ellipse at 50% 0%,rgba(57,255,106,.12),transparent 60%),#050505;color:#fff;font-family:Inter,system-ui,sans-serif;display:grid;place-items:center;padding:1.5rem}
.card{width:100%;max-width:360px;background:#0c0f0c;border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:2rem 1.6rem;text-align:center}
.logo{margin:0 0 1rem}.logo img{height:52px;width:auto}
p{color:#9aa39a;font-size:.9rem;margin:0 0 1.4rem}
input{width:100%;font:600 1.4rem Inter,sans-serif;letter-spacing:.5em;text-align:center;padding:.9rem;border-radius:12px;border:1.5px solid rgba(255,255,255,.25);background:#050605;color:#fff;outline:none}
input:focus{border-color:#39ff6a;box-shadow:0 0 0 3px rgba(57,255,106,.2)}
button{margin-top:.8rem;width:100%;padding:.95rem;border:0;border-radius:12px;background:#39ff6a;color:#04140a;font:600 .9rem Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;cursor:pointer}
.err{color:#ff6b6b;font-size:.85rem;margin:.8rem 0 0}
</style></head><body>
<form class="card" method="post" action="<?= htmlspecialchars($uri, ENT_QUOTES) ?>" autocomplete="off">
<h1 class="logo"><img src="/assets/brand/jolt-logo-white.svg" alt="Jolt" width="160" height="52"></h1>
<p>This site is private for now. Enter the password to continue.</p>
<input type="password" name="password" inputmode="numeric" aria-label="Password" placeholder="••••" autofocus required>
<button type="submit">Enter</button>
<?php if ($error): ?><p class="err" role="alert">Wrong password, try again.</p><?php endif; ?>
</form>
</body></html>
