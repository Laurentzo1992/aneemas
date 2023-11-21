#!/usr/bin/env php
<?php

/**
 *
 * DB-IP.com database import script
 *
 * Copyright (C) 2018 db-ip.com
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 */

require "dbip.class.php";

$opts = getopt("f:d:t:b:u:p:");

$filename = @$opts["f"];
$type = @$opts["d"];

$dbname = @$opts["b"]
or $dbname = "dbip";

$table = @$opts["t"]
or $table = "dbip_lookup";

$username = @$opts["u"]
or $username = "root";

$password = @$opts["p"]
or $password = "";

if (!isset($type) && preg_match('/dbip-(country-lite|city-lite|country|location|isp|full)/i', $filename, $res)) {
	$type = $res[1];
}

if (!isset($filename) || !isset($type)) {
	die("usage: {$argv[0]} -f <filename.csv[.gz]> [-d <country-lite|city-lite|country|location|isp|full>] [-b <database_name>] [-t <table_name>] [-u <username>] [-p <password>]\n");
}

switch (strtolower($type)) {
	case "country-lite":	$dbtype = DBIP::TYPE_COUNTRY_LITE;	break;
	case "city-lite":		$dbtype = DBIP::TYPE_CITY_LITE;		break;
	case "country":			$dbtype = DBIP::TYPE_COUNTRY;		break;
	case "location":		$dbtype = DBIP::TYPE_LOCATION;		break;
	case "isp":				$dbtype = DBIP::TYPE_ISP;			break;
	case "full":			$dbtype = DBIP::TYPE_FULL;			break;
	default:				echo "invalid database type\n"; exit(1);
}

try {
		// Connect to the database
        $db = new PDO("mysql:host=localhost;dbname={$dbname};charset=utf8mb4", $username, $password);
        // Alternatively connect to MySQL using the old interface
        // Comment the PDO statement above and uncomment the mysql_ calls
        // below if your PHP installation doesn't support PDO :
        // $db = mysql_connect("localhost", $username, $password);
        // mysql_select_db($dbname, $db);

        // Instanciate a new DBIP object with the database connection
        $dbip = new DBIP($db);
        // Alternatively instanciate a DBIP_MySQL object
        // Comment the new statement above and uncomment below if your PHP
        // installation doesn't support PDO :
        // $dbip = new DBIPMySQL($db);

	$nrecs = $dbip->importFromCsv($filename, $dbtype, $table, function($progress) {
		echo "\r{$progress} ...";
	});
	echo "\rfinished importing " . number_format($nrecs) . " records\n";
} catch (DBIPException $e) {
	echo "error: {$e->getMessage()}\n";
}