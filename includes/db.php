<?php
/* SQLite storage for website stats. The file lives in data/, which is web-blocked and never committed. */
require_once __DIR__ . '/config.php';

function db(): PDO
{
    static $pdo = null;
    global $config;
    if ($pdo) return $pdo;
    $dir = dirname($config['db_file']);
    if (!is_dir($dir)) @mkdir($dir, 0750, true);
    $pdo = new PDO('sqlite:' . $config['db_file'], null, null, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC]);
    $pdo->exec('PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 3000;');
    $pdo->exec('CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT NOT NULL, created_at TEXT NOT NULL,
        event TEXT NOT NULL, page TEXT, label TEXT, detail TEXT, source TEXT, medium TEXT, campaign TEXT,
        device TEXT, tz TEXT, visitor TEXT)');
    $pdo->exec('CREATE INDEX IF NOT EXISTS ev_day ON events(day, event)');
    $pdo->exec('CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT)');
    return $pdo;
}
function db_all(string $sql, array $p = []): array { $s = db()->prepare($sql); $s->execute($p); return $s->fetchAll(); }
function db_val(string $sql, array $p = []) { $s = db()->prepare($sql); $s->execute($p); return $s->fetchColumn(); }
function db_run(string $sql, array $p = []): void { db()->prepare($sql)->execute($p); }
function setting_get(string $k): ?string { $v = db_val('SELECT value FROM settings WHERE name = ?', [$k]); return $v === false ? null : $v; }
function setting_set(string $k, string $v): void { db_run('INSERT INTO settings(name, value) VALUES(?, ?) ON CONFLICT(name) DO UPDATE SET value = excluded.value', [$k, $v]); }
