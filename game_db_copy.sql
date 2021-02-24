-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: cloud_game_db
-- ------------------------------------------------------
-- Server version	8.0.22

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
) ENGINE=InnoDB AUTO_INCREMENT=1926 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
  `game_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `connection_status` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `launch_time` datetime NOT NULL,
  `close_time` datetime DEFAULT NULL,
  `total_play_time` bigint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client_connection_list`
--

LOCK TABLES `client_connection_list` WRITE;
/*!40000 ALTER TABLE `client_connection_list` DISABLE KEYS */;
INSERT INTO `client_connection_list` VALUES (1,NULL,'127.0.0.1','172.16.0.219','747350','closed','2021-01-12 03:38:41','2021-01-12 03:42:12',1065),(2,NULL,'127.0.0.1','172.16.0.219','519880','closed','2021-01-13 08:44:13','2021-01-13 08:44:59',877),(35,NULL,'172.16.0.213','172.16.0.3','410570','closed','2021-01-18 10:03:28','2021-01-18 10:05:01',93),(46,NULL,'192.168.10.117','192.168.10.116','519880','closed','2021-01-20 09:19:18','2021-01-20 09:21:16',118),(54,NULL,'192.168.0.105','192.168.0.100','519880','closed','2021-01-29 06:06:52','2021-01-29 06:07:58',66),(59,NULL,'172.16.0.4','172.16.0.3','410570','closed','2021-02-03 06:33:12','2021-02-03 06:39:22',911);
/*!40000 ALTER TABLE `client_connection_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game_list`
--

DROP TABLE IF EXISTS `game_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game_list` (
  `id` int NOT NULL AUTO_INCREMENT,
  `game_id` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `game_title` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `game_type` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `game_brief` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `img_url` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`game_id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_list`
--

LOCK TABLES `game_list` WRITE;
/*!40000 ALTER TABLE `game_list` DISABLE KEYS */;
INSERT INTO `game_list` VALUES (1,'410570','Gunjack','First-person shooter','Jump into your weapons turret and annihilate endless waves of enemies.','/static/games_icon/gunjack.jpg'),(3,'468700','NVIDIA VR Funhouse','First-person shooter','Step right up to VR Funhouse and enter a virtual carnival full of fun and games. Be an archer with flaming arrows. Test your skill shooting skeet targets blasted from a cannon. See how many moles you can punch, whack, and much more.','/static/games_icon/nvidia_funhouse.jpg'),(2,'519880','Redout','Speed Racing','An uncompromising, fast, tough and satisfying car racing game!','/static/games_icon/redout.jpg');
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game_servers`
--

LOCK TABLES `game_servers` WRITE;
/*!40000 ALTER TABLE `game_servers` DISABLE KEYS */;
INSERT INTO `game_servers` VALUES (9,'172.16.0.25',NULL,'2021-01-15 03:01:35','2021-01-15 03:02:47',0),(12,'172.16.0.219',NULL,'2021-01-20 07:15:17','2021-02-03 04:09:52',0),(15,'192.168.10.116',NULL,'2021-01-22 02:33:07','2021-01-22 02:33:07',0);
/*!40000 ALTER TABLE `game_servers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `myfavorite`
--

DROP TABLE IF EXISTS `myfavorite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `myfavorite` (
  `user_id` int DEFAULT NULL,
  `game_id` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  KEY `user_id` (`user_id`),
  KEY `game_id` (`game_id`),
  CONSTRAINT `myfavorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `myfavorite_ibfk_2` FOREIGN KEY (`game_id`) REFERENCES `game_list` (`game_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `myfavorite`
--

LOCK TABLES `myfavorite` WRITE;
/*!40000 ALTER TABLE `myfavorite` DISABLE KEYS */;
/*!40000 ALTER TABLE `myfavorite` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (2,'admin'),(1,'normal');
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
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stream_list`
--

LOCK TABLES `stream_list` WRITE;
/*!40000 ALTER TABLE `stream_list` DISABLE KEYS */;
INSERT INTO `stream_list` VALUES (4,'1.1.1.1','172.16.0.219','Jolin','Jolin is now playing LOL!',0,'/static/streams_icon/live_user_chiao622.jpg','https://www.twitch.tv/atize/video/77973733','2021-01-05 10:34:08','http://demo.unified-streaming.com/video/tears-of-steel/tears-of-steel.ism/.m3u8'),(5,'2.2.2.2','172.16.0.122','Ambition','Ambition is killing spree',0,'/static/streams_icon/live_user_lol_ambition.jpg','https://www.twitch.tv/videos/861935213','2021-01-05 10:35:02','https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'test','$2b$12$9/n7v6FaF7G5RX9DE1hpm.AngfwWNhzFXKJTLCEpg6oMcsXL7KebO',0,'2021-01-26 09:15:14'),(2,'admin','$2b$12$X7ZQApDDlzzw/yCZCt3Ng.WveClaMc3JvVN..ogrMd0tHSrYmTDbW',0,'2021-01-26 09:18:14'),(3,'jared','$2b$12$67qNqxr0a6VqcGH3uk9j0ueKotim1YiX8IZHMrIGvuHACBrNbgEoK',0,'2021-02-19 01:56:47');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_roles`
--

LOCK TABLES `user_roles` WRITE;
/*!40000 ALTER TABLE `user_roles` DISABLE KEYS */;
INSERT INTO `user_roles` VALUES (1,1,1),(2,2,2),(3,3,1);
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

-- Dump completed on 2021-02-24 14:28:56
