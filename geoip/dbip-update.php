#!/usr/bin/env php
<?php

/**
 *
 * DB-IP.com database update tool
 *
 * Copyright (C) 2021 db-ip.com
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

const API_BASE = "https://db-ip.com/account";
const DEFAULT_CONF = "dbip-update.ini";

function apiRequest($path, $key) {
	$url = API_BASE . "/" . $key . "/db" . $path;
	if (($jsonData = file_get_contents($url)) === false) {
		throw new Exception("cannot fetch API result from {$url}");
	} else if (!isset($jsonData) || !$jsonData || (($resp = json_decode($jsonData)) === false)) {
		throw new Exception("cannot decode API result from {$url}");
	} else if (isset($resp->error)) {
		throw new Exception("API error: {$resp->error}");
	}
	return $resp;
}

function vEcho($s) {
	if (!$GLOBALS["verbose"]) {
		return false;
	}
	echo $s;
}

try {

	$exitCode = 0;
	$opts = getopt("k:d:f:o:zZqlnwb:u:p:t:c:D");
	$verbose = !isset($opts["q"]);

	if (isset($opts["c"])) {
		if (!file_exists($opts["c"]) || !is_readable($opts["c"])) {
			throw new Exception("cannot read configuration file {$opts['c']}");
		}
		$confName = $opts["c"];
	} else if (file_exists(__DIR__ . DIRECTORY_SEPARATOR . DEFAULT_CONF) && is_readable(__DIR__ . DIRECTORY_SEPARATOR . DEFAULT_CONF)) {
		$confName = __DIR__ . DIRECTORY_SEPARATOR . DEFAULT_CONF;
	}

	if (isset($confName)) {
		if (($conf = parse_ini_file($confName)) === false) {
			throw new Exception("cannot parse configuration file {$confName}");
		}
		$confMap = [
			"accountKey" => "k",
			"dbType" => "d",
			"format" => "f",
			"outputDir" => "o",
			"outputFileName" => "o",
			"dataSourceName" => "b",
			"dbUser" => "u",
			"dbPassword" => "p",
			"dbTableName" => "t",
		];
		foreach ($conf as $name => $value) {
			if (!isset($confMap[$name])) {
				throw new Exception("invalid configuration parameter {$name}");
			} else if (!isset($opts[$confMap[$name]])) {
				$opts[$confMap[$name]] = $value;
			}
		}
	}

	if (!isset($opts["k"]) || !$opts["k"]) {
		echo "usage: {$argv[0]} -k <accountKey> [-l] [-d <dbType>] [-f <format>] [-o <outputDir|outputFileName>] [-b <dataSourceName> [-u <dbUser>] [-p <dbPassword] [-t <dbTableName>] [-D]] [-c <configFile>] [-n] [-z|-Z] [-w] [-q]\n";
		echo " -l  list available items and exit\n";
		echo " -n  request new items only\n";
		echo " -z  fetch uncompressed file (default for mmdb format)\n";
		echo " -Z  fetch compressed file (default for csv format)\n";
		echo " -w  overwrite destination file if it already exists\n";
		echo " -b  PDO DSN for database update (ie. \"mysql:host=localhost;dbname=dbip\")\n";
		echo "   -u  database username (default 'root')\n";
		echo "   -p  database password (default '')\n";
		echo "   -t  name of database table (default 'dbip_lookup')\n";
		echo "   -D  do not use a temporary table (table specified by -t must be empty)\n";
		echo " -q  be quiet\n";
		exit(1);
	}
	$apiKey = $opts["k"];

	if (!isset($opts["d"])) {
		$dbList = apiRequest("/", $apiKey);
		if (count((array)$dbList) > 1) {
			vEcho("Use -d to select a database type :\n");
			foreach ($dbList as $dbType => $dbInfo) {
				echo $dbType . "\n";
			}
			exit();
		} else {
			foreach ($dbList as $dbType => $dbInfo) {
				break;
			}
		}
	} else {
		$dbType = $opts["d"];
	}

	if (isset($opts["b"])) {
		if (isset($opts["o"])) {
			throw new Exception("Arguments -b and -o cannot be used in the same command line");
		}
		$dbUser = isset($opts["u"]) ? $opts["u"] : "root";
		$dbPassword = isset($opts["p"]) ? $opts["p"] : "";
		$dbTable = isset($opts["t"]) ? $opts["t"] : "dbip_lookup";
		$format = "csv";
		try {
			$dsn = $opts["b"];
			if (preg_match('/^mysql:/', $dsn)) {
				if (!preg_match('/charset=/', $dsn)) {
					$dsn .= ";charset=utf8mb4";
				}
				$dbQuoteChar = '`'; // backquote for MySQL
			} else {
				$dbQuoteChar = '"'; // double quote for ANSI SQL
			}
			$db = new PDO($dsn, $dbUser, $dbPassword);
			$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
			$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
			$dbUseTempTable = !isset($opts["D"]);
		} catch (PDOException $e) {
			throw new Exception("Cannot connect to database: {$e->getMessage()}");
		}
	} else {
		if (!isset($opts["f"])) {
			$filesList = apiRequest("/{$dbType}", $apiKey);
			vEcho("Use -f to specify a format for your {$dbType} subscription :\n");
			foreach ($filesList as $format => $fileInfo) {
				echo $format . "\n";
			}
			exit();
		}
		$format = $opts["f"];
	}
	$onlyNew = isset($opts["n"]);

	try {
		$queryString = $onlyNew ? "?new=1" : "";
		$fileInfo = apiRequest("/{$dbType}/{$format}{$queryString}", $apiKey);
		if ($onlyNew && !$fileInfo) {
			vEcho("there are no new downloads available\n");
			exit(0);
		}
	} catch (Exception $e) {
		throw new Exception("cannot access download info : {$e->getMessage()}");
	}

	if (isset($opts["l"])) {
		if (!isset($fileInfo)) {
			vEcho("no download file match\n");
			exit();
		}
		foreach ($fileInfo as $name => $value) {
			echo "{$name}: {$value}\n";
		}
		exit();
	}

	if (isset($opts["z"])) {
		$uncompress = true;
	} else if (isset($opts["Z"]) || ($format === "csv")) {
		$uncompress = false;
	} else {
		$uncompress = true;
	}

	$outputFile = "." . DIRECTORY_SEPARATOR . $fileInfo->name;
	if (isset($opts["o"])) {
		if (is_dir($opts["o"])) {
			$outputFile = $opts["o"] . DIRECTORY_SEPARATOR . $fileInfo->name;
		} else {
			$outputFile = $opts["o"];
		}
	}
	$sourcePrefix = $uncompress ? "compress.zlib://" : "";
	if ($uncompress && preg_match('/\.gz$/i', $outputFile)) {
		$outputFile = preg_replace('/\.gz$/i', '', $outputFile);
	}
	$outputTempFile = $outputFile . ".update-tmp";

	if (file_exists($outputTempFile) && !unlink($outputTempFile)) {
		throw new Exception("cannot delete temporary file {$outputTempFile}");
	} else if (!isset($db) && file_exists($outputFile) && !isset($opts["w"])) {
		throw new Exception("destination file {$outputFile} already exists, use -w to force overwrite");
	}

	vEcho("Starting update for {$dbType} ({$fileInfo->date})\n");
	if (!copy($sourcePrefix . $fileInfo->url, $outputTempFile, stream_context_create([], [ "notification" => function($notificationCode, $severity, $message, $messageCode, $bytesTransferred, $bytesMax) {
		static $totBytes, $prevPct = false;
		if ($bytesMax) {
			$totBytes = $bytesMax;
		}
		if ($bytesTransferred) {
			if (isset($totBytes) && $totBytes) {
				$pct = number_format(($bytesTransferred / $totBytes) * 100, 1);
			}
			if ($pct !== $prevPct) {
				vEcho("\rDownloading: " . number_format($bytesTransferred / 1024) . " KB" . (isset($pct) ? " ({$pct}%)" : ""));
				$prevPct = $pct;
			}
		}
	}]))) {
		throw new Exception("unable to download file to {$outputTempFile}");
	}
	vEcho("\rDownload completed: " . number_format(filesize($outputTempFile) / 1024, 1) . " KB\n");

	$checkPrefix = $uncompress ? "" : "compress.zlib://";
	if (isset($fileInfo->md5sum) || isset($fileInfo->sha1sum)) {
		vEcho("Verify signature: ");
		if (isset($fileInfo->md5sum)) {
			$md5sum = md5_file($checkPrefix . $outputTempFile);
			if ($md5sum !== $fileInfo->md5sum) {
				vEcho("MISMATCH {$md5sum} != {$fileInfo->md5sum}\n");
				throw new Exception("MD5 signature verification failed, file is probably corrupt or altered");
			}
			vEcho("[MD5] ");
		}
		if (isset($fileInfo->sha1sum)) {
			$sha1sum = sha1_file($checkPrefix . $outputTempFile);
			if ($sha1sum !== $fileInfo->sha1sum) {
				vEcho("MISMATCH {$sha1sum} != {$fileInfo->sha1sum}\n");
				throw new Exception("SHA1 signature verification failed, file is probably corrupt or altered");
			}
			vEcho("[SHA1] ");
		}
		vEcho("passed\n");
	}

	if (isset($db)) {
		$dbip = new DBIP($db, $dbQuoteChar);
		$relId = $dbType;
		if ($fileInfo->version) {
			$relId .= "-v{$fileInfo->version}";
		}
		switch ($relId) {
			case "ip-to-country-lite":	$importType = DBIP::TYPE_COUNTRY_LITE;	break;
			case "ip-to-city-lite":		$importType = DBIP::TYPE_CITY_LITE;		break;
			case "ip-to-country-v4":	$importType = DBIP::TYPE_COUNTRY_V4;	break;
			case "ip-to-location-v4":	$importType = DBIP::TYPE_LOCATION_V4;	break;
			case "ip-to-isp-v4":		$importType = DBIP::TYPE_ISP_V4;		break;
			case "ip-to-location-isp-v4":
			case "ip-to-full-v4":		$importType = DBIP::TYPE_FULL_V4;		break;
			case "ip-to-country-v3":	$importType = DBIP::TYPE_COUNTRY_V3;	break;
			case "ip-to-location-v3":	$importType = DBIP::TYPE_LOCATION_V3;	break;
			case "ip-to-isp-v3":		$importType = DBIP::TYPE_ISP_V3;		break;
			case "ip-to-location-isp-v3":
			case "ip-to-full-v3":		$importType = DBIP::TYPE_FULL_V3;		break;
			case "ip-to-location-v2":	$importType = DBIP::TYPE_LOCATION_V2;	break;
			case "ip-to-isp-v2":		$importType = DBIP::TYPE_ISP_V2;		break;
			case "ip-to-location-isp-v2":
			case "ip-to-full-v2":		$importType = DBIP::TYPE_FULL_V2;		break;
			default:					throw new Exception("unsupported database type");
		}
		if ($dbUseTempTable) {
			$tempTable = "dbip_update_" . time();
			$db->exec("drop table if exists {$dbQuoteChar}{$tempTable}{$dbQuoteChar}");
			$db->exec("create table {$dbQuoteChar}{$tempTable}{$dbQuoteChar} like {$dbQuoteChar}{$dbTable}{$dbQuoteChar}");
		} else {
			$tempTable = $dbTable;
		}
		$dbip->importFromCsv($outputTempFile, $importType, $tempTable, function($numRows) use ($fileInfo) {
			if ($numRows % 1000) {
				return false;
			}
			if (isset($fileInfo->rows) && $fileInfo->rows) {
				$pct = number_format(($numRows / $fileInfo->rows) * 100, 1);
			}
			vEcho("\rImporting: " . number_format($numRows) . " rows" . (isset($pct) ? " ({$pct}%)" : ""));
		});
		$numRows = (int)$db->query("select count(1) cnt from {$dbQuoteChar}{$tempTable}{$dbQuoteChar}")->fetchObject()->cnt;
		if ($dbUseTempTable) {
			$db->exec("drop table if exists {$dbQuoteChar}{$tempTable}_old{$dbQuoteChar}");
			$db->exec("rename table {$dbQuoteChar}{$dbTable}{$dbQuoteChar} to {$dbQuoteChar}{$tempTable}_old{$dbQuoteChar}, {$dbQuoteChar}{$tempTable}{$dbQuoteChar} to {$dbQuoteChar}{$dbTable}{$dbQuoteChar}");
			$db->exec("drop table {$dbQuoteChar}{$tempTable}_old{$dbQuoteChar}");
		}
		vEcho("\rDatabase updated: " . number_format($numRows) . " rows imported\n");
	} else {
		if (!rename($outputTempFile, $outputFile)) {
			throw new Exception("cannot rename temporary file {$outputTempFile} to {$outputFile}");
		}
		vEcho("Wrote {$outputFile}\n");
	}
	
} catch (Exception $e) {
	if ($stdErr = @fopen("php://stderr", "w")) {
		fwrite($stdErr, "ERROR: {$e->getMessage()}\n");
		fclose($stdErr);
	} else {
		echo "ERROR: {$e->getMessage()}\n";
	}
	$exitCode = 1;
} finally {
	if (isset($outputTempFile) && file_exists($outputTempFile)) {
		unlink($outputTempFile);
	}
	if (isset($db) && isset($tempTable) && $dbUseTempTable) {
		$db->exec("drop table if exists {$dbQuoteChar}{$tempTable}{$dbQuoteChar}");
		$db->exec("drop table if exists {$dbQuoteChar}{$tempTable}_old{$dbQuoteChar}");
	}
}
if ($exitCode) {
	exit($exitCode);
}
