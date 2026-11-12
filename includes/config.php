<?php
/*
 * Jolt site config for the stats tracker and the staff dashboard.
 *
 * STAFF PASSWORD: currently 123456789 (setup only). To change it, run
 *   php -r "echo password_hash('your-new-password', PASSWORD_DEFAULT), PHP_EOL;"
 * and paste the result below.
 */
$config = [
    'staff_password_hash' => '$2y$10$f57m3W0KxMaI5sLtUbXJPuErsu97xoDgNrotfAtE2X7S1.feZT1l6',
    'db_file'             => dirname(__DIR__) . '/data/jolt-stats.sqlite',
    'timezone'            => 'Europe/Dublin',
];
date_default_timezone_set($config['timezone']);
