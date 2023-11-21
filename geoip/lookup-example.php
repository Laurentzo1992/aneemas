#!/usr/bin/env php
<?php

/**
 *
 * DB-IP.com database sample query code
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

// Include the DB-IP class
require "dbip.class.php";

try {

	// Check if we have a command line parameter
	if ($argc < 2) {
		die("usage: {$argv[0]} <ip_address>\n");
	}

	// Connect to the database
	$db = new PDO("mysql:host=localhost;dbname=test", "root", "");

	// Alternatively connect to MySQL using the old interface
	// Comment the PDO statement above and uncomment the mysql_ calls
	// below if your PHP installation doesn't support PDO :
	// $db = mysql_connect("localhost", "root", "");
	// mysql_select_db("test", $db);

	// Instanciate a new DBIP object with the database connection
	$dbip = new DBIP($db);

	// Alternatively instanciate a DBIP_MySQL object
	// Comment the new statement above and uncomment below if your PHP
	// installation doesn't support PDO :
	// $dbip = new DBIPMySQL($db);

	// Lookup an IP address
	$inf = $dbip->lookup($argv[1]);

	// Show the associated country
	echo "country = " . $inf->country . "\n";

} catch (DBIPException $e) {
	echo "error: {$e->getMessage()}\n";
	exit(1);
}