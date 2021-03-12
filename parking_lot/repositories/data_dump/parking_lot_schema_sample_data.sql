-- MySQL dump 10.13  Distrib 8.0.23, for osx10.15 (x86_64)
--
-- Host: localhost    Database: parking_lot
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `merchant`
--

DROP TABLE IF EXISTS `merchant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `registered_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant`
--

LOCK TABLES `merchant` WRITE;
/*!40000 ALTER TABLE `merchant` DISABLE KEYS */;
INSERT INTO `merchant` VALUES (1,'Merchant 1','2020-01-01 00:00:00'),(2,'Merchant 2','2021-01-01 00:00:00');
/*!40000 ALTER TABLE `merchant` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking_lot`
--

DROP TABLE IF EXISTS `parking_lot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parking_lot` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `area` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pin_code` int DEFAULT NULL,
  `is_available` enum('0','1') COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `slot_count` int DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking_lot`
--

LOCK TABLES `parking_lot` WRITE;
/*!40000 ALTER TABLE `parking_lot` DISABLE KEYS */;
INSERT INTO `parking_lot` VALUES (1,'Forum','Koramangala',560095,'1','2000-01-01 00:00:00',100),(2,'Christ','Koramangala',560095,'1','1980-01-01 00:00:00',1000),(3,'Test','Marathalli',560037,'1','2021-01-01 00:00:00',6),(4,'Valet 1','Whitefield',560048,'1','2020-01-01 00:00:00',50),(5,'Motherhood','Sarjapur',560104,'1','2005-01-01 00:00:00',30),(6,'UB City','VM Road',560001,'1','2015-01-01 00:00:00',1000);
/*!40000 ALTER TABLE `parking_lot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking_slot`
--

DROP TABLE IF EXISTS `parking_slot`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parking_slot` (
  `id` int NOT NULL AUTO_INCREMENT,
  `merchant_id` int DEFAULT NULL,
  `parking_lot_id` int DEFAULT NULL,
  `vehicle_id` int DEFAULT NULL,
  `available` enum('0','1') COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_merchant` (`merchant_id`),
  KEY `fk_parking_lot` (`parking_lot_id`),
  KEY `fk_vehicle` (`vehicle_id`),
  CONSTRAINT `parking_slot_ibfk_1` FOREIGN KEY (`merchant_id`) REFERENCES `merchant` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `parking_slot_ibfk_3` FOREIGN KEY (`parking_lot_id`) REFERENCES `parking_lot` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `parking_slot_ibfk_4` FOREIGN KEY (`vehicle_id`) REFERENCES `vehicle` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking_slot`
--

LOCK TABLES `parking_slot` WRITE;
/*!40000 ALTER TABLE `parking_slot` DISABLE KEYS */;
INSERT INTO `parking_slot` VALUES (1,1,3,9,'0'),(2,1,3,10,'0'),(3,1,3,11,'0'),(4,1,3,12,'0'),(5,1,3,13,'0'),(6,1,3,14,'0'),(7,1,3,15,'0'),(8,1,3,16,'0');
/*!40000 ALTER TABLE `parking_slot` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vehicle`
--

DROP TABLE IF EXISTS `vehicle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vehicle` (
  `id` int NOT NULL AUTO_INCREMENT,
  `color` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `in_at` datetime DEFAULT NULL,
  `out_at` datetime DEFAULT NULL,
  `registration_no` varchar(13) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vehicle`
--

LOCK TABLES `vehicle` WRITE;
/*!40000 ALTER TABLE `vehicle` DISABLE KEYS */;
INSERT INTO `vehicle` VALUES (1,'White','2021-03-12 08:57:13',NULL,'KA-01-HH-1234'),(2,'White','2021-03-12 08:59:39',NULL,'KA-01-HH-1234'),(3,'White','2021-03-12 09:01:38',NULL,'KA-01-HH-1234'),(4,'White','2021-03-12 09:02:36',NULL,'KA-01-HH-1234'),(5,'golden','2021-03-12 09:03:10',NULL,'ka-51-mn-1892'),(6,'White','2021-03-12 09:20:05',NULL,'KA-01-HH-1234'),(7,'White','2021-03-12 09:44:58',NULL,'KA-01-HH-1234'),(8,'White','2021-03-12 09:45:30',NULL,'KA-01-HH-1234'),(9,'White','2021-03-12 09:46:51',NULL,'KA-01-HH-1234'),(10,'White','2021-03-12 09:47:14',NULL,'KA-01-HH-1234'),(11,'White','2021-03-12 09:47:15',NULL,'KA-01-HH-9999'),(12,'Black','2021-03-12 09:47:15',NULL,'KA-01-BB-0001'),(13,'Red','2021-03-12 09:47:15',NULL,'KA-01-HH-7777'),(14,'Blue','2021-03-12 09:47:15',NULL,'KA-01-HH-2701'),(15,'Black','2021-03-12 09:47:15',NULL,'KA-01-HH-3141'),(16,'White','2021-03-12 09:47:15',NULL,'KA-01-P-333');
/*!40000 ALTER TABLE `vehicle` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-03-12  9:51:33
