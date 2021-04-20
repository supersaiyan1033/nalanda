CREATE DATABASE  IF NOT EXISTS `nalanda` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `nalanda`;
-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: nalanda
-- ------------------------------------------------------
-- Server version	8.0.21

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `Book_ID` int NOT NULL AUTO_INCREMENT,
  `ISBN` int NOT NULL,
  `Shelf_ID` int NOT NULL,
  `Copy_number` int NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`Book_ID`),
  KEY `s_id_idx` (`Shelf_ID`),
  KEY `inder_idx` (`ISBN`),
  CONSTRAINT `inder` FOREIGN KEY (`ISBN`) REFERENCES `isbn` (`ISBN`),
  CONSTRAINT `s_id` FOREIGN KEY (`Shelf_ID`) REFERENCES `shelf` (`Shelf_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book`
--

LOCK TABLES `book` WRITE;
/*!40000 ALTER TABLE `book` DISABLE KEYS */;
INSERT INTO `book` VALUES (2,2746893,1,2,'On shelf'),(3,1445658,2,23,'On shelf'),(4,2874123,2,15,'On shlef'),(5,1523254,3,20,'On shelf'),(6,4123965,1,11,'On shelf'),(7,6352369,5,19,'On shelf'),(8,8564123,4,25,'On shelf'),(9,3658942,5,11,'On shelf'),(10,6352369,5,23,'On shelf');
/*!40000 ALTER TABLE `book` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2021-04-18 12:03:57.200295'),(2,'auth','0001_initial','2021-04-18 12:03:58.180220'),(3,'admin','0001_initial','2021-04-18 12:03:58.383492'),(4,'admin','0002_logentry_remove_auto_add','2021-04-18 12:03:58.397493'),(5,'admin','0003_logentry_add_action_flag_choices','2021-04-18 12:03:58.411495'),(6,'contenttypes','0002_remove_content_type_name','2021-04-18 12:03:58.543492'),(7,'auth','0002_alter_permission_name_max_length','2021-04-18 12:03:58.715288'),(8,'auth','0003_alter_user_email_max_length','2021-04-18 12:03:58.806535'),(9,'auth','0004_alter_user_username_opts','2021-04-18 12:03:58.819414'),(10,'auth','0005_alter_user_last_login_null','2021-04-18 12:03:58.895325'),(11,'auth','0006_require_contenttypes_0002','2021-04-18 12:03:58.900328'),(12,'auth','0007_alter_validators_add_error_messages','2021-04-18 12:03:58.911360'),(13,'auth','0008_alter_user_username_max_length','2021-04-18 12:03:58.996326'),(14,'auth','0009_alter_user_last_name_max_length','2021-04-18 12:03:59.082225'),(15,'auth','0010_alter_group_name_max_length','2021-04-18 12:03:59.109194'),(16,'auth','0011_update_proxy_permissions','2021-04-18 12:03:59.127191'),(17,'auth','0012_alter_user_first_name_max_length','2021-04-18 12:03:59.200191'),(18,'sessions','0001_initial','2021-04-18 12:03:59.260648');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('udfpn6je57ffvi1fmtqdre0vmuu0fpd3','.eJyrVsrJTCpKLMpMzPNMUbIy1FEqys9JVbJCCCvpKKXmJmbmAMWyE_NSDY2MlWoB8u0RiA:1lYhR2:BLlFjhfZ93zTgNMLKy2SnE2Lo31SSwkz8k04R6BHls8','2021-05-04 03:52:24.281858');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `friend_list`
--

DROP TABLE IF EXISTS `friend_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `friend_list` (
  `User_ID` int NOT NULL,
  `Friend_ID` int NOT NULL,
  `Status` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`User_ID`,`Friend_ID`),
  KEY `fid_idx` (`Friend_ID`),
  CONSTRAINT `fid` FOREIGN KEY (`Friend_ID`) REFERENCES `user` (`User_ID`),
  CONSTRAINT `usid` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `friend_list`
--

LOCK TABLES `friend_list` WRITE;
/*!40000 ALTER TABLE `friend_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `friend_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `isbn`
--

DROP TABLE IF EXISTS `isbn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `isbn` (
  `ISBN` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Year_of_Publication` year NOT NULL,
  `Genre` varchar(45) NOT NULL,
  `Author` varchar(200) NOT NULL,
  `Publisher` varchar(100) DEFAULT NULL,
  `Rating` int DEFAULT '0',
  `Total_no_of_copies` int NOT NULL,
  `Img_link` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`ISBN`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `isbn`
--

LOCK TABLES `isbn` WRITE;
/*!40000 ALTER TABLE `isbn` DISABLE KEYS */;
INSERT INTO `isbn` VALUES (1198563,'Artemis Fowl',2009,'Fiction','Eoin Colfer','Viking Press',NULL,35,'https://upload.wikimedia.org/wikipedia/en/0/07/Artemis_Fowl_first_edition_cover.jpg'),(1362598,'Evolution of Geographical Thought',2004,'History',' Majid Husain','Coleman Press',NULL,55,'https://images-na.ssl-images-amazon.com/images/I/51a1PVBjqCL._SX323_BO1,204,203,200_.jpg'),(1369802,'The Time Machine',1923,'Fiction ','H.G.Wells','Henry Holt and Company',NULL,60,'https://images-eu.ssl-images-amazon.com/images/I/51Zfgu-TTLL._SX198_BO1,204,203,200_QL40_FMwebp_.jpg'),(1445658,'War and Peace',1916,'Fiction','Leo Tolstoy','Mockra',NULL,30,'https://images-eu.ssl-images-amazon.com/images/I/51DFAicIbHL._SY264_BO1,204,203,200_QL40_FMwebp_.jpg'),(1523254,'Introduction to Engineering Mathematics',1998,'Science','Erzwig keigser','Pearson',NULL,60,'https://images-na.ssl-images-amazon.com/images/I/51C2Rl8tfqL._SX348_BO1,204,203,200_.jpg'),(1568947,'Genghis Khan and the Making of the Modern World',2004,'History','Jack Weatherford','NormanPress',NULL,50,'https://upload.wikimedia.org/wikipedia/en/9/95/Genghis_Khan_and_the_Making_of_the_Modern_World.jpg'),(1587432,'21 Lessons for the 21st Century',2018,'History','Yuval Noah Harari','Spiegel & Grau',NULL,15,'https://upload.wikimedia.org/wikipedia/en/thumb/5/5e/21_Lessons_for_the_21st_Century.jpg/200px-21_Lessons_for_the_21st_Century.jpg'),(1956874,'Computer Fundamentals and Programming in C',1994,'Science','Reema Thareja','Suchithra Raman press',NULL,45,'https://images-na.ssl-images-amazon.com/images/I/41TpD9+txWL._SX258_BO1,204,203,200_.jpg'),(2398756,'The Subtle Art of Not Giving a F*ck',2016,'Motivational','Mark Menson','HarperOne',NULL,50,'https://upload.wikimedia.org/wikipedia/en/thumb/b/bd/The_Subtle_Art_of_Not_Giving_a_F%2Ack_by_Mark_Manson_-_Book_Cover.png/220px-The_Subtle_Art_of_Not_Giving_a_F%2Ack_by_Mark_Manson_-_Book_Cover.png'),(2746893,'The Origin of Species.',1912,'History','Charles Darwin','Scholastic',NULL,100,'https://images-eu.ssl-images-amazon.com/images/I/51PNzwsl30L._SY264_BO1,204,203,200_QL40_FMwebp_.jpg'),(2874123,'Girl in Room 105',2018,'Fiction','Chetan Bhagat','Vermillion',NULL,30,'https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Girl_in_room_105.png/220px-Girl_in_room_105.png'),(2912356,'Introduction to Electrodynamics',1981,'Science','David J. Griffiths','Cambridge University Press',NULL,60,'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Front_cover_of_Griffiths%27_Electrodynamics.jpg/220px-Front_cover_of_Griffiths%27_Electrodynamics.jpg'),(3624756,'Wings of Fire',1999,'Motivational',' Dr A. P. J. Abdul Kalam','Universities Press',NULL,50,'https://upload.wikimedia.org/wikipedia/en/thumb/3/3a/Wings_of_Fire_by_A_P_J_Abdul_Kalam_Book_Cover.jpg/220px-Wings_of_Fire_by_A_P_J_Abdul_Kalam_Book_Cover.jpg'),(3658942,'Rich Dad Poor Dad',1990,'Motivational','Robert.T.Kiyosaki','Plata Publishing',NULL,25,'https://images-na.ssl-images-amazon.com/images/I/51wOOMQ+F3L._SY344_BO1,204,203,200_.jpg'),(4123965,'History of Modern India ',2001,'History',' Bipan Chandra','Black Swan',NULL,40,NULL),(5237152,'Mechanical Vibrations',1986,'Science','Singiresu S. Rao','JP Bathra',NULL,80,'https://images-na.ssl-images-amazon.com/images/I/41O2oQMy+dL._SX370_BO1,204,203,200_.jpg'),(5489723,'Pride and Prejudice.',1956,'Fiction','Jane Austen.','Cambridge Press',NULL,40,'https://upload.wikimedia.org/wikipedia/en/thumb/0/09/Brock_Pride_and_Prejudice.jpg/220px-Brock_Pride_and_Prejudice.jpg'),(6352369,'Python Crash Course',2019,'Science','Eric mathews','merryweather Press',NULL,25,'https://images-eu.ssl-images-amazon.com/images/I/51Z6Vf5UwTL._SX198_BO1,204,203,200_QL40_FMwebp_.jpg'),(7892361,'The Immortals of Meluha',2010,'Fiction',' Amish Tripathi','Westland Press',NULL,23,'https://upload.wikimedia.org/wikipedia/en/thumb/0/0e/The_Immortals_Of_Meluha.jpg/220px-The_Immortals_Of_Meluha.jpg'),(8564123,'The 7 Habits of Highly Effective People',1989,'Motivational','Stephen Covey','Free Press',NULL,30,'https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/The_7_Habits_of_Highly_Effective_People.jpg/220px-The_7_Habits_of_Highly_Effective_People.jpg');
/*!40000 ALTER TABLE `isbn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `librarian`
--

DROP TABLE IF EXISTS `librarian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `librarian` (
  `Librarian_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `DOB` date NOT NULL,
  PRIMARY KEY (`Librarian_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `librarian`
--

LOCK TABLES `librarian` WRITE;
/*!40000 ALTER TABLE `librarian` DISABLE KEYS */;
INSERT INTO `librarian` VALUES (1,'Kane Mama','$2b$12$2Pi0UxTaEM4ywTAZiTgCcO7VzsUTPQQd4doTgr5lZp6VdmKJ/g0fe','new zealand','kane123','2015-02-13'),(2,'revanth','$2b$12$8qNsbLfNDjLVZDhjU6bCTODybZM2Nx/0T0XGioGV0ppWWttGO0gpW','hi123 to 344','cse190001063@iiti.ac.in','2001-12-11');
/*!40000 ALTER TABLE `librarian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `on_hold`
--

DROP TABLE IF EXISTS `on_hold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `on_hold` (
  `Hold_ID` int NOT NULL AUTO_INCREMENT,
  `date_of_hold` datetime NOT NULL,
  `User_ID` int NOT NULL,
  `Book_ID` int NOT NULL,
  PRIMARY KEY (`Hold_ID`),
  KEY `usiid_idx` (`User_ID`),
  KEY `bnf_idx` (`Book_ID`),
  CONSTRAINT `bnf` FOREIGN KEY (`Book_ID`) REFERENCES `book` (`Book_ID`),
  CONSTRAINT `usiid` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `on_hold`
--

LOCK TABLES `on_hold` WRITE;
/*!40000 ALTER TABLE `on_hold` DISABLE KEYS */;
/*!40000 ALTER TABLE `on_hold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `on_loan`
--

DROP TABLE IF EXISTS `on_loan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `on_loan` (
  `Loan_ID` int NOT NULL AUTO_INCREMENT,
  `Book_ID` int DEFAULT NULL,
  `User_ID` int NOT NULL,
  `Date_of_Issue` datetime(6) NOT NULL,
  `last_email_date` datetime DEFAULT NULL,
  `Fine` int DEFAULT '0',
  `librarian_ID` int DEFAULT NULL,
  PRIMARY KEY (`Loan_ID`),
  KEY `ud_idx` (`User_ID`),
  KEY `bd_idx` (`Book_ID`),
  KEY `lde_idx` (`librarian_ID`),
  CONSTRAINT `bd` FOREIGN KEY (`Book_ID`) REFERENCES `book` (`Book_ID`),
  CONSTRAINT `lde` FOREIGN KEY (`librarian_ID`) REFERENCES `librarian` (`Librarian_ID`),
  CONSTRAINT `ud` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `on_loan`
--

LOCK TABLES `on_loan` WRITE;
/*!40000 ALTER TABLE `on_loan` DISABLE KEYS */;
/*!40000 ALTER TABLE `on_loan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `on_loan_on_hold`
--

DROP TABLE IF EXISTS `on_loan_on_hold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `on_loan_on_hold` (
  `Token_No` int NOT NULL AUTO_INCREMENT,
  `User_Id` int NOT NULL,
  `Time_stamp` datetime(6) DEFAULT NULL,
  `ISBN` int DEFAULT NULL,
  PRIMARY KEY (`Token_No`),
  KEY `userid_idx` (`User_Id`),
  KEY `inm_idx` (`ISBN`),
  CONSTRAINT `inm` FOREIGN KEY (`ISBN`) REFERENCES `isbn` (`ISBN`),
  CONSTRAINT `userid` FOREIGN KEY (`User_Id`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `on_loan_on_hold`
--

LOCK TABLES `on_loan_on_hold` WRITE;
/*!40000 ALTER TABLE `on_loan_on_hold` DISABLE KEYS */;
/*!40000 ALTER TABLE `on_loan_on_hold` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `previous_books`
--

DROP TABLE IF EXISTS `previous_books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `previous_books` (
  `User_ID` int NOT NULL,
  `Book_ID` int NOT NULL,
  `Date_of_issue` datetime NOT NULL,
  `Date_of_return` datetime DEFAULT NULL,
  `Fine` int DEFAULT NULL,
  PRIMARY KEY (`User_ID`,`Book_ID`),
  KEY `id_idx` (`User_ID`),
  KEY `ide_idx` (`Book_ID`),
  CONSTRAINT `i` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`),
  CONSTRAINT `ide` FOREIGN KEY (`Book_ID`) REFERENCES `book` (`Book_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `previous_books`
--

LOCK TABLES `previous_books` WRITE;
/*!40000 ALTER TABLE `previous_books` DISABLE KEYS */;
/*!40000 ALTER TABLE `previous_books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reading_list`
--

DROP TABLE IF EXISTS `reading_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reading_list` (
  `User_ID` int NOT NULL,
  `ISBN` int NOT NULL,
  PRIMARY KEY (`User_ID`,`ISBN`),
  KEY `ui_idx` (`User_ID`),
  KEY `isbnidfor_idx` (`ISBN`),
  CONSTRAINT `isbnidfor` FOREIGN KEY (`ISBN`) REFERENCES `isbn` (`ISBN`),
  CONSTRAINT `ui` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reading_list`
--

LOCK TABLES `reading_list` WRITE;
/*!40000 ALTER TABLE `reading_list` DISABLE KEYS */;
/*!40000 ALTER TABLE `reading_list` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `review` (
  `Review` varchar(250) DEFAULT NULL,
  `ISBN` int NOT NULL,
  `User_ID` int NOT NULL,
  `Rating` int DEFAULT NULL,
  PRIMARY KEY (`ISBN`,`User_ID`),
  KEY `rs_idx` (`User_ID`),
  CONSTRAINT `akis` FOREIGN KEY (`ISBN`) REFERENCES `isbn` (`ISBN`),
  CONSTRAINT `rs` FOREIGN KEY (`User_ID`) REFERENCES `user` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `review`
--

LOCK TABLES `review` WRITE;
/*!40000 ALTER TABLE `review` DISABLE KEYS */;
/*!40000 ALTER TABLE `review` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS `shelf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shelf` (
  `Shelf_ID` int NOT NULL,
  `Capacity` int DEFAULT NULL,
  PRIMARY KEY (`Shelf_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shelf`
--

LOCK TABLES `shelf` WRITE;
/*!40000 ALTER TABLE `shelf` DISABLE KEYS */;
INSERT INTO `shelf` VALUES (1,20),(2,30),(3,50),(4,45),(5,100);
/*!40000 ALTER TABLE `shelf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `User_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `email` varchar(100) CHARACTER SET utf8 NOT NULL,
  `DOB` date NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Category` varchar(45) CHARACTER SET utf8 NOT NULL,
  `Address` varchar(100) CHARACTER SET utf8 NOT NULL,
  `Unpaid_fees` int DEFAULT '0',
  PRIMARY KEY (`User_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Revanth','thotarevanth347@gmail.com','2001-12-11','$2b$12$Q/UTmfZkVjg98FtAkTq9x.GTnTP2UcqCrVmWC.PLGPB9qvrO5eKdC','Male','Flat no:CS3,My Home Complex,Beside SRR College, Machavaram, Vijayawada.',NULL),(2,'Roomno605','roomno605','2019-08-12','$2b$12$HTJ3KHyEfxQlA/VQDnLvGuxqv1H.bOvo2X53i96XzDjBI3Ss5xBCe','Student','Flat no:CS3,My Home Complex,Beside SRR College, Machavaram, Vijayawada.',NULL),(3,'sairam','cse190001026@iiti.ac.in','2021-04-01','$2b$12$HTJ3KHyEfxQlA/VQDnLvGuxqv1H.bOvo2X53i96XzDjBI3Ss5xBCe','Student','Flat no:CS3,My Home Complex,Beside SRR College, Machavaram, Vijayawada.',0),(4,'sumanth','thotarevanth347@yahoo.com','2021-04-06','$2b$12$S/YqFu76GrPoe6qA4ZIN2.9SDNNBjG3MAey8k3jSQpHQkDmRU0iO6','Faculty','Flat no:CS3,My Home Complex,Beside SRR College, Machavaram, Vijayawada.',0);
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

-- Dump completed on 2021-04-20 10:19:20
