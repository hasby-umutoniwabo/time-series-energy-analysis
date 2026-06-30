-- ============================================================
-- AEP Hourly Energy Consumption Database Schema
-- Database: MySQL
-- Description: Stores hourly energy consumption readings
--              with time dimension and region information
-- ============================================================

CREATE DATABASE IF NOT EXISTS energy_consumption;
USE energy_consumption;

-- ------------------------------------------------------------
-- Table 1: regions
-- Stores the energy region information
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS regions (
    region_id   INT AUTO_INCREMENT PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL,
    country     VARCHAR(50) NOT NULL DEFAULT 'USA',
    timezone    VARCHAR(50) NOT NULL DEFAULT 'US/Eastern',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- Table 2: time_dimension
-- Breaks down each timestamp into useful time components
-- This makes time based queries faster and simpler
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS time_dimension (
    time_id     INT AUTO_INCREMENT PRIMARY KEY,
    datetime    DATETIME NOT NULL UNIQUE,
    hour        TINYINT NOT NULL,
    day         TINYINT NOT NULL,
    month       TINYINT NOT NULL,
    year        SMALLINT NOT NULL,
    day_of_week TINYINT NOT NULL,
    season      VARCHAR(10) NOT NULL,
    is_weekend  BOOLEAN NOT NULL
);

-- ------------------------------------------------------------
-- Table 3: energy_readings
-- Stores the actual hourly energy consumption readings
-- Links to both regions and time_dimension tables
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS energy_readings (
    reading_id  INT AUTO_INCREMENT PRIMARY KEY,
    region_id   INT NOT NULL,
    time_id     INT NOT NULL,
    consumption DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions(region_id),
    FOREIGN KEY (time_id)   REFERENCES time_dimension(time_id)
);

-- ============================================================
-- Sample Data Inserts
-- ============================================================

INSERT INTO regions (region_name, country, timezone) VALUES
('AEP', 'USA', 'US/Eastern');

INSERT INTO time_dimension (datetime, hour, day, month, year, day_of_week, season, is_weekend) VALUES
('2004-10-01 01:00:00', 1,  1, 10, 2004, 4, 'Autumn', FALSE),
('2004-10-01 02:00:00', 2,  1, 10, 2004, 4, 'Autumn', FALSE),
('2004-10-01 03:00:00', 3,  1, 10, 2004, 4, 'Autumn', FALSE),
('2004-10-01 04:00:00', 4,  1, 10, 2004, 4, 'Autumn', FALSE),
('2004-10-01 05:00:00', 5,  1, 10, 2004, 4, 'Autumn', FALSE);

INSERT INTO energy_readings (region_id, time_id, consumption) VALUES
(1, 1, 12379.00),
(1, 2, 11935.00),
(1, 3, 11692.00),
(1, 4, 11597.00),
(1, 5, 11681.00);

-- ============================================================
-- Queries
-- ============================================================

-- Query 1: Average energy consumption per season
SELECT t.season,
       ROUND(AVG(e.consumption), 2) AS avg_consumption_mw
FROM energy_readings e
JOIN time_dimension t ON e.time_id = t.time_id
GROUP BY t.season
ORDER BY avg_consumption_mw DESC;

-- Query 2: Get the highest consumption hours of the day
SELECT t.hour,
       ROUND(AVG(e.consumption), 2) AS avg_consumption_mw
FROM energy_readings e
JOIN time_dimension t ON e.time_id = t.time_id
GROUP BY t.hour
ORDER BY avg_consumption_mw DESC
LIMIT 5;

-- Query 3: Total consumption per year
SELECT t.year,
       ROUND(SUM(e.consumption), 2) AS total_consumption_mw
FROM energy_readings e
JOIN time_dimension t ON e.time_id = t.time_id
GROUP BY t.year
ORDER BY t.year ASC;

