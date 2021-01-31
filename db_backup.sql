-- --------------------------------------------------------
-- Host:                         cicada.zayo.us
-- Server version:               5.7.18-log - MySQL Community Server (GPL)
-- Server OS:                    Linux
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table test.tbl_back_bone
CREATE TABLE IF NOT EXISTS `tbl_back_bone` (
  `nw_code` int(11) NOT NULL,
  `nw_name` varchar(50) NOT NULL,
  `from_cli` varchar(10) NOT NULL,
  `to_cli` varchar(500) NOT NULL,
  `cli_count` int(11) DEFAULT NULL,
  PRIMARY KEY (`nw_code`,`from_cli`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table test.tbl_back_bone: ~0 rows (approximately)
/*!40000 ALTER TABLE `tbl_back_bone` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_back_bone` ENABLE KEYS */;

-- Dumping structure for table test.tbl_back_bone_log
CREATE TABLE IF NOT EXISTS `tbl_back_bone_log` (
  `circuit_design_id` int(15) NOT NULL,
  `exchange_carrier_circuit_id` varchar(50) NOT NULL DEFAULT '',
  `nw_code` int(11) NOT NULL,
  `from_cli` varchar(15) NOT NULL,
  `to_cli` varchar(15) NOT NULL,
  `status` varchar(15) NOT NULL,
  PRIMARY KEY (`circuit_design_id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 ROW_FORMAT=DYNAMIC;

-- Dumping data for table test.tbl_back_bone_log: ~0 rows (approximately)
/*!40000 ALTER TABLE `tbl_back_bone_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_back_bone_log` ENABLE KEYS */;

-- Dumping structure for table test.tbl_cli_cordinates
CREATE TABLE IF NOT EXISTS `tbl_cli_cordinates` (
  `cli` varchar(50) NOT NULL,
  `longitude` float DEFAULT NULL,
  `lattitude` float DEFAULT NULL,
  PRIMARY KEY (`cli`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table test.tbl_cli_cordinates: ~0 rows (approximately)
/*!40000 ALTER TABLE `tbl_cli_cordinates` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_cli_cordinates` ENABLE KEYS */;

-- Dumping structure for table test.tbl_config
CREATE TABLE IF NOT EXISTS `tbl_config` (
  `network` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `query` varchar(2000) NOT NULL,
  `genarate` char(1) NOT NULL DEFAULT 'N',
  `color` varchar(45) NOT NULL,
  `code` varchar(50) NOT NULL,
  PRIMARY KEY (`network`),
  UNIQUE KEY `network_UNIQUE` (`network`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table test.tbl_config: ~2 rows (approximately)
/*!40000 ALTER TABLE `tbl_config` DISABLE KEYS */;
INSERT INTO `tbl_config` (`network`, `name`, `query`, `genarate`, `color`, `code`) VALUES
	(6461, 'Zayo', 'SELECT exchange_carrier_circuit_id,circuit_design_id  FROM correlation_data.m6_circuit c WHERE exchange_carrier_circuit_id Like \'701%/1%G%\'  LIMIT 100', 'Y', 'm_ylw-pushpin0', 'AS6461'),
	(7385, 'rajesh', 'SELECT  exchange_carrier_circuit_id,circuit_design_id  FROM correlation_data.m6_circuit c WHERE exchange_carrier_circuit_id Like \'702%/1%G%\'  LIMIT 100', 'Y', 'm_ylw-pushpin3', 'AS6461');
/*!40000 ALTER TABLE `tbl_config` ENABLE KEYS */;

-- Dumping structure for table test.tbl_pop_data
CREATE TABLE IF NOT EXISTS `tbl_pop_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cli_code` varchar(50) NOT NULL,
  `site` varchar(50) NOT NULL,
  `street` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `equipment` varchar(250) NOT NULL,
  `comment` varchar(250) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `cli_code` (`cli_code`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table test.tbl_pop_data: ~0 rows (approximately)
/*!40000 ALTER TABLE `tbl_pop_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_pop_data` ENABLE KEYS */;

-- Dumping structure for table test.tbl_rawData_Monthly
CREATE TABLE IF NOT EXISTS `tbl_rawData_Monthly` (
  `CircuitPerf_ID` int(10) NOT NULL AUTO_INCREMENT,
  `CustomerID` int(11) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `MaintenanceStart` time DEFAULT NULL,
  `MaintenanceEnd` time DEFAULT NULL,
  `CellSiteFACode` varchar(45) DEFAULT NULL,
  `DeviceName` varchar(45) DEFAULT NULL,
  `CircuitID` varchar(45) DEFAULT NULL,
  `interfaceName` varchar(45) DEFAULT NULL,
  `DDR_AVG` float DEFAULT NULL,
  `DDR_Min` float DEFAULT NULL,
  `DDR_MAX` float DEFAULT NULL,
  `DDDR_StdDev` float DEFAULT NULL,
  `RTD_Avg` float DEFAULT NULL,
  `RTD_Min` float DEFAULT NULL,
  `RTD_Max` float DEFAULT NULL,
  `RTD_StdDev` float DEFAULT NULL,
  `FJ_Avg` float DEFAULT NULL,
  `FJ_Min` float DEFAULT NULL,
  `FJ_Max` float DEFAULT NULL,
  `FJ_StdDev` float DEFAULT NULL,
  `MTTR_PerLata_h` float DEFAULT NULL,
  `TTR_h` float DEFAULT NULL,
  `CircuitAvail` float DEFAULT NULL,
  `EVC_Avail` float DEFAULT NULL,
  `EVC_Avail_sec` float DEFAULT NULL,
  `SiteAvail` float DEFAULT NULL,
  `SiteAvail_sec` float DEFAULT NULL,
  PRIMARY KEY (`CircuitPerf_ID`),
  UNIQUE KEY `CircuitPerf_ID_UNIQUE` (`CircuitPerf_ID`),
  UNIQUE KEY `Record_unq` (`StartDate`,`EndDate`,`interfaceName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table test.tbl_rawData_Monthly: ~964 rows (approximately)
/*!40000 ALTER TABLE `tbl_rawData_Monthly` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_rawData_Monthly` ENABLE KEYS */;

-- Dumping structure for procedure test.test_multi_sets
DELIMITER //
//
DELIMITER ;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
