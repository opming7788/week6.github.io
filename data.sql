-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.0.32

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
-- Table structure for table `membercontent`
--

DROP TABLE IF EXISTS `membercontent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membercontent` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique ID',
  `member_id` bigint NOT NULL COMMENT 'Member ID for Message Sender',
  `content` varchar(255) DEFAULT NULL COMMENT 'content',
  `time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Publish Time',
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `membercontent_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `memberdata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membercontent`
--

LOCK TABLES `membercontent` WRITE;
/*!40000 ALTER TABLE `membercontent` DISABLE KEYS */;
INSERT INTO `membercontent` VALUES (2,1,'Hello World','2024-05-06 18:53:42'),(5,2,'XX老師','2024-05-06 18:54:45'),(7,1,'今天天氣真他媽好','2024-05-06 19:52:47'),(9,3,'乾0老師','2024-05-06 19:53:44'),(10,5,'我說在座的各位都是垃圾','2024-05-06 20:03:33'),(11,2,'今天天氣真好','2024-05-06 20:05:26'),(12,2,'吃早餐沒?','2024-05-06 20:24:22'),(13,1,'吃早餐去','2024-05-06 20:45:36'),(15,1,'吃晚餐囉','2024-05-06 23:23:31'),(17,1,'123到台灣，台灣有個阿里山','2024-05-07 01:29:53'),(18,2,'哈哈哈哈哈哈哈哈哈哈哈哈','2024-05-07 01:30:11'),(19,2,'十萬青年十萬肝','2024-05-07 01:31:12'),(20,4,'GG輪班救台灣','2024-05-07 01:32:14'),(21,4,'喔喔喔喔喔喔','2024-05-07 01:32:47'),(22,6,'台灣獨立','2024-05-07 01:34:37'),(25,3,'天下武功，唯快不破 ','2024-05-07 01:38:25'),(26,3,' ','2024-05-07 01:40:04'),(29,1,'嘻嘻嘻嘻嘻','2024-05-07 02:00:50'),(30,1,'握草','2024-05-07 02:01:15'),(31,5,'好的老師帶你上天堂，不好的老師帶你住套房','2024-05-07 02:02:13'),(32,5,' ','2024-05-07 02:02:46'),(33,2,'12345678','2024-05-07 02:08:45');
/*!40000 ALTER TABLE `membercontent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memberdata`
--

DROP TABLE IF EXISTS `memberdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memberdata` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'Unique ID',
  `yourname` varchar(255) NOT NULL COMMENT 'yourname',
  `username` varchar(255) NOT NULL COMMENT 'Username',
  `password` varchar(255) NOT NULL COMMENT 'Password',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memberdata`
--

LOCK TABLES `memberdata` WRITE;
/*!40000 ALTER TABLE `memberdata` DISABLE KEYS */;
INSERT INTO `memberdata` VALUES (1,'小明','opming','12345'),(2,'澎澎','ply','aaa'),(3,'陳明','ss','aaa'),(4,'丁滿','ding','a123'),(5,'精靈','spirit','12345'),(6,'蔡英文','guessEnglish','aaa');
/*!40000 ALTER TABLE `memberdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-07  2:19:05
