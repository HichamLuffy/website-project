-- MySQL dump 10.13  Distrib 8.0.36, for Linux (x86_64)
--
-- Host: localhost    Database: AQZ
-- ------------------------------------------------------
-- Server version	8.0.36-0ubuntu0.22.04.1

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
-- Table structure for table `option`
--

DROP TABLE IF EXISTS `option`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `option` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text` text NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `question_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  CONSTRAINT `option_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `option`
--

LOCK TABLES `option` WRITE;
/*!40000 ALTER TABLE `option` DISABLE KEYS */;
INSERT INTO `option` VALUES (1,'Naruto Uzumaki',1,1),(2,'Sasuke Uchiha',0,1),(3,'Kakashi Hatake',0,1),(4,'Itachi Uchiha',0,1),(5,'Naruto',0,2),(6,'One Piece',0,2),(7,'Bleach',0,2),(8,'Fairy Tail',1,2),(9,'Eren Yeager',1,3),(10,'Levi Ackerman',0,3),(11,'Mikasa Ackerman',0,3),(12,'Armin Arlert',0,3),(13,'Deku',1,4),(14,'Bakugo',0,4),(15,'Todoroki',0,4),(16,'All Might',0,4),(17,'Gomu Gomu no Mi',0,5),(18,'Yami Yami no Mi',1,5),(19,'Mera Mera no Mi',0,5),(20,'Hie Hie no Mi',0,5),(21,'Hana Hana no Mi',0,6),(22,'Bara Bara no Mi',1,6),(23,'Gura Gura no Mi',0,6),(24,'Bane Bane no Mi',0,6),(25,'Gura Gura no Mi',1,7),(26,'Hie Hie no Mi',0,7),(27,' Pika Pika no Mi',0,7),(28,'Goro Goro no Mi',0,7),(29,'Ope Ope no Mi',1,8),(30,'Hobi Hobi no Mi',0,8),(31,'Bara Bara no Mi',0,8),(32,'Bari Bari no Mi',0,8),(33,'Gojo Satoru',0,9),(34,' Mahito',1,9),(35,'Toge Inumaki',0,9),(36,'Sukuna',0,9),(37,'Find One Piece',0,10),(38,'Become a pirate',0,10),(39,'Draw a map of the world',1,10),(40,'Become a great swordsman',0,10),(41,'Domain Expansion',0,11),(42,'Cursed Energy Manipulation',0,11),(43,'Ten Shadows Technique',1,11),(44,'Black Flash',0,11),(45,'300,000,000',1,12),(46,'100,000,000',0,12),(47,'500,000,000',0,12),(48,'400,000,000',0,12);
/*!40000 ALTER TABLE `option` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profile`
--

DROP TABLE IF EXISTS `profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profile` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(30) NOT NULL,
  `avatar` varchar(255) NOT NULL,
  `bio` text,
  `user_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `profile_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profile`
--

LOCK TABLES `profile` WRITE;
/*!40000 ALTER TABLE `profile` DISABLE KEYS */;
INSERT INTO `profile` VALUES (1,'Luffy','static/images/todorokidefault.jpg','add bio.',1,'2024-02-28 21:53:13','2024-02-28 21:53:13'),(2,'iiHicham2k','static/images/gojodefault.jpg','add bio.',2,'2024-02-29 20:26:27','2024-02-29 20:26:27');
/*!40000 ALTER TABLE `profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `question` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question_text` text NOT NULL,
  `quiz_id` int NOT NULL,
  `score` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'Who is the main character of Naruto?',1,10),(2,'In which anime is the protagonist a pirate searching for the One Piece?',1,10),(3,'Who is the main character of Attack on Titan?',2,10),(4,'What is the name of the main character in My Hero Academia?',2,10),(5,'Which Devil Fruit grants its user the ability to manipulate darkness and create and control tangible constructs made of darkness?',3,20),(6,'What is the name of the Devil Fruit eaten by Buggy the Clown?',3,20),(7,'What is the name of the Devil Fruit eaten by white beard?',3,20),(8,'What is the name of the Devil Fruit eaten by Trafalgar Law?',3,20),(9,'Who manipulates souls in \"Jujutsu Kaisen\"?',4,20),(10,'Nami\'s childhood dream?',4,20),(11,'Megumi Fushiguro\'s summoning technique?',4,20),(12,'Luffy\'s first bounty after Enies Lobby?',4,20);
/*!40000 ALTER TABLE `question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  `level` varchar(100) NOT NULL,
  `user_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `quiz_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz`
--

LOCK TABLES `quiz` WRITE;
/*!40000 ALTER TABLE `quiz` DISABLE KEYS */;
INSERT INTO `quiz` VALUES (1,'Anime Quiz 1','Anime','Easy',1,'2024-02-28 21:54:33','2024-02-28 21:54:33'),(2,'Anime Quiz 2','Anime','Medium',1,'2024-02-28 21:54:33','2024-02-28 21:54:33'),(3,'One piece Devil fruit','Questions','Hard',1,'2024-02-29 20:25:00','2024-02-29 20:25:04'),(4,'Characters and Backstories','Questions','Hard',1,'2024-02-29 20:25:05','2024-02-29 20:25:06');
/*!40000 ALTER TABLE `quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_answer` text NOT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `score` int NOT NULL,
  `question_id` int NOT NULL,
  `quiz_id` int NOT NULL,
  `user_id` int NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `quiz_id` (`quiz_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`question_id`) REFERENCES `question` (`id`),
  CONSTRAINT `score_ibfk_2` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`id`),
  CONSTRAINT `score_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (1,'Kakashi Hatake',0,0,1,1,1,'2024-02-28 22:27:12','2024-02-28 22:27:12'),(2,'Bleach',0,0,2,1,1,'2024-02-28 22:27:12','2024-02-28 22:27:12'),(3,'Eren Yeager',1,1,3,2,1,'2024-02-28 22:30:36','2024-02-28 22:30:36'),(4,'Deku',1,2,4,2,1,'2024-02-28 22:30:36','2024-02-28 22:30:36'),(5,'Eren Yeager',1,1,3,2,1,'2024-02-28 22:38:39','2024-02-28 22:38:39'),(6,'Bakugo',0,1,4,2,1,'2024-02-28 22:38:39','2024-02-28 22:38:39'),(7,'Sasuke Uchiha',0,0,1,1,1,'2024-02-28 22:39:12','2024-02-28 22:39:12'),(8,'Bleach',0,0,2,1,1,'2024-02-28 22:39:12','2024-02-28 22:39:12'),(9,'Kakashi Hatake',0,0,1,1,1,'2024-02-28 22:39:35','2024-02-28 22:39:35'),(10,'Naruto',0,0,2,1,1,'2024-02-28 22:39:35','2024-02-28 22:39:35'),(11,'Yami Yami no Mi',1,1,5,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(12,'Bara Bara no Mi',1,2,6,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(13,'Gura Gura no Mi',1,3,7,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(14,'Ope Ope no Mi',1,4,8,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(15,' Mahito',1,1,9,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(16,'Draw a map of the world',1,2,10,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(17,'Ten Shadows Technique',1,3,11,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(18,'300,000,000',1,4,12,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(19,'Yami Yami no Mi',1,1,5,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(20,'Gura Gura no Mi',0,1,6,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(21,' Pika Pika no Mi',0,1,7,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(22,'Ope Ope no Mi',1,2,8,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(23,' Mahito',1,1,9,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(24,'Draw a map of the world',1,2,10,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(25,'Domain Expansion',0,2,11,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(26,'100,000,000',0,2,12,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56');
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(60) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Luffy','luffy@gmail.com','$2b$12$2VDJlVIkhizkHTEarnowIu5/SxMMYIgB2mc9ZqacImUNp4TlfFI3W','2024-02-28 21:53:13','2024-02-28 21:53:13'),(2,'iiHicham2k','hicham@gmail.com','$2b$12$Z6YrDCw3avNAijfTwxJB2.Giw4sEvtCsDKSr02rbFyydVzxGnT0Me','2024-02-29 20:26:27','2024-02-29 20:26:27');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-29 21:34:25
