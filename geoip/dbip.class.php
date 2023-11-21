<?php

/**
 *
 * DB-IP.com database query and management class
 *
 * Copyright (C) 2022 db-ip.com
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

class DBIPException extends Exception {

}

class DBIP {

	const VERSION = 4;

	const TYPE_COUNTRY_LITE = 1;
	const TYPE_CITY_LITE = 2;
	const TYPE_COUNTRY_V4 = 3;
	const TYPE_LOCATION_V4 = 4;
	const TYPE_ISP_V4 = 5;
	const TYPE_FULL_V4 = 6;

	const TYPE_COUNTRY_V3 = 7;
	const TYPE_LOCATION_V3 = 8;
	const TYPE_ISP_V3 = 9;
	const TYPE_FULL_V3 = 10;

	const TYPE_LOCATION_V2 = 11;
	const TYPE_ISP_V2 = 12;
	const TYPE_FULL_V2 = 13;

	const TYPE_COUNTRY = self::TYPE_COUNTRY_V4;
	const TYPE_LOCATION = self::TYPE_LOCATION_V4;
	const TYPE_ISP = self::TYPE_ISP_V4;
	const TYPE_FULL = self::TYPE_FULL_V4;

	private $db;
	private $dbQuoteChar = "";

	public function __construct(PDO $db, $dbQuoteChar = "") {
		$this->db = $db;
		$this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$this->dbQuoteChar = $dbQuoteChar;
	}

	public function importFromCsv($fileName, $type, $tableName = "dbip_lookup", $progressCallback = null) {
		switch ($type) {
			case self::TYPE_COUNTRY_LITE:
			$fields = array("ip_start", "ip_end", "country");
			break;
			case self::TYPE_CITY_LITE:
			$fields = array("ip_start", "ip_end", "continent", "country", "stateprov", "city", "latitude", "longitude");
			break;
			case self::TYPE_COUNTRY_V4:
			case self::TYPE_COUNTRY_V3:
			$fields = array("ip_start", "ip_end", "continent", "country");
			break;
			case self::TYPE_LOCATION_V4:
			$fields = array("ip_start", "ip_end", "continent", "country", "stateprov_code", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name", "weather_code");
			break;
			case self::TYPE_ISP_V4:
			$fields = array("ip_start", "ip_end", "continent", "country", "isp_name", "as_number", "usage_type", "connection_type", "organization_name");
			break;
			case self::TYPE_FULL_V4:
			$fields = array("ip_start", "ip_end", "continent", "country", "stateprov_code", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name", "weather_code", "isp_name", "as_number", "usage_type", "connection_type", "organization_name");
			break;
			case self::TYPE_LOCATION_V3:
			$fields = array("ip_start", "ip_end", "continent", "country", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name", "weather_code");
			break;
			case self::TYPE_ISP_V3:
			$fields = array("ip_start", "ip_end", "continent", "country", "isp_name", "as_number", "connection_type", "organization_name");
			break;
			case self::TYPE_FULL_V3:
			$fields = array("ip_start", "ip_end", "continent", "country", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name", "weather_code", "isp_name", "as_number", "connection_type", "organization_name");
			break;
			case self::TYPE_LOCATION_V2:
			$fields = array("ip_start", "ip_end", "country", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name");
			break;
			case self::TYPE_ISP_V2:
			$fields = array("ip_start", "ip_end", "country", "isp_name", "connection_type", "organization_name");
			break;
			case self::TYPE_FULL_V2:
			$fields = array("ip_start", "ip_end", "country", "stateprov", "district", "city", "zipcode", "latitude", "longitude", "geoname_id", "timezone_offset", "timezone_name", "isp_name", "connection_type", "organization_name");
			break;
			default:
			throw new DBIPException("invalid database type");
		}
		if (!file_exists($fileName)) {
			throw new DBIPException("file {$fileName} does not exists");
		}
		$q = $this->prepareImport($tableName, $fields);
		if (preg_match('/\.gz(\..+)?$/', $fileName)) {
			$openName = "compress.zlib://" . $fileName;
		} else {
			$openName = $fileName;
		}
		$f = @fopen($openName, "r");
		if (!is_resource($f)) {
			throw new DBIPException("cannot open {$fileName} for reading");
		}
		$nrecs = 0;
		while ($r = fgetcsv($f, 1024, ",", '"', "\0")) {
			foreach ($r as $k => $v) {
				if (!isset($fields[$k])) {
					throw new DBIPException("invalid CSV record for {$r[0]}");
				}
				switch ($fields[$k]) {
					case "latitude":
					case "longitude":
					case "timezone_offset":
					$r[$k] = (float)$v;
					break;
					case "isp_name":
					case "organization_name":
					$r[$k] = mb_substr($v, 0, 128);
					break;
					case "city":
					case "district":
					case "stateprov":
					$r[$k] = mb_substr($v, 0, 80);
					break;
					case "zipcode":
					$r[$k] = mb_substr($v, 0, 20);
					break;
					case "timezone_name":
					$r[$k] = mb_substr($v, 0, 64);
					break;
					case "connection_type":
					case "stateprov_code":
					case "usage_type":
					case "geoname_id":
					case "as_number":
					if (!$r[$k]) $r[$k] = null;
					break;
					default:
				}
			}
			try {
				$r[] = self::addrType($r[0]);
				$r[0] = inet_pton($r[0]);
				$r[1] = inet_pton($r[1]);
				$this->importRow($q, $r);
			} catch (Exception $e) {
				var_dump($r);
				throw new Exception("cannot import record #{$nrecs}: {$e->getMessage()}");
			}
			if ((($nrecs % 100) === 0) && is_callable($progressCallback)) {
				call_user_func($progressCallback, $nrecs);
			}
			$nrecs++;
		}
		fclose($f);
		$this->finalizeImport();
		return $nrecs;
	}

	public function lookup($addr, $tableName = "dbip_lookup") {
		if ($ret = $this->doLookup($tableName, self::addrType($addr), inet_pton($addr))) {
			$ret->ip_start = inet_ntop($ret->ip_start);
			$ret->ip_end = inet_ntop($ret->ip_end);
			return $ret;
		} else {
			throw new DBIPException("address not found");
		}
	}

	protected function prepareImport($tableName, array $fields) {
		try {
			if ($this->db->query("select count(*) as cnt from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar}")->fetchObject()->cnt) {
				throw new DBIPException("table {$tableName} is not empty");
			}
			$this->db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
			$this->db->beginTransaction();
			$q = $this->db->prepare("insert into {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar} (" . implode(",", $fields) . ",addr_type) values (" . implode(",", array_fill(0, count($fields), "?")) . ",?)");
			return $q;
		} catch (PDOException $e) {
			throw new DBIPException("database error: {$e->getMessage()}");
		}
	}

	protected function finalizeImport() {
		$this->db->commit();
	}

	protected function importRow($res, $row) {
		return $res->execute($row);
	}

	protected function doLookup($tableName, $addrType, $addrStart) {
		$q = $this->db->prepare("select * from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar} where addr_type = ? and ip_start <= ? order by ip_start desc limit 1");
		$q->execute(array($addrType, $addrStart));
		return $q->fetchObject();
	}

	static private function addrType($addr) {
		if (ip2long($addr) !== false) {
			return "ipv4";
		} else if (preg_match('/^[0-9a-fA-F:]+$/', $addr) && @inet_pton($addr)) {
			return "ipv6";
		}
		throw new DBIPException("unknown address type for {$addr}");
	}

}

/**
 * DBIP MySQL class
 *
 * If you are using a MySQL database backend, please prefer the DBIP base class which uses the PDO mysql driver.
 * This is only meant to be used on PHP installations where PDO is disabled and the old mysql_* interface is available.
 */
class DBIPMySQL extends DBIP {

	private $db;

	public function __construct($db) {
		$this->db = $db;
	}

	protected function prepareImport($tableName, array $fields) {
		$q = mysql_query("select count(*) as cnt from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar}", $this->db);
		$r = mysql_fetch_object($q);
		mysql_free_result($q);
		if ($r->cnt) {
			throw new DBIPException("table {$tableName} is not empty");
		}
		return array($tableName, $fields);
	}

	protected function finalizeImport() {
	}

	protected function importRow($res, $row) {
		$vals = array();
		foreach ($row as $val) {
			$vals[] = "'" . mysql_real_escape_string($val) . "'";
		}
		if (!mysql_query("insert into {$this->dbQuoteChar}{$res[0]}{$this->dbQuoteChar} (" . implode(",", $res[1]) . ",addr_type) values (" . implode(",", $vals) . ")", $this->db)) {
			throw new DBIPException("database error: cannot insert row");
		}
		return true;
	}

	protected function doLookup($tableName, $addrType, $addrStart) {
		$q = mysql_query("select * from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar} where addr_type = '{$addrType}' and ip_start <= '" . mysql_real_escape_string($addrStart) . "' order by ip_start desc limit 1", $this->db);
		$r = mysql_fetch_object($q);
		mysql_free_result($q);
		return $r;
	}

}

/**
 * DBIP MySQLI class
 *
 * If you are using a MySQL database backend, please prefer the DBIP base class which uses the PDO mysql driver.
 * This is only meant to be used on PHP installations where PDO is disabled and the old mysqli_* interface is available.
 */
class DBIPMySQLI extends DBIP {

	private $db;

	public function __construct($db) {
		$this->db = $db;
	}

	protected function prepareImport($tableName, array $fields) {
		$q = mysqli_query($this->db, "select count(*) as cnt from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar}");
		$r = mysqli_fetch_object($q);
		mysqli_free_result($q);
		if ($r->cnt) {
			throw new DBIPException("table {$tableName} is not empty");
		}
		return array($tableName, $fields);
	}

	protected function finalizeImport() {
	}

	protected function importRow($res, $row) {
		$vals = array();
		foreach ($row as $val) {
			$vals[] = "'" . mysqli_real_escape_string($this->db, $val) . "'";
		}
		if (!mysqli_query($this->db, "insert into {$this->dbQuoteChar}{$res[0]}{$this->dbQuoteChar} (" . implode(",", $res[1]) . ",addr_type) values (" . implode(",", $vals) . ")")) {
			throw new DBIPException("database error: cannot insert row");
		}
		return true;
	}

	protected function doLookup($tableName, $addrType, $addrStart) {
		$q = mysqli_query($this->db, "select * from {$this->dbQuoteChar}{$tableName}{$this->dbQuoteChar} where addr_type = '{$addrType}' and ip_start <= '" . mysqli_real_escape_string($this->db, $addrStart) . "' order by ip_start desc limit 1");
		$r = mysqli_fetch_object($q);
		mysqli_free_result($q);
		return $r;
	}

}