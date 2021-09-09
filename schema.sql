DROP TABLE IF EXISTS `tles`;

CREATE TABLE `tles` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `tle` varchar(255) UNIQUE NOT NULL,
  `sat_id` int,
  `sat_name` varchar(255),
  `norad_id` int,
  `classification` varchar(255),
  `international_id` varchar(255),
  `epoch` timestamp(3),
  `epoch_year` int,
  `epoch_day` DOUBLE,
  `first_deriv_mm` DOUBLE,
  `second_deriv_mm` DOUBLE,
  `drag` DOUBLE,
  `type` int,
  `element_num` int,
  `inclination` DOUBLE,
  `ra_node` DOUBLE,
  `eccentricity` DOUBLE,
  `arg_perigee` DOUBLE,
  `mean_anomaly` DOUBLE,
  `mean_motion` DOUBLE,
  `revolution_num` int,
  `source` varchar(255),
  FOREIGN KEY (`sat_id`) REFERENCES `sats` (`id`),
  FOREIGN KEY (`id`) REFERENCES `targets` (`tle_id`)
);

DROP TABLE IF EXISTS `sats`;

CREATE TABLE `sats` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `norad_id` int UNIQUE,
  `international_id` varchar(255),
  `name` varchar(255),
  `type` varchar(255),
  `launch` timestamp,
  `deorbited` boolean
);

DROP TABLE IF EXISTS `images`;

CREATE TABLE `images` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `imageFile` varchar(255) UNIQUE NOT NULL,
  `msb_title` varchar(255),
  `telescope` varchar(255),
  `instrument` varchar(255),
  `target` varchar(255),
  `type` varchar(255),
  `start_time` timestamp(3),
  `end_time` timestamp(3),
  `exposure` DOUBLE,
  `filter` varchar(255),
  `sensor_temp` DOUBLE,
  `air_temp` DOUBLE,
  `gain` DOUBLE,
  `n_reads` int,
  `read_mode` varchar(255),
  `focus` DOUBLE,
  `tel_ra` DOUBLE,
  `tel_dec` DOUBLE,
  `ra_rate` DOUBLE,
  `dec_rate` DOUBLE,
  `airmass` DOUBLE,
  `darkFile` varchar(255),
  `flatFile` varchar(255),
  `reduced` timestamp(3),
  `astrometry` timestamp(3),
  `pp_aperture` DOUBLE,
  FOREIGN KEY (`id`) REFERENCES `referenceStars` (`image_id`),
  FOREIGN KEY (`id`) REFERENCES `targets` (`image_id`)
);

DROP TABLE IF EXISTS `referenceStars`;

CREATE TABLE `referenceStars` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `image_id` int UNIQUE NOT NULL,
  `photometric_catalog` varchar(255),
  `ra` DOUBLE,
  `decl` DOUBLE,
  `alt` DOUBLE,
  `az` DOUBLE,
  `airmass` DOUBLE,
  `inst_mag` DOUBLE,
  `inst_mag_error` DOUBLE,
  `magnitude` DOUBLE,
  `magnitude_error` DOUBLE,
  `zeropoint` DOUBLE,
  `zeropoint_error` DOUBLE,
  `fwhm` DOUBLE,
  `sextractor` int,
  `rejected` boolean
);

DROP TABLE IF EXISTS `referenceStarMatching`;

CREATE TABLE `referenceStarMatching` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `ref_star_id` int NOT NULL,
  `target_id` int NOT NULL,
  FOREIGN KEY (`ref_star_id`) REFERENCES `referenceStars` (`id`),
  FOREIGN KEY (`target_id`) REFERENCES `targets` (`id`)
);

DROP TABLE IF EXISTS `targets`;

CREATE TABLE `targets` (
  `id` INTEGER PRIMARY KEY NOT NULL,
  `target_id` int,
  `image_id` int NOT NULL,
  `ref_star_match_id` int,
  `pp_aperture` DOUBLE,
  `ra` DOUBLE,
  `decl` DOUBLE,
  `inst_mag` DOUBLE,
  `inst_mag_error` DOUBLE,
  `zeropoint` DOUBLE,
  `zeropoint_error` DOUBLE,
  `magnitude` DOUBLE,
  `magnitude_error` DOUBLE,
  `fwhm` DOUBLE,
  `tle_id` int,
  `tle_age` DOUBLE,
  `ra_predicted` DOUBLE,
  `decl_predicted` DOUBLE,
  `ra_error` DOUBLE,
  `decl_error` DOUBLE,
  `pointing_error` DOUBLE,
  `ra_rate_predicted` DOUBLE,
  `decl_rate_predicted` DOUBLE,
  `velocity_predicted` DOUBLE,
  `alt_predicted` DOUBLE,
  `az_predicted` DOUBLE,
  `lat_predicted` DOUBLE,
  `lon_predicted` DOUBLE,
  `airmass_predicted` DOUBLE,
  `orbit_height_predicted` DOUBLE,
  `range_predicted` DOUBLE,
  `sun_elong_predicted` DOUBLE,
  `eclipsed` boolean,
  `sextractor` int,
  `rejected` boolean,
  FOREIGN KEY (`target_id`) REFERENCES `sats` (`id`)
);

-- ALTER TABLE `tles` ADD FOREIGN KEY (`sat_id`) REFERENCES `sats` (`id`);

-- ALTER TABLE `images` ADD FOREIGN KEY (`id`) REFERENCES `referenceStars` (`image_id`);

-- ALTER TABLE `targets` ADD FOREIGN KEY (`target_id`) REFERENCES `sats` (`id`);

-- ALTER TABLE `images` ADD FOREIGN KEY (`id`) REFERENCES `targets` (`image_id`);

-- ALTER TABLE `tles` ADD FOREIGN KEY (`id`) REFERENCES `targets` (`tle_id`);

-- ALTER TABLE `referenceStarMatching` ADD FOREIGN KEY (`ref_star_id`) REFERENCES `referenceStars` (`id`);

-- ALTER TABLE `referenceStarMatching` ADD FOREIGN KEY (`target_id`) REFERENCES `targets` (`id`);
