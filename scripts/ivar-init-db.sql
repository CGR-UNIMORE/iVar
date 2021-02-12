-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Oct 26, 2020 at 06:26 PM
-- Server version: 10.3.18-MariaDB-1:10.3.18+maria~bionic-log
-- PHP Version: 7.2.24-0ubuntu0.18.04.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ivar`
--
CREATE DATABASE IF NOT EXISTS `ivar` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ivar`;

-- --------------------------------------------------------

--
-- Table structure for table `ANNOTATION_FILE`
--

CREATE TABLE `ANNOTATION_FILE` (
  `id` int(11) NOT NULL,
  `file_upload` varchar(512) DEFAULT NULL,
  `filename_upload` varchar(200) DEFAULT '',
  `date_upload` datetime DEFAULT NULL,
  `fl_elaborated` varchar(1) DEFAULT NULL,
  `ANNOTATION_TYPE_id` int(11) DEFAULT NULL,
  `date_valid_from` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `ANNOTATION_TYPE`
--

CREATE TABLE `ANNOTATION_TYPE` (
  `id` int(11) NOT NULL,
  `name_type` varchar(50) DEFAULT '',
  `variant_attribute` longtext DEFAULT '',
  `gene` varchar(10) DEFAULT '',
  `variant_hg19` varchar(50) DEFAULT '',
  `variant_hg38` varchar(50) DEFAULT '',
  `classif_eval` longtext DEFAULT '',
  `break_condition` longtext DEFAULT '',
  `row_filter` longtext DEFAULT '',
  `classif_valid_from` varchar(100) DEFAULT NULL,
  `char_sep` varchar(2) DEFAULT NULL,
  `classif` varchar(50) DEFAULT NULL,
  `sample` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `PANEL`
--

CREATE TABLE `PANEL` (
  `id` int(11) NOT NULL,
  `name_panel` varchar(50) DEFAULT '',
  `gene` varchar(500) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `SAMPLE`
--

CREATE TABLE `SAMPLE` (
  `id` int(11) NOT NULL,
  `sample` varchar(50) CHARACTER SET utf8 DEFAULT '',
  `fl_sample_type` varchar(1) CHARACTER SET utf8 DEFAULT '',
  `TISSUE_TYPE_id` int(11) DEFAULT NULL,
  `fl_sex` varchar(1) CHARACTER SET utf8 DEFAULT '',
  `date_sample` date DEFAULT NULL,
  `VCF_FILE_ids` longtext CHARACTER SET utf8 DEFAULT NULL,
  `TEXT_FILE_ids` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SAMPLE_VARIANT`
--

CREATE TABLE `SAMPLE_VARIANT` (
  `id` int(11) NOT NULL,
  `SAMPLE_id` int(11) DEFAULT NULL,
  `VARIANT_id` int(11) DEFAULT NULL,
  `AF` varchar(20) CHARACTER SET utf8 DEFAULT '',
  `GT` varchar(20) CHARACTER SET utf8 DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `SAMPLE_VARIANT_ATTRIBUTE`
--

CREATE TABLE `SAMPLE_VARIANT_ATTRIBUTE` (
  `id` int(11) NOT NULL,
  `sample_variant_id` int(11) DEFAULT NULL,
  `attribute_name` varchar(250) DEFAULT '',
  `attribute_value` varchar(250) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `SEARCH_CRITERIA`
--

CREATE TABLE `SEARCH_CRITERIA` (
  `id` int(11) NOT NULL,
  `search_name` varchar(50) DEFAULT NULL,
  `variant` longtext DEFAULT NULL,
  `attribute` longtext DEFAULT NULL,
  `attribute_prev` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Table structure for table `TISSUE_TYPE`
--

CREATE TABLE `TISSUE_TYPE` (
  `id` int(11) NOT NULL,
  `tissue_type` varchar(50) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `VARIANT`
--

CREATE TABLE `VARIANT` (
  `id` int(11) NOT NULL,
  `gene` varchar(20) DEFAULT '',
  `note` longtext DEFAULT '',
  `classif` varchar(2) DEFAULT '',
  `id_hg19` varchar(500) DEFAULT '',
  `id_hg38` varchar(500) DEFAULT '',
  `last_check` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `VARIANT_ATTRIBUTE`
--

CREATE TABLE `VARIANT_ATTRIBUTE` (
  `id` int(11) NOT NULL,
  `VARIANT_id` int(11) DEFAULT NULL,
  `attribute_name` varchar(250) DEFAULT '',
  `valid_from` date DEFAULT NULL,
  `attribute_value` varchar(500) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_COUNT`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_COUNT` (
`id` int(11)
,`VARIANT_id` int(11)
,`attribute_name` varchar(250)
,`count` bigint(21)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_CURRENT`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_CURRENT` (
`id` int(11)
,`VARIANT_id` int(11)
,`attribute_name` varchar(250)
,`valid_from` date
,`attribute_value` varchar(500)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_PREV`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_PREV` (
`id` int(11)
,`VARIANT_ATTRIBUTE_id` int(11)
,`VARIANT_ATTRIBUTE_id_prev` int(11)
,`attribute_value_prev` varchar(500)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_PREV_ID`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_PREV_ID` (
`id` int(11)
,`VARIANT_ATTRIBUTE_id` int(11)
,`VARIANT_ATTRIBUTE_id_prev` int(11)
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_STORIC`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_STORIC` (
`id` int(11)
,`VARIANT_id` int(11)
,`attribute_name` varchar(250)
,`attribute_value` varchar(500)
,`valid_from` date
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `VARIANT_ATTRIBUTE_VALID`
-- (See below for the actual view)
--
CREATE TABLE `VARIANT_ATTRIBUTE_VALID` (
`id` int(11)
,`VARIANT_id` int(11)
,`attribute_name` varchar(250)
,`attribute_value` varchar(500)
,`valid_from` date
);

-- --------------------------------------------------------

--
-- Table structure for table `VCF_FILE`
--

CREATE TABLE `VCF_FILE` (
  `id` int(11) NOT NULL,
  `file_upload` varchar(512) DEFAULT NULL,
  `filename_upload` varchar(200) DEFAULT '',
  `date_upload` datetime DEFAULT NULL,
  `hg` varchar(10) DEFAULT '',
  `samples` longtext DEFAULT '',
  `fl_elaborated` varchar(1) DEFAULT '',
  `VCF_TYPE_id` int(11) DEFAULT NULL,
  `PANEL_id` int(11) DEFAULT NULL,
  `date_vcf` date DEFAULT NULL,
  `VIRTUAL_PANEL_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `VCF_TYPE`
--

CREATE TABLE `VCF_TYPE` (
  `id` int(11) NOT NULL,
  `name_type` varchar(50) DEFAULT NULL,
  `variant` varchar(50) DEFAULT NULL,
  `row_filter` longtext DEFAULT NULL,
  `sample_attribute` longtext DEFAULT NULL,
  `variant_attribute` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `VIRTUAL_PANEL`
--

CREATE TABLE `VIRTUAL_PANEL` (
  `id` int(11) NOT NULL,
  `name_virtual_panel` varchar(50) DEFAULT '',
  `gene` varchar(500) DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_cas`
--

CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_event`
--

CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_membership`
--

CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_COUNT`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_COUNT`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_COUNT`  AS  select max(`VARIANT_ATTRIBUTE`.`id`) AS `id`,`VARIANT_ATTRIBUTE`.`VARIANT_id` AS `VARIANT_id`,`VARIANT_ATTRIBUTE`.`attribute_name` AS `attribute_name`,count(0) AS `count` from `VARIANT_ATTRIBUTE` group by `VARIANT_ATTRIBUTE`.`VARIANT_id`,`VARIANT_ATTRIBUTE`.`attribute_name` ;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_CURRENT`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_CURRENT`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_CURRENT`  AS  select `a`.`id` AS `id`,`a`.`VARIANT_id` AS `VARIANT_id`,`a`.`attribute_name` AS `attribute_name`,`a`.`valid_from` AS `valid_from`,`a`.`attribute_value` AS `attribute_value` from `VARIANT_ATTRIBUTE` `a` where `a`.`id` = (select `b`.`id` from `VARIANT_ATTRIBUTE` `b` where `b`.`VARIANT_id` = `a`.`VARIANT_id` and `b`.`attribute_name` = `a`.`attribute_name` order by `b`.`valid_from` desc limit 1) ;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_PREV`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_PREV`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_PREV`  AS  select `id`.`id` AS `id`,`id`.`VARIANT_ATTRIBUTE_id` AS `VARIANT_ATTRIBUTE_id`,`id`.`VARIANT_ATTRIBUTE_id_prev` AS `VARIANT_ATTRIBUTE_id_prev`,`p`.`attribute_value` AS `attribute_value_prev` from (`VARIANT_ATTRIBUTE_PREV_ID` `id` left join `VARIANT_ATTRIBUTE` `p` on(`id`.`VARIANT_ATTRIBUTE_id_prev` = `p`.`id`)) ;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_PREV_ID`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_PREV_ID`;

CREATE ALGORITHM=MERGE DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_PREV_ID`  AS  select `a`.`id` AS `id`,`a`.`id` AS `VARIANT_ATTRIBUTE_id`,(select `p`.`id` from `VARIANT_ATTRIBUTE` `p` where `p`.`VARIANT_id` = `a`.`VARIANT_id` and `p`.`attribute_name` = `a`.`attribute_name` and `p`.`valid_from` < `a`.`valid_from` order by `p`.`VARIANT_id`,`p`.`attribute_name`,`p`.`valid_from` desc limit 1) AS `VARIANT_ATTRIBUTE_id_prev` from `VARIANT_ATTRIBUTE` `a` ;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_STORIC`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_STORIC`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_STORIC`  AS  select `a`.`id` AS `id`,`a`.`VARIANT_id` AS `VARIANT_id`,`a`.`attribute_name` AS `attribute_name`,`a`.`attribute_value` AS `attribute_value`,`a`.`valid_from` AS `valid_from` from `VARIANT_ATTRIBUTE` `a` where `a`.`valid_from` <> (select max(`b`.`valid_from`) from `VARIANT_ATTRIBUTE` `b` where `a`.`VARIANT_id` = `b`.`VARIANT_id` and `a`.`attribute_name` = `b`.`attribute_name`) ;

-- --------------------------------------------------------

--
-- Structure for view `VARIANT_ATTRIBUTE_VALID`
--
DROP TABLE IF EXISTS `VARIANT_ATTRIBUTE_VALID`;

CREATE ALGORITHM=MERGE DEFINER=`ivar`@`localhost` SQL SECURITY DEFINER VIEW `VARIANT_ATTRIBUTE_VALID`  AS  select `a`.`id` AS `id`,`a`.`VARIANT_id` AS `VARIANT_id`,`a`.`attribute_name` AS `attribute_name`,`a`.`attribute_value` AS `attribute_value`,`a`.`valid_from` AS `valid_from` from `VARIANT_ATTRIBUTE` `a` where `a`.`valid_from` = (select max(`b`.`valid_from`) from `VARIANT_ATTRIBUTE` `b` where `a`.`VARIANT_id` = `b`.`VARIANT_id` and `a`.`attribute_name` = `b`.`attribute_name`) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ANNOTATION_FILE`
--
ALTER TABLE `ANNOTATION_FILE`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ANNOTATION_TYPE_id__idx` (`ANNOTATION_TYPE_id`);

--
-- Indexes for table `ANNOTATION_TYPE`
--
ALTER TABLE `ANNOTATION_TYPE`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `PANEL`
--
ALTER TABLE `PANEL`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `SAMPLE`
--
ALTER TABLE `SAMPLE`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sample_UNIQUE` (`sample`),
  ADD KEY `TISSUE_TYPE__fk_idx` (`TISSUE_TYPE_id`),
  ADD KEY `data_sample__idx` (`date_sample`,`sample`);

--
-- Indexes for table `SAMPLE_VARIANT`
--
ALTER TABLE `SAMPLE_VARIANT`
  ADD PRIMARY KEY (`id`),
  ADD KEY `VARIANT__fk_idx` (`VARIANT_id`),
  ADD KEY `SAMPLE__fk_idx` (`SAMPLE_id`);

--
-- Indexes for table `SAMPLE_VARIANT_ATTRIBUTE`
--
ALTER TABLE `SAMPLE_VARIANT_ATTRIBUTE`
  ADD PRIMARY KEY (`id`),
  ADD KEY `SAMPLE_VARIANT__fk_idx` (`sample_variant_id`);

--
-- Indexes for table `SEARCH_CRITERIA`
--
ALTER TABLE `SEARCH_CRITERIA`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `TISSUE_TYPE`
--
ALTER TABLE `TISSUE_TYPE`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `VARIANT`
--
ALTER TABLE `VARIANT`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `HG19_idx` (`id_hg19`,`id`),
  ADD KEY `CLASSIF_idx` (`classif`),
  ADD KEY `GENE_idx` (`gene`,`id_hg19`);

--
-- Indexes for table `VARIANT_ATTRIBUTE`
--
ALTER TABLE `VARIANT_ATTRIBUTE`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `VARIANT_id_attribute__idx` (`VARIANT_id`,`attribute_name`,`valid_from`,`id`),
  ADD UNIQUE KEY `valid_from__idx` (`valid_from`,`attribute_name`,`VARIANT_id`,`id`),
  ADD KEY `attribute_value__idx` (`attribute_value`,`attribute_name`,`VARIANT_id`),
  ADD KEY `attribute_name__idx` (`attribute_name`,`VARIANT_id`,`valid_from`);

--
-- Indexes for table `VCF_FILE`
--
ALTER TABLE `VCF_FILE`
  ADD PRIMARY KEY (`id`),
  ADD KEY `VCF_TYPE_id__idx` (`VCF_TYPE_id`),
  ADD KEY `PANEL_id__idx` (`PANEL_id`),
  ADD KEY `FILENAME_UPLOAD_idx` (`filename_upload`),
  ADD KEY `VIRTUAL_PANEL_id__idx` (`VIRTUAL_PANEL_id`);

--
-- Indexes for table `VCF_FILE_INFO`
--
ALTER TABLE `VCF_FILE_INFO`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `VCF_TYPE`
--
ALTER TABLE `VCF_TYPE`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `VIRTUAL_PANEL`
--
ALTER TABLE `VIRTUAL_PANEL`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_cas`
--
ALTER TABLE `auth_cas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id__idx` (`user_id`);

--
-- Indexes for table `auth_event`
--
ALTER TABLE `auth_event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id__idx` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `auth_membership`
--
ALTER TABLE `auth_membership`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id__idx` (`user_id`),
  ADD KEY `group_id__idx` (`group_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD KEY `group_id__idx` (`group_id`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ANNOTATION_FILE`
--
ALTER TABLE `ANNOTATION_FILE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `ANNOTATION_TYPE`
--
ALTER TABLE `ANNOTATION_TYPE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `PANEL`
--
ALTER TABLE `PANEL`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `SAMPLE`
--
ALTER TABLE `SAMPLE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `SAMPLE_VARIANT`
--
ALTER TABLE `SAMPLE_VARIANT`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `SAMPLE_VARIANT_ATTRIBUTE`
--
ALTER TABLE `SAMPLE_VARIANT_ATTRIBUTE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `SEARCH_CRITERIA`
--
ALTER TABLE `SEARCH_CRITERIA`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `TISSUE_TYPE`
--
ALTER TABLE `TISSUE_TYPE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `VARIANT`
--
ALTER TABLE `VARIANT`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `VARIANT_ATTRIBUTE`
--
ALTER TABLE `VARIANT_ATTRIBUTE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `VCF_FILE`
--
ALTER TABLE `VCF_FILE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `VCF_FILE_INFO`
--
ALTER TABLE `VCF_FILE_INFO`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Tabella contenente le info dei VCF caricati massivamente per recuperare il pregresso. Contengono le info, come il pannello, utili per l’elaborazione. E’ una tabella usata una volta, ma conservata per eventuali controlli successivi al recupero massivo';
--
-- AUTO_INCREMENT for table `VCF_TYPE`
--
ALTER TABLE `VCF_TYPE`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `VIRTUAL_PANEL`
--
ALTER TABLE `VIRTUAL_PANEL`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_cas`
--
ALTER TABLE `auth_cas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_event`
--
ALTER TABLE `auth_event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_membership`
--
ALTER TABLE `auth_membership`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `ANNOTATION_FILE`
--
ALTER TABLE `ANNOTATION_FILE`
  ADD CONSTRAINT `ANNOTATION_FILE_ibfk_1` FOREIGN KEY (`ANNOTATION_TYPE_id`) REFERENCES `ANNOTATION_TYPE` (`id`) ON UPDATE CASCADE;

--
-- Constraints for table `SAMPLE`
--
ALTER TABLE `SAMPLE`
  ADD CONSTRAINT `TISSUE_TYPE__fk` FOREIGN KEY (`TISSUE_TYPE_id`) REFERENCES `TISSUE_TYPE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `SAMPLE_VARIANT`
--
ALTER TABLE `SAMPLE_VARIANT`
  ADD CONSTRAINT `SAMPLE__fk` FOREIGN KEY (`SAMPLE_id`) REFERENCES `SAMPLE` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `VARIANT__fk` FOREIGN KEY (`VARIANT_id`) REFERENCES `VARIANT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `SAMPLE_VARIANT_ATTRIBUTE`
--
ALTER TABLE `SAMPLE_VARIANT_ATTRIBUTE`
  ADD CONSTRAINT `SAMPLE_VARIANT__fk` FOREIGN KEY (`sample_variant_id`) REFERENCES `SAMPLE_VARIANT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `VARIANT_ATTRIBUTE`
--
ALTER TABLE `VARIANT_ATTRIBUTE`
  ADD CONSTRAINT `VARIANT_ATTRIBUTE_VARIANT__fk` FOREIGN KEY (`VARIANT_id`) REFERENCES `VARIANT` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `VCF_FILE`
--
ALTER TABLE `VCF_FILE`
  ADD CONSTRAINT `VCF_FILE_ibfk_1` FOREIGN KEY (`VIRTUAL_PANEL_id`) REFERENCES `VIRTUAL_PANEL` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_cas`
--
ALTER TABLE `auth_cas`
  ADD CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_event`
--
ALTER TABLE `auth_event`
  ADD CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_membership`
--
ALTER TABLE `auth_membership`
  ADD CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE;

--
-- Default Data
--
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

INSERT INTO `auth_group` (`id`, `role`, `description`) VALUES
(1, '-- initial group --', 'Default group for new user.'),
(2, 'Admin', 'Superuser'),
(3, 'Consultation only', NULL),
(4, 'User manager', NULL);

INSERT INTO `auth_permission` (`id`, `group_id`, `name`, `table_name`, `record_id`) VALUES
(1, 2, 'ADMIN', '', 0),
(2, 2, 'import', 'VCF', 0),
(3, 2, 'view', 'VARIANT', 0),
(4, 2, 'manage', 'VARIANT', 0),
(5, 2, 'delete', 'VARIANT', 0),
(6, 2, 'view', 'SAMPLE', 0),
(7, 2, 'manage', 'SAMPLE', 0),
(8, 2, 'delete', 'SAMPLE', 0),
(9, 2, 'manage', 'VCF', 0),
(10, 2, 'delete', 'VCF', 0),
(11, 2, 'view', 'VCF', 0),
(12, 2, 'view', 'ANNOTATION', 0),
(13, 2, 'manage', 'ANNOTATION', 0),
(14, 2, 'delete', 'ANNOTATION', 0),
(15, 2, 'import', 'ANNOTATION', 0),
(16, 2, 'view', 'SAMPLE_VARIANT', 0),
(17, 2, 'manage', 'SAMPLE_VARIANT', 0),
(18, 2, 'delete', 'SAMPLE_VARIANT', 0),
(19, 3, 'view', 'VARIANT', 0),
(20, 3, 'view', 'SAMPLE', 0),
(21, 3, 'view', 'ANNOTATION', 0),
(22, 3, 'view', 'VCF', 0),
(23, 3, 'view', 'SAMPLE_VARIANT', 0),
(24, 4, 'ADMIN', '', 0);

INSERT INTO `auth_user` (`id`, `first_name`, `last_name`, `email`, `password`, `registration_key`, `reset_password_key`, `registration_id`) VALUES
(1, 'admin', 'admin', 'admin@example.com', 'pbkdf2(1000,20,sha512)$8019bb957fd23180$098b1204be652d4ee6f52e7a0a65037c0ff8d601', '', '', '');

INSERT INTO `auth_membership` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 2);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

