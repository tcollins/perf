
DROP TABLE IF EXISTS `daily_summary`;
CREATE TABLE `daily_summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formattedcreated` datetime NOT NULL,
  `app` varchar(40) NOT NULL,
  `method` varchar(200) NOT NULL,
  `callcount` int(11) NOT NULL,
  `totalduration` int(11) NOT NULL,
  `avgduration` int(11) NOT NULL,
  `minduration` int(11) NOT NULL,
  `maxduration` int(11) NOT NULL,
  `stdev` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_daily_summary_method` (`method`),
  KEY `ix_daily_summary_formattedcreated` (`formattedcreated`),
  KEY `ix_daily_summary_callcount` (`callcount`),
  KEY `ix_daily_summary_avgduration` (`avgduration`),
  KEY `ix_daily_summary_app` (`app`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `monthly_summary`;
CREATE TABLE `monthly_summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formattedcreated` datetime NOT NULL,
  `app` varchar(40) NOT NULL,
  `method` varchar(200) NOT NULL,
  `callcount` int(11) NOT NULL,
  `totalduration` int(11) NOT NULL,
  `avgduration` int(11) NOT NULL,
  `minduration` int(11) NOT NULL,
  `maxduration` int(11) NOT NULL,
  `stdev` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_monthly_summary_avgduration` (`avgduration`),
  KEY `ix_monthly_summary_method` (`method`),
  KEY `ix_monthly_summary_formattedcreated` (`formattedcreated`),
  KEY `ix_monthly_summary_callcount` (`callcount`),
  KEY `ix_monthly_summary_app` (`app`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


DROP TABLE IF EXISTS `rawlog`;
CREATE TABLE `rawlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `duration` int(11) NOT NULL,
  `app` varchar(40) NOT NULL,
  `method` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `rawlog_unique_index` (`created`,`duration`,`app`,`method`),
  KEY `ix_rawlog_method` (`method`),
  KEY `ix_rawlog_app` (`app`)
) ENGINE=InnoDB AUTO_INCREMENT=187438 DEFAULT CHARSET=latin1;
