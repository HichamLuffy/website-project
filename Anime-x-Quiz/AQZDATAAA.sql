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
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `text` text NOT NULL,
  `rating` int NOT NULL,
  `created_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_user_id` (`user_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,1,'woww nice site',5,'2024-03-11 19:48:25'),(19,2,'amazing work',5,'2024-03-11 20:59:12'),(20,2,'damn nice work',5,'2024-03-11 21:00:13'),(21,2,'hhhhhhhh',3,'2024-03-11 21:01:28');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `follower`
--

DROP TABLE IF EXISTS `follower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `follower` (
  `id` int NOT NULL AUTO_INCREMENT,
  `follower_id` int DEFAULT NULL,
  `followed_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `follower_id` (`follower_id`),
  KEY `followed_id` (`followed_id`),
  CONSTRAINT `follower_ibfk_1` FOREIGN KEY (`follower_id`) REFERENCES `user` (`id`),
  CONSTRAINT `follower_ibfk_2` FOREIGN KEY (`followed_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `follower`
--

LOCK TABLES `follower` WRITE;
/*!40000 ALTER TABLE `follower` DISABLE KEYS */;
INSERT INTO `follower` VALUES (1,1,2);
/*!40000 ALTER TABLE `follower` ENABLE KEYS */;
UNLOCK TABLES;

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
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `option`
--

LOCK TABLES `option` WRITE;
/*!40000 ALTER TABLE `option` DISABLE KEYS */;
INSERT INTO `option` VALUES (1,'Naruto Uzumaki',1,1),(2,'Sasuke Uchiha',0,1),(3,'Kakashi Hatake',0,1),(4,'Itachi Uchiha',0,1),(5,'Naruto',0,2),(6,'One Piece',0,2),(7,'Bleach',0,2),(8,'Fairy Tail',1,2),(9,'Eren Yeager',1,3),(10,'Levi Ackerman',0,3),(11,'Mikasa Ackerman',0,3),(12,'Armin Arlert',0,3),(13,'Deku',1,4),(14,'Bakugo',0,4),(15,'Todoroki',0,4),(16,'All Might',0,4),(17,'Gomu Gomu no Mi',0,5),(18,'Yami Yami no Mi',1,5),(19,'Mera Mera no Mi',0,5),(20,'Hie Hie no Mi',0,5),(21,'Hana Hana no Mi',0,6),(22,'Bara Bara no Mi',1,6),(23,'Gura Gura no Mi',0,6),(24,'Bane Bane no Mi',0,6),(25,'Gura Gura no Mi',1,7),(26,'Hie Hie no Mi',0,7),(27,' Pika Pika no Mi',0,7),(28,'Goro Goro no Mi',0,7),(29,'Ope Ope no Mi',1,8),(30,'Hobi Hobi no Mi',0,8),(31,'Bara Bara no Mi',0,8),(32,'Bari Bari no Mi',0,8),(33,'Gojo Satoru',0,9),(34,' Mahito',1,9),(35,'Toge Inumaki',0,9),(36,'Sukuna',0,9),(37,'Find One Piece',0,10),(38,'Become a pirate',0,10),(39,'Draw a map of the world',1,10),(40,'Become a great swordsman',0,10),(41,'Domain Expansion',0,11),(42,'Cursed Energy Manipulation',0,11),(43,'Ten Shadows Technique',1,11),(44,'Black Flash',0,11),(45,'300,000,000',1,12),(46,'100,000,000',0,12),(47,'500,000,000',0,12),(48,'400,000,000',0,12),(49,'one piece',0,13),(50,'jujutsu kaisen',1,13),(51,'Solo leveling',0,13),(52,'Demon slayer',0,13),(53,'MNHA',0,14),(54,'attack on titan',0,14),(55,'Solo leveling',1,14),(56,'Naruto',0,14),(57,'Yuji Itadori',1,15),(58,'Megumi Fushiguro',0,15),(59,'Nobara Kugisaki',0,15),(60,'Satoru Gojo',0,15),(61,'Nami',0,16),(62,'Roronoa Zoro',0,16),(63,'Monkey D. Luffy',1,16),(64,'Sanji',0,16),(65,'Tanjiro Kamado',0,17),(66,'Nezuko Kamado',1,17),(67,'Zenitsu Agatsuma',0,17),(68,'Inosuke Hashibira',0,17),(69,' Portgas D. Ace',0,18),(70,'Nico Robin',0,18),(71,'zoro',1,18),(72,'Usopp',0,18),(73,' Sasuke Uchiha',1,19),(74,'Shikamaru Nara',0,19),(75,' Gaara of the Sand',0,19),(76,' Rock Lee',0,19),(77,'Spirit Bomb',1,20),(78,'Kamehameha Wave',0,20),(79,'Instant Transmission',0,20),(80,'Kaioken',0,20),(81,'Raftel',0,21),(82,'Laugh Tale',1,21),(83,'Mariejois',0,21),(84,'Skypiea',0,21),(85,'Vegapunk',1,22),(86,'Gol D. Roger',0,22),(87,'Dr. Kureha',0,22),(88,'Monkey D. Garp',0,22),(89,'Big Mom',0,24),(90,'Blackbeard',0,24),(91,'Kaido',1,24),(92,'shanks',0,24),(93,'Sanji',0,25),(94,'Franky',1,25),(95,'Chopper',0,25),(96,'Robin',0,25),(97,'sukuna',0,26),(98,'geto',1,26),(99,'yoji',0,26),(100,'aa',0,26),(101,'gojo',1,27),(102,'yuta',0,27),(103,'yoju',0,27),(104,'toji',0,27),(105,'tanjiro',0,28),(106,'muzan',1,28),(107,'tengen',0,28),(108,'nezeku',0,28),(109,'luffy',1,29),(110,'zoro',0,29),(111,'joyboy',0,29),(112,'kaido',0,29),(113,'30,000,000 Berries',1,30),(114,'100,000,000 Berries',0,30),(115,'10,000,000 Berries',0,30),(116,'50,000,000 Berries',0,30),(117,'8',0,31),(118,'7',1,31),(119,'9',0,31),(120,'6',0,31),(121,'Water 7',0,32),(122,' Foosha Village',1,32),(123,'Sabaody Archipelago',0,32),(124,'Loguetown',0,32),(125,'Meat',1,33),(126,' Rice balls',0,33),(127,'Fish',0,33),(128,'Ramen',0,33),(129,'Hie Hie no Mi',0,34),(130,'Mera Mera no Mi',0,34),(131,'Gura Gura no Mi',0,34),(132,'Gomu Gomu no Mi',1,34),(133,'7 years',1,35),(134,'10 years',0,35),(135,'A few weeks',0,35),(136,'3 years',0,35);
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
INSERT INTO `profile` VALUES (1,'Luffy','6fbdb6d9d64231bc.PNG','S A Y O N A R A',1,'2024-02-28 21:53:13','2024-02-28 21:53:13'),(2,'iiHicham2k','9c2567150b961ce1.jpg','add bio.',2,'2024-02-29 20:26:27','2024-02-29 20:26:27');
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
  `score` int NOT NULL DEFAULT '10',
  `image_path` varchar(255) DEFAULT NULL,
  `sound_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `quiz_id` (`quiz_id`),
  CONSTRAINT `question_ibfk_1` FOREIGN KEY (`quiz_id`) REFERENCES `quiz` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `question`
--

LOCK TABLES `question` WRITE;
/*!40000 ALTER TABLE `question` DISABLE KEYS */;
INSERT INTO `question` VALUES (1,'Who is the main character of Naruto?',1,10,NULL,NULL),(2,'In which anime is the protagonist a pirate searching for the One Piece?',1,10,NULL,NULL),(3,'Who is the main character of Attack on Titan?',2,10,NULL,NULL),(4,'What is the name of the main character in My Hero Academia?',2,10,NULL,NULL),(5,'Which Devil Fruit grants its user the ability to manipulate darkness and create and control tangible constructs made of darkness?',3,20,NULL,NULL),(6,'What is the name of the Devil Fruit eaten by Buggy the Clown?',3,20,NULL,NULL),(7,'What is the name of the Devil Fruit eaten by white beard?',3,20,NULL,NULL),(8,'What is the name of the Devil Fruit eaten by Trafalgar Law?',3,20,NULL,NULL),(9,'Who manipulates souls in \"Jujutsu Kaisen\"?',4,20,NULL,NULL),(10,'Nami\'s childhood dream?',4,20,NULL,NULL),(11,'Megumi Fushiguro\'s summoning technique?',4,20,NULL,NULL),(12,'Luffy\'s first bounty after Enies Lobby?',4,20,NULL,NULL),(13,'from what anime is this opening',5,10,NULL,'../static/sounds/op/jjkop.mp3'),(14,'from what anime is this opening',5,10,NULL,'../static/sounds/op/soloop.mp3'),(15,'who is this character',6,10,'../static/images/imgquestions/itadory.PNG',''),(16,'who is this character',6,10,'../static/images/imgquestions/luffysmile.PNG',''),(17,'who is this character',6,10,'../static/images/imgquestions/Nezuku.jpg',''),(18,'who is this character',6,10,'../static/images/imgquestions/zoroeye.PNG',''),(19,'In the anime \"Naruto,\" what is the name of Naruto\'s primary rival',7,10,NULL,NULL),(20,'In \"Dragon Ball Z,\" what technique does Goku use to defeat Frieza on Namek',7,10,NULL,NULL),(21,'What is the name of the island where the Straw Hat Pirates found the legendary One Piece?',8,10,NULL,NULL),(22,'Who can create the Devil Fruits in the world of \"One Piece\"',8,10,NULL,NULL),(24,'Which of the following characters is known as the \"Strongest Creature in the World\" in \"One Piece\"?',8,10,NULL,NULL),(25,'Who is the shipwright of the Straw Hat Pirates?',8,10,NULL,NULL),(26,'who is gojo\'best friend',12,10,NULL,NULL),(27,'who killed geto',12,10,NULL,NULL),(28,'who is the best strongest in demon slayer',13,10,NULL,NULL),(29,'the main character of one piece ',14,10,NULL,NULL),(30,'Luffy\'s first bounty?',15,10,NULL,NULL),(31,'Luffy\'s age when he first met sabo',15,10,NULL,NULL),(32,'Luffy\'s hometown?',15,10,NULL,NULL),(33,'Luffy\'s favorite food?',15,10,NULL,NULL),(34,'Luffy\'s devil fruit power?',15,10,NULL,NULL),(35,'how much luffy spend time with sabo ace in the flash back',15,10,NULL,NULL);
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
  `quizpic` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `quiz_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz`
--

LOCK TABLES `quiz` WRITE;
/*!40000 ALTER TABLE `quiz` DISABLE KEYS */;
INSERT INTO `quiz` VALUES (1,'Anime Quiz 1','Anime','Easy',1,'2024-02-28 21:54:33','2024-02-28 21:54:33','animeqq.PNG'),(2,'Anime Quiz 2','Anime','Medium',1,'2024-02-28 21:54:33','2024-02-28 21:54:33','animeqq.PNG'),(3,'One piece Devil fruit','Questions','Hard',1,'2024-02-29 20:25:00','2024-02-29 20:25:04','devilfruit.PNG'),(4,'Characters and Backstories','Questions','Hard',1,'2024-02-29 20:25:05','2024-02-29 20:25:06','backstorys.PNG'),(5,'Anime opening','sound','Easy',1,'2024-03-01 17:38:49','2024-03-01 17:38:50','opening.PNG'),(6,'Guess The Character','image','Easy',1,'2024-03-01 18:07:37','2024-03-01 18:07:39','animeeye.png'),(7,'Random question','Question','Easy',1,'2024-03-09 01:37:28','2024-03-09 01:37:30','questions.jpg'),(8,'One Piece World','Question','Easy',1,'2024-03-09 01:38:05','2024-03-09 01:38:06','onepiecewolrd.PNG'),(12,'gojo quiz','category1','easy',1,'2024-03-10 17:09:25','2024-03-10 17:09:25','gojoobackground.png'),(13,'demon slayer quiz','category1','easy',1,'2024-03-11 01:46:28','2024-03-11 01:46:28','tanjirobackground.jpg'),(14,'one piece quiz','category1','easy',1,'2024-03-11 02:06:19','2024-03-11 02:06:19','56e0a1d764bdd89f.png'),(15,'how much you know about luffy','category1','easy',2,'2024-03-11 21:47:35','2024-03-11 21:47:35','d2ec4da02763a586.png');
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
) ENGINE=InnoDB AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (1,'Kakashi Hatake',0,0,1,1,1,'2024-02-28 22:27:12','2024-02-28 22:27:12'),(2,'Bleach',0,0,2,1,1,'2024-02-28 22:27:12','2024-02-28 22:27:12'),(3,'Eren Yeager',1,1,3,2,1,'2024-02-28 22:30:36','2024-02-28 22:30:36'),(4,'Deku',1,2,4,2,1,'2024-02-28 22:30:36','2024-02-28 22:30:36'),(5,'Eren Yeager',1,1,3,2,1,'2024-02-28 22:38:39','2024-02-28 22:38:39'),(6,'Bakugo',0,1,4,2,1,'2024-02-28 22:38:39','2024-02-28 22:38:39'),(7,'Sasuke Uchiha',0,0,1,1,1,'2024-02-28 22:39:12','2024-02-28 22:39:12'),(8,'Bleach',0,0,2,1,1,'2024-02-28 22:39:12','2024-02-28 22:39:12'),(9,'Kakashi Hatake',0,0,1,1,1,'2024-02-28 22:39:35','2024-02-28 22:39:35'),(10,'Naruto',0,0,2,1,1,'2024-02-28 22:39:35','2024-02-28 22:39:35'),(11,'Yami Yami no Mi',1,1,5,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(12,'Bara Bara no Mi',1,2,6,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(13,'Gura Gura no Mi',1,3,7,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(14,'Ope Ope no Mi',1,4,8,3,1,'2024-02-29 20:04:47','2024-02-29 20:04:47'),(15,' Mahito',1,1,9,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(16,'Draw a map of the world',1,2,10,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(17,'Ten Shadows Technique',1,3,11,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(18,'300,000,000',1,4,12,4,1,'2024-02-29 20:05:28','2024-02-29 20:05:28'),(19,'Yami Yami no Mi',1,1,5,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(20,'Gura Gura no Mi',0,1,6,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(21,' Pika Pika no Mi',0,1,7,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(22,'Ope Ope no Mi',1,2,8,3,1,'2024-02-29 20:12:44','2024-02-29 20:12:44'),(23,' Mahito',1,1,9,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(24,'Draw a map of the world',1,2,10,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(25,'Domain Expansion',0,2,11,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(26,'100,000,000',0,2,12,4,2,'2024-02-29 20:26:56','2024-02-29 20:26:56'),(27,'Mera Mera no Mi',0,0,5,3,1,'2024-02-29 21:01:49','2024-02-29 21:01:49'),(28,'Gura Gura no Mi',0,0,6,3,1,'2024-02-29 21:01:49','2024-02-29 21:01:49'),(29,'Gura Gura no Mi',1,1,7,3,1,'2024-02-29 21:01:49','2024-02-29 21:01:49'),(30,'Ope Ope no Mi',1,2,8,3,1,'2024-02-29 21:01:49','2024-02-29 21:01:49'),(31,'jujutsu kaisen',1,1,13,5,1,'2024-03-01 16:49:53','2024-03-01 16:49:53'),(32,'jujutsu kaisen',1,1,13,5,1,'2024-03-01 17:22:47','2024-03-01 17:22:47'),(33,'Solo leveling',1,2,14,5,1,'2024-03-01 17:22:47','2024-03-01 17:22:47'),(34,'Yuji Itadori',1,1,15,6,1,'2024-03-01 17:30:00','2024-03-01 17:30:00'),(35,'Monkey D. Luffy',1,2,16,6,1,'2024-03-01 17:30:00','2024-03-01 17:30:00'),(36,'Nezuko Kamado',1,3,17,6,1,'2024-03-01 17:30:00','2024-03-01 17:30:00'),(37,'zoro',1,4,18,6,1,'2024-03-01 17:30:00','2024-03-01 17:30:00'),(38,'Megumi Fushiguro',0,0,15,6,1,'2024-03-01 17:30:31','2024-03-01 17:30:31'),(39,'Nami',0,0,16,6,1,'2024-03-01 17:30:31','2024-03-01 17:30:31'),(40,'Nezuko Kamado',1,1,17,6,1,'2024-03-01 17:30:31','2024-03-01 17:30:31'),(41,'Nico Robin',0,1,18,6,1,'2024-03-01 17:30:31','2024-03-01 17:30:31'),(42,'jujutsu kaisen',1,1,13,5,1,'2024-03-06 19:25:53','2024-03-06 19:25:53'),(43,'attack on titan',0,1,14,5,1,'2024-03-06 19:25:53','2024-03-06 19:25:53'),(44,'Toge Inumaki',0,0,9,4,2,'2024-03-06 20:31:44','2024-03-06 20:31:44'),(45,'Find One Piece',0,0,10,4,2,'2024-03-06 20:31:44','2024-03-06 20:31:44'),(46,'Ten Shadows Technique',1,1,11,4,2,'2024-03-06 20:31:44','2024-03-06 20:31:44'),(47,'100,000,000',0,1,12,4,2,'2024-03-06 20:31:44','2024-03-06 20:31:44'),(48,'Yuji Itadori',1,1,15,6,1,'2024-03-09 00:13:07','2024-03-09 00:13:07'),(49,'Yuji Itadori',1,1,16,6,1,'2024-03-09 00:13:07','2024-03-09 00:13:07'),(50,'Yuji Itadori',1,1,17,6,1,'2024-03-09 00:13:07','2024-03-09 00:13:07'),(51,'Yuji Itadori',1,1,18,6,1,'2024-03-09 00:13:07','2024-03-09 00:13:07'),(52,'Nobara Kugisaki',0,0,15,6,1,'2024-03-09 00:17:24','2024-03-09 00:17:24'),(53,'Sanji',0,0,16,6,1,'2024-03-09 00:17:24','2024-03-09 00:17:24'),(54,'Tanjiro Kamado',0,0,17,6,1,'2024-03-09 00:17:24','2024-03-09 00:17:24'),(55,'zoro',1,1,18,6,1,'2024-03-09 00:17:24','2024-03-09 00:17:24'),(56,'Yuji Itadori',1,1,15,6,1,'2024-03-09 00:31:08','2024-03-09 00:31:08'),(57,'Monkey D. Luffy',1,2,16,6,1,'2024-03-09 00:31:08','2024-03-09 00:31:08'),(58,'Nezuko Kamado',1,3,17,6,1,'2024-03-09 00:31:08','2024-03-09 00:31:08'),(59,'zoro',1,4,18,6,1,'2024-03-09 00:31:08','2024-03-09 00:31:08'),(60,'Nobara Kugisaki',0,0,15,6,1,'2024-03-09 00:31:35','2024-03-09 00:31:35'),(61,'Sanji',0,0,16,6,1,'2024-03-09 00:31:35','2024-03-09 00:31:35'),(62,'Zenitsu Agatsuma',0,0,17,6,1,'2024-03-09 00:31:35','2024-03-09 00:31:35'),(63,'zoro',1,1,18,6,1,'2024-03-09 00:31:35','2024-03-09 00:31:35'),(64,'Laugh Tale',1,1,21,8,1,'2024-03-09 01:58:43','2024-03-09 01:58:43'),(65,'Vegapunk',1,2,22,8,1,'2024-03-09 01:58:43','2024-03-09 01:58:43'),(66,'Kaido',1,3,24,8,1,'2024-03-09 01:58:43','2024-03-09 01:58:43'),(67,'Franky',1,4,25,8,1,'2024-03-09 01:58:43','2024-03-09 01:58:43'),(68,'geto',1,1,26,12,1,'2024-03-10 17:10:00','2024-03-10 17:10:00'),(69,'gojo',1,2,27,12,1,'2024-03-10 17:10:00','2024-03-10 17:10:00'),(70,'geto',1,1,26,12,1,'2024-03-10 20:33:25','2024-03-10 20:33:25'),(71,'gojo',1,2,27,12,1,'2024-03-10 20:33:25','2024-03-10 20:33:25'),(72,'geto',1,1,26,12,1,'2024-03-10 21:24:27','2024-03-10 21:24:27'),(73,'gojo',1,2,27,12,1,'2024-03-10 21:24:27','2024-03-10 21:24:27'),(74,'Yuji Itadori',1,1,15,6,1,'2024-03-10 21:28:19','2024-03-10 21:28:19'),(75,'Monkey D. Luffy',1,2,16,6,1,'2024-03-10 21:28:19','2024-03-10 21:28:19'),(76,'Nezuko Kamado',1,3,17,6,1,'2024-03-10 21:28:19','2024-03-10 21:28:19'),(77,'zoro',1,4,18,6,1,'2024-03-10 21:28:19','2024-03-10 21:28:19'),(78,'jujutsu kaisen',1,1,13,5,1,'2024-03-10 21:35:00','2024-03-10 21:35:00'),(79,'Solo leveling',1,2,14,5,1,'2024-03-10 21:35:00','2024-03-10 21:35:00'),(80,'Yuji Itadori',1,1,15,6,1,'2024-03-10 21:49:53','2024-03-10 21:49:53'),(81,'Monkey D. Luffy',1,2,16,6,1,'2024-03-10 21:49:53','2024-03-10 21:49:53'),(82,'Nezuko Kamado',1,3,17,6,1,'2024-03-10 21:49:53','2024-03-10 21:49:53'),(83,'zoro',1,4,18,6,1,'2024-03-10 21:49:53','2024-03-10 21:49:53'),(84,'jujutsu kaisen',1,1,13,5,1,'2024-03-11 18:26:43','2024-03-11 18:26:43'),(85,'Solo leveling',1,2,14,5,1,'2024-03-11 18:26:43','2024-03-11 18:26:43'),(86,'Yuji Itadori',1,1,15,6,2,'2024-03-11 23:45:23','2024-03-11 23:45:23'),(87,'Monkey D. Luffy',1,2,16,6,2,'2024-03-11 23:45:23','2024-03-11 23:45:23'),(88,'Nezuko Kamado',1,3,17,6,2,'2024-03-11 23:45:23','2024-03-11 23:45:23'),(89,'zoro',1,4,18,6,2,'2024-03-11 23:45:23','2024-03-11 23:45:23');
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
  `last_seen` datetime DEFAULT CURRENT_TIMESTAMP,
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
INSERT INTO `user` VALUES (1,'Luffy','luffy@gmail.com','$2b$12$2VDJlVIkhizkHTEarnowIu5/SxMMYIgB2mc9ZqacImUNp4TlfFI3W','2024-02-28 21:53:13','2024-02-28 21:53:13','2024-03-11 23:24:56'),(2,'iiHicham2k','hicham@gmail.com','$2b$12$Z6YrDCw3avNAijfTwxJB2.Giw4sEvtCsDKSr02rbFyydVzxGnT0Me','2024-02-29 20:26:27','2024-02-29 20:26:27','2024-03-11 23:45:24');
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

-- Dump completed on 2024-03-11 23:54:58
