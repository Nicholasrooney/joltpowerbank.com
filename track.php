<?php
/* Receives one stats event from assets/site.js (navigator.sendBeacon). Always answers 204. No cookies are set. */
require_once __DIR__ . '/includes/stats.php';
header('Cache-Control: no-store');
header('X-Robots-Tag: noindex');
$host = preg_replace('/:\d+$/', '', strtolower((string) ($_SERVER['HTTP_HOST'] ?? '')));
$origin = (string) ($_SERVER['HTTP_ORIGIN'] ?? $_SERVER['HTTP_REFERER'] ?? '');
if (($_SERVER['REQUEST_METHOD'] ?? '') === 'POST'
    && ($origin === '' || preg_replace('/^www\./', '', strtolower((string) parse_url($origin, PHP_URL_HOST))) === preg_replace('/^www\./', '', $host))
    && empty($_COOKIE['jolt_staff'])) {
    $in = $_POST ?: (json_decode((string) file_get_contents('php://input'), true) ?: []);
    try { stats_record($in, mb_substr((string) ($_SERVER['HTTP_USER_AGENT'] ?? ''), 0, 400), (string) ($_SERVER['REMOTE_ADDR'] ?? ''), $host); } catch (Throwable $e) {}
}
http_response_code(204);
