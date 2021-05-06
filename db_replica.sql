CREATE DATABASE  IF NOT EXISTS `cloud_game_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `cloud_game_db`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: cloud_game_db
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_list`
--

DROP TABLE IF EXISTS `app_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `app_list` (
  `id` int DEFAULT NULL,
  `app_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `app_title` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `app_genre` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `app_brief` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `img_url` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `developer` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `publication_status` varchar(16) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  `platform` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`app_id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_list`
--

LOCK TABLES `app_list` WRITE;
/*!40000 ALTER TABLE `app_list` DISABLE KEYS */;
INSERT INTO `app_list` VALUES (3,'3','AR_Beethoven3D','Utilities','The most comfortable and immersive mixed reality experience available, with industry-leading solutions that deliver value in minutes','/static/apps_icon/default.png','Compal','Public','2021-02-12 03:38:41','2021-02-12 03:38:41','compal'),(1,'382110','Virtual Desktop','Utilities','Virtual Desktop is an application developed for the Oculus Rift / Rift S, HTC Vive, Valve Index and WMR headsets that lets you use your computer in VR. You can browse the web, watch movies, Netflix or even play games on a giant virtual screen.','/static/apps_icon/virtual_desktop.jpg','Guy Godin','Public','2021-01-12 03:38:41','2021-01-12 03:38:41','steam');
/*!40000 ALTER TABLE `app_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `available_apps_for_servers`
--

DROP TABLE IF EXISTS `available_apps_for_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `available_apps_for_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `server_ip` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `server_ip` (`server_ip`),
  CONSTRAINT `available_apps_for_servers_ibfk_1` FOREIGN KEY (`server_ip`) REFERENCES `game_servers` (`server_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=237 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_apps_for_servers`
--

LOCK TABLES `available_apps_for_servers` WRITE;
/*!40000 ALTER TABLE `available_apps_for_servers` DISABLE KEYS */;
INSERT INTO `available_apps_for_servers` VALUES (83,'348250','172.16.0.3'),(84,'382110','172.16.0.3'),(85,'410570','172.16.0.3'),(86,'438100','172.16.0.3'),(87,'444930','172.16.0.3'),(88,'450390','172.16.0.3'),(89,'468700','172.16.0.3'),(90,'519880','172.16.0.3'),(91,'719950','172.16.0.3'),(92,'826480','172.16.0.3'),(93,'3','172.16.0.3'),(94,'348250','172.16.0.3'),(95,'382110','172.16.0.3'),(96,'410570','172.16.0.3'),(97,'438100','172.16.0.3'),(98,'444930','172.16.0.3'),(99,'450390','172.16.0.3'),(100,'468700','172.16.0.3'),(101,'519880','172.16.0.3'),(102,'719950','172.16.0.3'),(103,'826480','172.16.0.3'),(104,'3','172.16.0.3'),(105,'348250','172.16.0.3'),(106,'382110','172.16.0.3'),(107,'410570','172.16.0.3'),(108,'438100','172.16.0.3'),(109,'444930','172.16.0.3'),(110,'450390','172.16.0.3'),(111,'468700','172.16.0.3'),(112,'519880','172.16.0.3'),(113,'719950','172.16.0.3'),(114,'826480','172.16.0.3'),(115,'3','172.16.0.3'),(116,'348250','172.16.0.3'),(117,'382110','172.16.0.3'),(118,'410570','172.16.0.3'),(119,'438100','172.16.0.3'),(120,'444930','172.16.0.3'),(121,'450390','172.16.0.3'),(122,'468700','172.16.0.3'),(123,'519880','172.16.0.3'),(124,'719950','172.16.0.3'),(125,'826480','172.16.0.3'),(126,'3','172.16.0.3'),(127,'348250','172.16.0.3'),(128,'382110','172.16.0.3'),(129,'410570','172.16.0.3'),(130,'438100','172.16.0.3'),(131,'444930','172.16.0.3'),(132,'450390','172.16.0.3'),(133,'468700','172.16.0.3'),(134,'519880','172.16.0.3'),(135,'719950','172.16.0.3'),(136,'826480','172.16.0.3'),(137,'3','172.16.0.3'),(138,'348250','172.16.0.3'),(139,'382110','172.16.0.3'),(140,'410570','172.16.0.3'),(141,'438100','172.16.0.3'),(142,'444930','172.16.0.3'),(143,'450390','172.16.0.3'),(144,'468700','172.16.0.3'),(145,'519880','172.16.0.3'),(146,'719950','172.16.0.3'),(147,'826480','172.16.0.3'),(148,'3','172.16.0.3'),(149,'348250','172.16.0.3'),(150,'382110','172.16.0.3'),(151,'410570','172.16.0.3'),(152,'438100','172.16.0.3'),(153,'444930','172.16.0.3'),(154,'450390','172.16.0.3'),(155,'468700','172.16.0.3'),(156,'519880','172.16.0.3'),(157,'719950','172.16.0.3'),(158,'826480','172.16.0.3'),(159,'3','172.16.0.3'),(160,'348250','172.16.0.3'),(161,'382110','172.16.0.3'),(162,'410570','172.16.0.3'),(163,'438100','172.16.0.3'),(164,'444930','172.16.0.3'),(165,'450390','172.16.0.3'),(166,'468700','172.16.0.3'),(167,'519880','172.16.0.3'),(168,'719950','172.16.0.3'),(169,'826480','172.16.0.3'),(170,'3','172.16.0.3'),(171,'348250','172.16.0.3'),(172,'382110','172.16.0.3'),(173,'410570','172.16.0.3'),(174,'438100','172.16.0.3'),(175,'444930','172.16.0.3'),(176,'450390','172.16.0.3'),(177,'468700','172.16.0.3'),(178,'519880','172.16.0.3'),(179,'719950','172.16.0.3'),(180,'826480','172.16.0.3'),(181,'3','172.16.0.3'),(182,'348250','172.16.0.3'),(183,'382110','172.16.0.3'),(184,'410570','172.16.0.3'),(185,'438100','172.16.0.3'),(186,'444930','172.16.0.3'),(187,'450390','172.16.0.3'),(188,'468700','172.16.0.3'),(189,'519880','172.16.0.3'),(190,'719950','172.16.0.3'),(191,'826480','172.16.0.3'),(192,'3','172.16.0.3'),(193,'348250','172.16.0.3'),(194,'382110','172.16.0.3'),(195,'410570','172.16.0.3'),(196,'438100','172.16.0.3'),(197,'444930','172.16.0.3'),(198,'450390','172.16.0.3'),(199,'468700','172.16.0.3'),(200,'519880','172.16.0.3'),(201,'719950','172.16.0.3'),(202,'826480','172.16.0.3'),(203,'3','172.16.0.3'),(204,'348250','172.16.0.3'),(205,'382110','172.16.0.3'),(206,'410570','172.16.0.3'),(207,'438100','172.16.0.3'),(208,'444930','172.16.0.3'),(209,'450390','172.16.0.3'),(210,'468700','172.16.0.3'),(211,'519880','172.16.0.3'),(212,'719950','172.16.0.3'),(213,'826480','172.16.0.3'),(214,'3','172.16.0.3'),(215,'348250','172.16.0.3'),(216,'382110','172.16.0.3'),(217,'410570','172.16.0.3'),(218,'438100','172.16.0.3'),(219,'444930','172.16.0.3'),(220,'450390','172.16.0.3'),(221,'468700','172.16.0.3'),(222,'519880','172.16.0.3'),(223,'719950','172.16.0.3'),(224,'826480','172.16.0.3'),(225,'3','172.16.0.3'),(226,'348250','172.16.0.3'),(227,'382110','172.16.0.3'),(228,'410570','172.16.0.3'),(229,'438100','172.16.0.3'),(230,'444930','172.16.0.3'),(231,'450390','172.16.0.3'),(232,'468700','172.16.0.3'),(233,'519880','172.16.0.3'),(234,'719950','172.16.0.3'),(235,'826480','172.16.0.3'),(236,'3','172.16.0.3');
/*!40000 ALTER TABLE `available_apps_for_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `available_games_for_servers`
--

DROP TABLE IF EXISTS `available_games_for_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `available_games_for_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `game_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `server_ip` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `server_ip` (`server_ip`),
  CONSTRAINT `available_games_for_servers_ibfk_1` FOREIGN KEY (`server_ip`) REFERENCES `game_servers` (`server_ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_games_for_servers`
--

LOCK TABLES `available_games_for_servers` WRITE;
/*!40000 ALTER TABLE `available_games_for_servers` DISABLE KEYS */;
/*!40000 ALTER TABLE `available_games_for_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client_connection_list`
--

DROP TABLE IF EXISTS `client_connection_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client_connection_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `client_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `server_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `app_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `platform` varchar(15) COLLATE utf8mb4_general_ci NOT NULL,
  `connection_status` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `launch_time` datetime NOT NULL,
  `close_time` datetime DEFAULT NULL,
  `total_play_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_connection_list`
--

LOCK TABLES `client_connection_list` WRITE;
/*!40000 ALTER TABLE `client_connection_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `client_connection_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dataflow`
--

DROP TABLE IF EXISTS `dataflow`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dataflow` (
  `id` int NOT NULL AUTO_INCREMENT,
  `source_url` varchar(512) COLLATE utf8mb4_general_ci NOT NULL,
  `protocol` int NOT NULL,
  `app_name` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `dataflow_id` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dataflow_id_UNIQUE` (`dataflow_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dataflow`
--

LOCK TABLES `dataflow` WRITE;
/*!40000 ALTER TABLE `dataflow` DISABLE KEYS */;
/*!40000 ALTER TABLE `dataflow` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device`
--

DROP TABLE IF EXISTS `device`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `device` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_name` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device`
--

LOCK TABLES `device` WRITE;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
/*!40000 ALTER TABLE `device` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_list`
--

DROP TABLE IF EXISTS `game_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_list` (
  `id` int DEFAULT NULL,
  `game_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `game_title` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `game_genre` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `game_brief` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `img_url` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `developer` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `publication_status` varchar(16) COLLATE utf8mb4_general_ci NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  `platform` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `game_listcol` varchar(45) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_list`
--

LOCK TABLES `game_list` WRITE;
/*!40000 ALTER TABLE `game_list` DISABLE KEYS */;
INSERT INTO `game_list` VALUES (1,'410570','Gunjack','First-person Shooter','Jump into your weapons turret and annihilate endless waves of enemies.','/static/games_icon/gunjack.jpg','Jack Rabbit','Public','2021-01-12 03:38:41','2021-01-18 10:05:01','steam',NULL),(3,'468700','NVIDIA VR Funhouse','First-person Shooter','Step right up to VR Funhouse and enter a virtual carnival full of fun and games. Be an archer with flaming arrows. Test your skill shooting skeet targets blasted from a cannon. See how many moles you can punch, whack, and much more.','/static/games_icon/nvidia_funhouse.jpg','NVIDIA','Private','2021-02-03 06:33:12','2021-02-03 06:39:22','steam',NULL),(2,'519880','Redout','Speed Racing','An uncompromising, fast, tough and satisfying car racing game!','/static/games_icon/redout.jpg','Car Richard','Public','2021-01-13 08:44:13','2021-01-29 06:07:58','steam',NULL);
/*!40000 ALTER TABLE `game_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_servers`
--

DROP TABLE IF EXISTS `game_servers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `server_ip` varchar(80) COLLATE utf8mb4_general_ci NOT NULL,
  `client_ip` varchar(80) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `last_connection_at` datetime DEFAULT NULL,
  `is_available` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `server_ip` (`server_ip`),
  UNIQUE KEY `client_ip` (`client_ip`),
  CONSTRAINT `game_servers_chk_1` CHECK ((`is_available` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_servers`
--

LOCK TABLES `game_servers` WRITE;
/*!40000 ALTER TABLE `game_servers` DISABLE KEYS */;
INSERT INTO `game_servers` VALUES (9,'172.16.0.25',NULL,'2021-01-15 03:01:35','2021-01-15 03:02:47',0),(12,'172.16.0.219',NULL,'2021-01-20 07:15:17','2021-02-03 04:09:52',0),(15,'192.168.10.116',NULL,'2021-01-22 02:33:07','2021-01-22 02:33:07',0),(24,'192.168.10.103',NULL,'2021-02-24 06:54:14','2021-02-24 06:54:14',0),(25,'127.0.0.1',NULL,'2021-03-16 03:27:01','2021-03-16 03:27:01',0),(26,'172.16.0.3',NULL,'2021-03-17 08:33:10','2021-04-08 09:05:40',0);
/*!40000 ALTER TABLE `game_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myfavoriteapp`
--

DROP TABLE IF EXISTS `myfavoriteapp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myfavoriteapp` (
  `user_id` int DEFAULT NULL,
  `app_id` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `app_id` (`app_id`),
  CONSTRAINT `myfavoriteapp_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `myfavoriteapp_ibfk_2` FOREIGN KEY (`app_id`) REFERENCES `app_list` (`app_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myfavoriteapp`
--

LOCK TABLES `myfavoriteapp` WRITE;
/*!40000 ALTER TABLE `myfavoriteapp` DISABLE KEYS */;
/*!40000 ALTER TABLE `myfavoriteapp` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myfavoritegame`
--

DROP TABLE IF EXISTS `myfavoritegame`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myfavoritegame` (
  `user_id` int DEFAULT NULL,
  `game_id` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `myfavoritegame_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `myfavoritegame_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `game_list` (`game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myfavoritegame`
--

LOCK TABLES `myfavoritegame` WRITE;
/*!40000 ALTER TABLE `myfavoritegame` DISABLE KEYS */;
/*!40000 ALTER TABLE `myfavoritegame` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (2,'Administrator'),(3,'Developer'),(1,'Player');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stream_clone`
--

DROP TABLE IF EXISTS `stream_clone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stream_clone` (
  `id` int NOT NULL DEFAULT '0',
  `server_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `client_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `client_username` varchar(62) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stream_title` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `num_of_audience` int DEFAULT NULL,
  `img_url` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stream_url` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `started_from` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stream_clone`
--

LOCK TABLES `stream_clone` WRITE;
/*!40000 ALTER TABLE `stream_clone` DISABLE KEYS */;
INSERT INTO `stream_clone` VALUES (4,'172.16.0.25','172.16.0.219','Jolin','Jolin is now playing LOL!',0,'https://steamuserimages-a.akamaihd.net/ugc/947347712784059553/6956821877AA474C9DA60B09E286287723560CB4/','https://www.twitch.tv/atize/video/77973733','2021-01-05 10:34:08'),(5,'172.16.0.32','172.16.0.122','Ambition','Ambition is killing spree',0,'https://steamuserimages-a.akamaihd.net/ugc/1025077468220642201/9EC4FD6477FCEE4AD8F68F12B70248D9E19E0E5C/','https://www.twitch.tv/videos/861935213','2021-01-05 10:35:02');
/*!40000 ALTER TABLE `stream_clone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stream_list`
--

DROP TABLE IF EXISTS `stream_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stream_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `server_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `client_ip` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `client_username` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stream_title` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `num_of_audience` int DEFAULT NULL,
  `img_url` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stream_url` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `started_from` datetime NOT NULL,
  `video_source_url` varchar(512) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `server_ip` (`server_ip`),
  UNIQUE KEY `client_ip` (`client_ip`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stream_list`
--

LOCK TABLES `stream_list` WRITE;
/*!40000 ALTER TABLE `stream_list` DISABLE KEYS */;
INSERT INTO `stream_list` VALUES (4,'1.1.1.1','172.16.0.219','Toy','Redout',0,'/static/redout_demo.png','https://www.youtube.com/embed/Ume5gZEE8jI?autoplay=1&mute=1&controls=0&amp;start=120','2021-01-05 10:34:08','https://bitdash-a.akamaihd.net/content/MI201109210084_1/m3u8s/f08e80da-bf1d-4e3d-8899-f0f6155f6efa.m3u8'),(5,'2.2.2.2','172.16.0.122','Ambition','Gunjack',0,'/static/streaming_demo.png','https://www.youtube.com/embed/8ci_uyV-hyI?autoplay=1&mute=1&controls=0&amp;start=6','2021-01-05 10:35:02','https://bitdash-a.akamaihd.net/content/sintel/hls/playlist.m3u8');
/*!40000 ALTER TABLE `stream_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  `delete_flag` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `user_chk_1` CHECK ((`delete_flag` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Anderson','$2b$12$9/n7v6FaF7G5RX9DE1hpm.AngfwWNhzFXKJTLCEpg6oMcsXL7KebO',0,'2021-01-26 09:15:14'),(3,'Jack Rabbit','$2b$12$67qNqxr0a6VqcGH3uk9j0ueKotim1YiX8IZHMrIGvuHACBrNbgEoK',0,'2021-02-19 01:56:47'),(8,'Compal admin','$2b$12$ehHH0Vm6k8Q6okH1Bx2qZOQpqf2C4orJ.5JG1BCx6xtkqPLS7Ik1u',0,'2021-03-10 05:48:54');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,1,3),(3,3,1),(4,8,2);
/*!40000 ALTER TABLE `user_roles` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-06 17:07:52
