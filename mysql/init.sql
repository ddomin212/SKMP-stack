CREATE USER 'dbadmin'@'%' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON *.* TO 'dbadmin'@'%' WITH GRANT OPTION;

CREATE DATABASE IF NOT EXISTS weather;

USE weather;

CREATE TABLE IF NOT EXISTS data (
    id INT NOT NULL AUTO_INCREMENT,
    CityName VARCHAR(255),
    Temperature DOUBLE,
    Humidity INT,
    CreationTime DATETIME,
    PRIMARY KEY (id)
);