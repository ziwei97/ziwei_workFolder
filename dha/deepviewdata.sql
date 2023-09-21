-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: imagingappdb
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
-- Table structure for table `anatomicallocation_imaging`
--

DROP TABLE IF EXISTS `anatomicallocation_imaging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `anatomicallocation_imaging` (
  `AnatomicalLocationID` int NOT NULL AUTO_INCREMENT,
  `LocationName` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `InnerSuffix` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`AnatomicalLocationID`),
  UNIQUE KEY `AnatomicalLocationID_UNIQUE` (`AnatomicalLocationID`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anatomicallocation_imaging`
--

LOCK TABLES `anatomicallocation_imaging` WRITE;
/*!40000 ALTER TABLE `anatomicallocation_imaging` DISABLE KEYS */;
INSERT INTO `anatomicallocation_imaging` VALUES (1,'Ant.Head','Lateral$Medial$Superior$Inferior'),(2,'Ant.Neck','Lateral$Medial$Superior$Inferior'),(3,'Ant.R.Shoulder','Lateral$Medial$Superior$Inferior'),(4,'Ant.L.Shoulder','Lateral$Medial$Superior$Inferior'),(5,'Ant.R.U.Trunk','Lateral$Medial$Superior$Inferior'),(6,'Ant.R.L.Trunk','Lateral$Medial$Superior$Inferior'),(7,'Ant.L.U.Trunk','Lateral$Medial$Superior$Inferior'),(8,'Ant.L.L.Trunk','Lateral$Medial$Superior$Inferior'),(9,'Genitalia',''),(10,'Ant.R.U.Arm','Lateral$Medial$Proximal$Distal'),(11,'Ant.R.L.Arm','Lateral$Medial$Proximal$Distal'),(12,'Ant.L.U.Arm','Lateral$Medial$Proximal$Distal'),(13,'Ant.L.L.Arm','Lateral$Medial$Proximal$Distal'),(14,'Ant.R.Hand','Lateral$Medial$Proximal$Distal'),(15,'Ant.L.Hand','Lateral$Medial$Proximal$Distal'),(16,'Ant.R.Thigh','Lateral$Medial$Proximal$Distal'),(17,'Ant.L.Thigh','Lateral$Medial$Proximal$Distal'),(18,'Ant.R.Leg','Lateral$Medial$Proximal$Distal'),(19,'Ant.L.Leg','Lateral$Medial$Proximal$Distal'),(20,'Ant.R.Foot','Lateral$Medial$Dorsal$Plantar'),(21,'Ant.L.Foot','Lateral$Medial$Dorsal$Plantar'),(22,'Post.Head','Lateral$Medial$Superior$Inferior'),(23,'Post.Neck','Lateral$Medial$Superior$Inferior'),(24,'Post.R.Shoulder','Lateral$Medial$Superior$Inferior'),(25,'Post.L.Shoulder','Lateral$Medial$Superior$Inferior'),(26,'Post.R.U.Trunk','Lateral$Medial$Superior$Inferior'),(27,'Post.R.L.Trunk','Lateral$Medial$Superior$Inferior'),(28,'Post.L.U.Trunk','Lateral$Medial$Superior$Inferior'),(29,'Post.L.L.Trunk','Lateral$Medial$Superior$Inferior'),(30,'Post.R.Buttock','Lateral$Medial$Superior$Inferior'),(31,'Post.L.Buttock','Lateral$Medial$Superior$Inferior'),(32,'Post.R.U.Arm','Lateral$Medial$Proximal$Distal'),(33,'Post.R.L.Arm','Lateral$Medial$Proximal$Distal'),(34,'Post.L.U.Arm','Lateral$Medial$Proximal$Distal'),(35,'Post.L.L.Arm','Lateral$Medial$Proximal$Distal'),(36,'Post.R.Hand','Lateral$Medial$Proximal$Distal'),(37,'Post.L.Hand','Lateral$Medial$Proximal$Distal'),(38,'Post.R.Thigh','Lateral$Medial$Proximal$Distal'),(39,'Post.L.Thigh','Lateral$Medial$Proximal$Distal'),(40,'Post.R.Leg','Lateral$Medial$Proximal$Distal'),(41,'Post.L.Leg','Lateral$Medial$Proximal$Distal'),(42,'Post.R.Foot','Lateral$Medial$Dorsal$Plantar'),(43,'Post.L.Foot','Lateral$Medial$Dorsal$Plantar');
/*!40000 ALTER TABLE `anatomicallocation_imaging` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceinfo_imaging`
--

DROP TABLE IF EXISTS `deviceinfo_imaging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deviceinfo_imaging` (
  `DeviceID` int NOT NULL AUTO_INCREMENT,
  `SiteName` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `DeviceSerialNumber` varchar(500) COLLATE utf8mb4_bin NOT NULL,
  `DeviceType` varchar(500) COLLATE utf8mb4_bin NOT NULL,
  `SWVersion` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL,
  `LastUpdate` bigint DEFAULT NULL,
  PRIMARY KEY (`DeviceID`,`SiteName`),
  UNIQUE KEY `DeviceID_UNIQUE` (`DeviceID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceinfo_imaging`
--

LOCK TABLES `deviceinfo_imaging` WRITE;
/*!40000 ALTER TABLE `deviceinfo_imaging` DISABLE KEYS */;
/*!40000 ALTER TABLE `deviceinfo_imaging` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagecollection_imaging`
--

DROP TABLE IF EXISTS `imagecollection_imaging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagecollection_imaging` (
  `IMCOLLID` int NOT NULL,
  `ImgCollGUID` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `WOUNDID` int NOT NULL,
  `ImageCollFolderName` varchar(260) COLLATE utf8mb4_bin NOT NULL,
  `ImageCollStatus` tinyint NOT NULL,
  `CreateDateTime` bigint NOT NULL,
  `LastUpdate` bigint NOT NULL,
  PRIMARY KEY (`IMCOLLID`),
  KEY `fk_WOUNDID_idx` (`WOUNDID`),
  CONSTRAINT `fk_WOUNDID` FOREIGN KEY (`WOUNDID`) REFERENCES `wounds_imaging` (`WOUNDID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagecollection_imaging`
--

LOCK TABLES `imagecollection_imaging` WRITE;
/*!40000 ALTER TABLE `imagecollection_imaging` DISABLE KEYS */;
INSERT INTO `imagecollection_imaging` VALUES (1,'b5872ca7-7b7d-4139-9922-8484c3357e4b',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_1',0,3896500876909263800,3896500876909263800),(2,'a80f3bc1-8b23-48f8-b030-45ef99ac7e20',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_2',0,3896501393010661100,3896501393010661100),(3,'37649d66-7be9-4a05-b874-dcf8379e2f32',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_3',0,3896502559477532300,3896502559477532300),(4,'237fd5d6-b16a-452a-b770-16ed4c9d9d54',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_4',0,3896502806392577400,3896502806392577400),(5,'d41dafd3-3382-46f8-b0df-abc03f41f921',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_5',0,3896503055983898800,3896503055984895000),(6,'b5c852f8-58d1-4690-be5c-58ce4ebe0686',1,'D:\\ImagingApp\\patient_1\\Ant.R.U.Trunk_Medial\\ImageColl_6',0,3896503866761599600,3896503866761599600),(7,'53e591d9-5f5d-4e07-ae7c-658af86b96e5',2,'D:\\ImagingApp\\patient_3\\Ant.Head_Medial\\ImageColl_7',0,3896690128351531800,3896690128351531800),(8,'dbe398fe-ff8b-4f7e-9175-9ded7bafd27e',2,'D:\\ImagingApp\\patient_3\\Ant.Head_Medial\\ImageColl_8',0,3896690543053117000,3896690543053117000),(9,'3d5ec04c-a73b-4e84-ac32-99000884847b',3,'D:\\ImagingApp\\patient_4\\Ant.R.L.Arm_Lateral\\ImageColl_9',0,3896847632897590200,3896847632897590200),(10,'e32ddebf-61ba-4d65-8aae-c1c000b82aa0',3,'D:\\ImagingApp\\patient_4\\Ant.R.L.Arm_Lateral\\ImageColl_10',0,3896847652267830800,3896847652267830800),(11,'0461dc04-c77b-450e-b614-6931962c9dc0',4,'D:\\ImagingApp\\patient_4\\Ant.L.U.Arm_Lateral\\ImageColl_11',0,3896847698822033800,3896847698822033800),(12,'ecfc2abc-019f-4cb6-8c91-bce16091c00b',4,'D:\\ImagingApp\\patient_4\\Ant.L.U.Arm_Lateral\\ImageColl_12',0,3896847725353920900,3896847725353920900),(13,'6e79a982-7eee-4b9a-8ffd-15e4aaa735ce',5,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Lateral\\ImageColl_13',0,3896847808007614000,3896847808007614000),(14,'aecdcd88-9677-45fd-a616-d9aad68c2a30',5,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Lateral\\ImageColl_14',0,3896847824104951900,3896847824104951900),(15,'25d5a384-dfb3-4cf9-bce0-355b56c30c89',6,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Medial\\ImageColl_15',0,3896847870481725000,3896847870481725000),(16,'b0a9cc32-2952-4858-83cf-6937afa143af',6,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Medial\\ImageColl_16',0,3896847884811870200,3896847884811870200),(17,'6ac11e0d-77b6-4c0a-91c1-ab3f9fb503ff',7,'D:\\ImagingApp\\patient_5\\Post.L.L.Trunk_Superior\\ImageColl_17',0,3896925116565440500,3896925116565440500),(18,'b8b1865a-686b-469c-ae87-478672494cb1',7,'D:\\ImagingApp\\patient_5\\Post.L.L.Trunk_Superior\\ImageColl_18',0,3896925132550978200,3896925132550978200),(19,'267903a8-0e44-4728-897e-9b12281d87bf',8,'D:\\ImagingApp\\patient_5\\Ant.L.U.Trunk_Superior\\ImageColl_19',0,3896925212438198400,3896925212438198400),(20,'cb180cc5-f05b-4454-8d6c-745b927be6bc',8,'D:\\ImagingApp\\patient_5\\Ant.L.U.Trunk_Superior\\ImageColl_20',0,3896925225946106600,3896925225946106600),(21,'92468abe-64b7-45d2-a7e7-1d24ac78e7d0',3,'D:\\ImagingApp\\patient_4\\Ant.R.L.Arm_Lateral\\ImageColl_21',0,3897007008004662600,3897007008004662600),(22,'928516c1-43bc-4bdb-94ba-69fc046c0d2b',3,'D:\\ImagingApp\\patient_4\\Ant.R.L.Arm_Lateral\\ImageColl_22',0,3897007024189745700,3897007024189745700),(23,'265d40e9-a755-422e-b9a1-7904a1d7cdfc',4,'D:\\ImagingApp\\patient_4\\Ant.L.U.Arm_Lateral\\ImageColl_23',0,3897007052586623600,3897007052586623600),(24,'282b5bb1-470d-4939-afec-eed718bab3a8',4,'D:\\ImagingApp\\patient_4\\Ant.L.U.Arm_Lateral\\ImageColl_24',0,3897007070324182400,3897007070324182400),(25,'b06b9182-3a9a-43eb-b3dd-99f46b31676d',5,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Lateral\\ImageColl_25',0,3897007114618975500,3897007114618975500),(26,'f32ffb1b-d73e-45a4-ac46-7124b0e263ad',5,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Lateral\\ImageColl_26',0,3897007128711199900,3897007128711199900),(27,'d7618a5c-3165-497d-8591-f3d5a6243ec4',6,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Medial\\ImageColl_27',0,3897007154787810600,3897007154787810600),(28,'7619a402-36a1-438f-a30d-f7004500c99f',6,'D:\\ImagingApp\\patient_4\\Ant.L.L.Arm_Medial\\ImageColl_28',0,3897007179871989900,3897007179871989900),(29,'06845ce1-6d75-4426-a5fe-719d58a9ac84',8,'D:\\ImagingApp\\patient_5\\Ant.L.U.Trunk_Superior\\ImageColl_29',0,3897022484831533600,3897022484831533600),(30,'317a5cb1-1e08-4c1d-acc3-1462e59e2443',8,'D:\\ImagingApp\\patient_5\\Ant.L.U.Trunk_Superior\\ImageColl_30',0,3897022501823062400,3897022501823062400),(31,'701c8a8e-87a5-4149-950b-66e3dec445bf',9,'D:\\ImagingApp\\patient_6\\Ant.R.L.Arm_Proximal\\ImageColl_31',0,3897107391426153600,3897107391426153600),(32,'7f075162-0278-4baa-8d46-d9b05d2d0b08',9,'D:\\ImagingApp\\patient_6\\Ant.R.L.Arm_Proximal\\ImageColl_32',0,3897107407386983000,3897107407386983000),(33,'c891b854-20b8-4c43-86ee-08d1532d8bee',10,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Lateral\\ImageColl_33',0,3897107507118342300,3897107507118342300),(34,'6e6ea761-9f34-4378-afe2-47057962a193',10,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Lateral\\ImageColl_34',0,3897107524678982600,3897107524678982600),(35,'34cc92c8-49c9-43ab-9f40-504869a3018b',11,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Medial\\ImageColl_35',0,3897107596945000400,3897107596945000400),(36,'9c13f8e7-f9f1-43f0-8b0a-15f2edba01ef',11,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Medial\\ImageColl_36',0,3897107611855094200,3897107611855094200),(37,'faa362e1-a49e-4a4d-92bc-7bdc9a2d5f41',12,'D:\\ImagingApp\\patient_7\\Ant.R.Leg_Lateral\\ImageColl_37',0,3897383431312279100,3897383431312279100),(38,'3273552b-a6c7-4e34-8f9e-e7ca8c6f8512',12,'D:\\ImagingApp\\patient_7\\Ant.R.Leg_Lateral\\ImageColl_38',0,3897383450951884800,3897383450951884800),(39,'e1b805fb-bdf3-4012-880e-8095e7ea9817',13,'D:\\ImagingApp\\patient_7\\Ant.R.Leg_Medial\\ImageColl_39',0,3897383502292318700,3897383502292318700),(40,'6b2f383b-7a78-4eba-bafc-ab688cb3ed14',13,'D:\\ImagingApp\\patient_7\\Ant.R.Leg_Medial\\ImageColl_40',0,3897383519539138600,3897383519539138600),(41,'4b995d14-c5a9-4f55-a8c6-c93802488f89',9,'D:\\ImagingApp\\patient_6\\Ant.R.L.Arm_Proximal\\ImageColl_41',0,3897444890084392800,3897444890084392800),(42,'1d2800cd-4b71-48c4-8731-fbf3a89ab9d3',9,'D:\\ImagingApp\\patient_6\\Ant.R.L.Arm_Proximal\\ImageColl_42',0,3897444928536092000,3897444928536092000),(43,'09828ccb-c69e-41c0-b0ab-2d01db732a27',10,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Lateral\\ImageColl_43',0,3897444960297983700,3897444960297983700),(44,'9c9e3af5-e0b0-4ee1-b386-16c366811dff',10,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Lateral\\ImageColl_44',0,3897444975942252200,3897444975942252200),(45,'5bd36991-01df-4870-a213-8b998b39281e',11,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Medial\\ImageColl_45',0,3897445010659723100,3897445010659723100),(46,'7fab84e9-5c9f-49e2-a3e9-ae28b7d6eb60',11,'D:\\ImagingApp\\patient_6\\Ant.R.Leg_Medial\\ImageColl_46',0,3897445026405695100,3897445026405695100),(47,'e96c2962-e863-4403-8961-141170702a53',14,'D:\\ImagingApp\\patient_8\\Ant.L.U.Trunk_Medial\\ImageColl_47',0,3897798980730723600,3897798980730723600),(48,'ca1350d6-053a-4fdd-8d45-96d0e2526056',14,'D:\\ImagingApp\\patient_8\\Ant.L.U.Trunk_Medial\\ImageColl_48',0,3897799004859998200,3897799004859998200),(49,'f787b151-ca40-4edb-87ff-302ab6a233a3',15,'D:\\ImagingApp\\patient_8\\Ant.R.L.Arm_Distal\\ImageColl_49',0,3897799067345056700,3897799067345056700),(50,'89b4ded4-a708-4080-8147-5e101d5c1501',15,'D:\\ImagingApp\\patient_8\\Ant.R.L.Arm_Distal\\ImageColl_50',0,3897799085207674200,3897799085207674200),(51,'8f25698b-06da-47c6-bc73-f06bbc27bee9',16,'D:\\ImagingApp\\patient_9\\Post.R.U.Trunk_Lateral\\ImageColl_51',0,3899426698363270500,3899426698363270500),(52,'f30ccd61-8e60-4c97-8395-2330194349e3',16,'D:\\ImagingApp\\patient_9\\Post.R.U.Trunk_Lateral\\ImageColl_52',0,3899426721977825600,3899426721977825600),(53,'a4408bb6-a376-43f0-b385-774a376eacce',17,'D:\\ImagingApp\\patient_9\\Post.R.U.Arm_Lateral\\ImageColl_53',0,3899426768118465300,3899426768118465300),(54,'b521c07a-7569-40f4-b11b-83fef0169213',17,'D:\\ImagingApp\\patient_9\\Post.R.U.Arm_Lateral\\ImageColl_54',0,3899426783694663900,3899426783694663900),(55,'41195aae-d848-427b-8d99-a81a5e7764ca',18,'D:\\ImagingApp\\patient_9\\Post.R.Thigh_Lateral\\ImageColl_55',0,3899426821012634500,3899426821012634500),(56,'69780eeb-b1ae-4f08-a03c-a32576485fae',18,'D:\\ImagingApp\\patient_9\\Post.R.Thigh_Lateral\\ImageColl_56',0,3899426836374988900,3899426836374988900),(57,'9657b8d1-d07b-4e8d-9e1f-826aea4beb54',19,'D:\\ImagingApp\\patient_9\\Post.R.Leg_Lateral\\ImageColl_57',0,3899426868218642900,3899426868218642900),(58,'bc39cff4-80d8-4f98-8aeb-1540d363b87b',19,'D:\\ImagingApp\\patient_9\\Post.R.Leg_Lateral\\ImageColl_58',0,3899426882708768400,3899426882708768400);
/*!40000 ALTER TABLE `imagecollection_imaging` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_imaging`
--

DROP TABLE IF EXISTS `patient_imaging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_imaging` (
  `PID` int NOT NULL,
  `PGUID` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `FirstName` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `LastName` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `Identifiable` tinyint DEFAULT NULL,
  `Height` float DEFAULT NULL,
  `Weight` float DEFAULT NULL,
  `Birthday` bigint NOT NULL,
  `MedicalNumber` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `VisitNumber` varchar(100) COLLATE utf8mb4_bin DEFAULT NULL,
  `Sex` varchar(10) COLLATE utf8mb4_bin NOT NULL,
  `TypeOfPID` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `PatientIdentityRemoved` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `LastUpdate` bigint DEFAULT NULL,
  `CreateDateTime` bigint DEFAULT NULL,
  PRIMARY KEY (`PID`),
  UNIQUE KEY `PID_UNIQUE` (`PID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_imaging`
--

LOCK TABLES `patient_imaging` WRITE;
/*!40000 ALTER TABLE `patient_imaging` DISABLE KEYS */;
INSERT INTO `patient_imaging` VALUES (1,'b33d1307-10f2-4c62-a45c-69e5114cd314','John','Doe',1,0,0,3896499289397943000,'123-456-7890',NULL,'',NULL,NULL,3896499289408913100,0),(2,'c5f8a6cd-304e-498a-9d4c-856e9b2285ad','John','Doe',1,0,0,3896503767553289800,'5797',NULL,'',NULL,NULL,3896503767559274500,0),(3,'51d4f816-5243-4c74-8d66-77690b9921f5','John','Doe',1,0,0,3896690104236863700,'5555',NULL,'',NULL,NULL,3896690104250892400,0),(4,'0af2aba0-2754-41ee-ab22-e6875ac0f35c','John','Doe',1,0,0,3896845324478320200,'101-001',NULL,'',NULL,NULL,3896845324485406600,0),(5,'80c666a5-8385-462a-8a4b-2f99bf628cbe','John','Doe',1,0,0,3896850732503855000,'101-002',NULL,'',NULL,NULL,3896850732519335900,0),(6,'731f8de7-beac-40e9-9280-85a461134297','John','Doe',1,0,0,3897107143506211300,'101-003',NULL,'',NULL,NULL,3897107143521832100,0),(7,'478f2354-3988-4a7f-bada-084f9b05a614','John','Doe',1,0,0,3897383343461340300,'101-004',NULL,'',NULL,NULL,3897383343467323000,0),(8,'1cec852c-4f94-4463-8307-72deaa2272fd','John','Doe',1,0,0,3897798841998041500,'101-005',NULL,'',NULL,NULL,3897798841998041500,0),(9,'76d5c7e0-097f-4058-a4d5-c6dade6fad6f','John','Doe',1,0,0,3899424241693353500,'101-006',NULL,'',NULL,NULL,3899424241700382700,0);
/*!40000 ALTER TABLE `patient_imaging` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wounds_imaging`
--

DROP TABLE IF EXISTS `wounds_imaging`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wounds_imaging` (
  `PID` int NOT NULL,
  `WOUNDID` int NOT NULL,
  `AnatomicalLocation` varchar(100) NOT NULL,
  `CreateDateTime` bigint NOT NULL,
  PRIMARY KEY (`PID`,`WOUNDID`),
  UNIQUE KEY `WOUNDID_UNIQUE` (`WOUNDID`),
  CONSTRAINT `fk_PID` FOREIGN KEY (`PID`) REFERENCES `patient_imaging` (`PID`) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wounds_imaging`
--

LOCK TABLES `wounds_imaging` WRITE;
/*!40000 ALTER TABLE `wounds_imaging` DISABLE KEYS */;
INSERT INTO `wounds_imaging` VALUES (1,1,'Ant.R.U.Trunk_Medial',3896499302216272400),(3,2,'Ant.Head_Medial',3896690118559572300),(4,3,'Ant.R.L.Arm_Lateral',3896847604636656000),(4,4,'Ant.L.U.Arm_Lateral',3896847681750641000),(4,5,'Ant.L.L.Arm_Lateral',3896847759728129700),(4,6,'Ant.L.L.Arm_Medial',3896847860051511300),(5,7,'Post.L.L.Trunk_Superior',3896925075993883100),(5,8,'Ant.L.U.Trunk_Superior',3896925195690462200),(6,9,'Ant.R.L.Arm_Proximal',3897107355650375500),(6,10,'Ant.R.Leg_Lateral',3897107447075043500),(6,11,'Ant.R.Leg_Medial',3897107554050569200),(7,12,'Ant.R.Leg_Lateral',3897383385299551600),(7,13,'Ant.R.Leg_Medial',3897383482103404700),(8,14,'Ant.L.U.Trunk_Medial',3897798873880479900),(8,15,'Ant.R.L.Arm_Distal',3897799051250516800),(9,16,'Post.R.U.Trunk_Lateral',3899426649050787700),(9,17,'Post.R.U.Arm_Lateral',3899426759485709200),(9,18,'Post.R.Thigh_Lateral',3899426809716624800),(9,19,'Post.R.Leg_Lateral',3899426859844167200);
/*!40000 ALTER TABLE `wounds_imaging` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-27  8:05:41
