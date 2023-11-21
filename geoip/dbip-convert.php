#!/usr/bin/env php
<?php

/**
 *
 * DB-IP.com CSV database format conversion tool
 *
 * Copyright (C) 2020 db-ip.com
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

$outputFormats = [
	"range" => function(array $csvData, $of, string $firstIpBin, string $lastIpBin): void {
		writeCSV($of, $csvData);
	},
	"cidr" => function(array $csvData, $of, string $firstIpBin, string $lastIpBin): void {
		array_shift($csvData);
		foreach (rangeToCIDR($firstIpBin, $lastIpBin) as $cidrNet) {
			$csvData[0] = $cidrNet;
			writeCSV($of, $csvData);
		}
	},
	"long" => function(array $csvData, $of, string $firstIpBin, string $lastIpBin): void {
		if (($firstIpLong = ip2long($csvData[0])) === false) {
			throw new Exception("invalid IP address for long conversion : {$csvData[0]}");
		} else if (($lastIpLong = ip2long($csvData[1])) === false) {
			throw new Exception("invalid IP address for long conversion : {$csvData[1]}");
		}
		$csvData[0] = $firstIpLong;
		$csvData[1] = $lastIpLong;
		writeCSV($of, $csvData);
	},
];

function writeCSV($of, $csvData) {
	fputcsv($of, $csvData);
}

function vEcho(string $s): void {
	if (!$GLOBALS["verbose"]) {
		return;
	}
	echo $s;
}

function findLargestNetwork(string $ipStartBin): int {
	for ($i = strlen($ipStartBin); $i--; $i >= 0) {
		$byte = ord($ipStartBin[$i]);
		for ($j = 7; $j >= 0; $j--) {
			if ($byte & (0xff >> $j)) {
				return ($i << 3) + $j + 1;
			}
		}
	}
	return 0;
}

function getLastAddress(string $ipStartBin, int $cidrBits): string {
	$ret = $ipStartBin;
	for ($i = strlen($ipStartBin); $i--; $i >= 0) {
		$firstBit = ($i << 3) + 1;
		$lastBit = ($i + 1) << 3;
		if ($cidrBits > $lastBit) {
			continue;
		} else if ($cidrBits < $firstBit) {
			$ret[$i] = "\xff";
		} else {
			$ret[$i] = chr(ord($ret[$i]) | (0xff >> ($cidrBits - $firstBit + 1)));
		}
	}
	return $ret;
}

function getNextAddress(string $ipStartBin): string {
	$ret = $ipStartBin;
	for ($i = strlen($ipStartBin); $i--; $i >= 0) {
		for ($j = 7; $j >= 0; $j--) {
			$byte = ord($ret[$i]);
			$mask = 1 << (7 - $j);
			if ($byte & $mask) {
				$ret[$i] = chr($byte & ~$mask);
			} else {
				$ret[$i] = chr($byte | $mask);
				return $ret;
			}
		}
	}
	throw new Exception("no next address for " . inet_ntop($ipStartBin));
}

function rangeToCIDR(string $ipStartBin, string $ipEndBin): array {
	if (strcmp($ipStartBin, $ipEndBin) > 0) {
		throw new Exception("wrong ip address order");
	}
	$cidrNets = [];
	$cidrBits = findLargestNetwork($ipStartBin);
	do {
		$lastAddrBin = getLastAddress($ipStartBin, $cidrBits);
		if (($cmp = strcmp($lastAddrBin, $ipEndBin)) <= 0) {
			$cidrNets[] = inet_ntop($ipStartBin) . "/" . $cidrBits;
			if ($cmp === 0) {
				return $cidrNets;
			}
			$ipStartBin = getNextAddress($lastAddrBin);
			$cidrBits = findLargestNetwork($ipStartBin);
		} else {
			$cidrBits++;
		}
	} while (true);
}

try {

	$exitCode = 0;
	$opts = getopt("i:o:f:qhw46");
	$verbose = !isset($opts["q"]);

	if (!$opts || isset($opts["h"]) || !isset($opts["i"]) || !isset($opts["o"]) || !isset($opts["f"]) || (isset($opts["4"]) && isset($opts["6"]))) {
		echo "usage: {$argv[0]} -i <inputFileName.csv> -o <outputFileName.csv> -f <outputFormat> [-4|-6] [-w] [-q]\n";
		echo " -i  input CSV file\n";
		echo " -o  output file name\n";
		echo " -f  output format (" . implode("|", array_keys($outputFormats)) . ")\n";
		echo " -4  output ipv4 networks only\n";
		echo " -6  output ipv6 networks only\n";
		echo " -w  overwrite output file if it already exists\n";
		echo " -q  be quiet\n";
		exit(1);
	}

	$inputFile = $opts["i"];
	if (!file_exists($inputFile)) {
		throw new Exception("cannot find input file: {$inputFile}");
	} else if (!is_readable($inputFile)) {
		throw new Exception("cannot read input file: {$inputFile}");
	}
	if (substr($inputFile, -3) === ".gz") {
		$inputFile = "compress.zlib://" . $inputFile;
	}
	if (!$if = fopen($inputFile, "r")) {
		throw new Exception("cannot open input file: {$inputFile}");
	}

	$outputFile = $opts["o"];
	if (file_exists($outputFile) && !isset($opts["w"])) {
		throw new Exception("output file {$outputFile} already exists, use -w to force overwrite");
	}
	if (substr($outputFile, -3) === ".gz") {
		$outputFile = "compress.zlib://" . $outputFile;
	}
	if (!$of = fopen($outputFile, "w")) {
		throw new Exception("cannot open output file: {$outPutFile}");
	}

	if (!isset($outputFormats[$opts["f"]])) {
		throw new Exception("invalid output format {$opts['f']}");
	}
	$outputFormatter = $outputFormats[$opts["f"]];

	$i = 0;
	while ($r = fgetcsv($if, 8192)) {
		$i++;
		[ $firstIp, $lastIp ] = $r;
		try {
			if (!$firstIpBin = inet_pton($firstIp)) {
				throw new Exception("invalid first IP '{$firstIp}' in CSV record");
			} else if (!$lastIpBin = inet_pton($lastIp)) {
				throw new Exception("invalid last IP '{$lastIp}' in CSV record");
			} else if (($addrLen = strlen($firstIpBin)) !== strlen($lastIpBin)) {
				throw new Exception("first and last IP address family mismatch ({$firstIp} / {$lastIp})");
			}
			if (isset($opts["4"]) && ($addrLen !== 4)) {
				continue;
			} else if (isset($opts["6"]) && ($addrLen !== 16)) {
				continue;
			}
			$outputFormatter($r, $of, $firstIpBin, $lastIpBin);
		} catch (Exception $e) {
			throw new Exception("line {$i}: {$e->getMessage()}");
		}
	}
	fclose($if);
	fclose($of);

	vEcho("Wrote {$outputFile}\n");

} catch (Exception $e) {
	if ($stdErr = @fopen("php://stderr", "w")) {
		fwrite($stdErr, "ERROR: {$e->getMessage()}\n");
		fclose($stdErr);
	} else {
		echo "ERROR: {$e->getMessage()}\n";
	}
	$exitCode = 1;
}
if ($exitCode) {
	exit($exitCode);
}