DROP DATABASE IF EXISTS TiebaCrawler;

CREATE DATABASE IF NOT EXISTS TiebaCrawler
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE TiebaCrawler;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS Forum;

CREATE TABLE Forum (
  fid       INT UNSIGNED NOT NULL,
  tbs       LONGTEXT     NOT NULL,
  exper     LONGTEXT     NOT NULL,
  href      LONGTEXT     NOT NULL,
  title     LONGTEXT     NOT NULL,
  timestamp LONG         NOT NULL
  COMMENT '爬虫更新时间',
  PRIMARY KEY (fid)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;