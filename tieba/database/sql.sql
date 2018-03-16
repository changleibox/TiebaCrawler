DROP DATABASE IF EXISTS tieba_crawler;

CREATE DATABASE IF NOT EXISTS tieba_crawler
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE tieba_crawler;

SET NAMES utf8mb4;

DROP TABLE IF EXISTS Forum;

CREATE TABLE Forum (
  fid       VARCHAR(100) NOT NULL,
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

DROP TABLE IF EXISTS Note;

CREATE TABLE Note (
  fid       VARCHAR(100) NOT NULL
  COMMENT '贴吧id',
  id        VARCHAR(100) NOT NULL
  COMMENT '帖子id',
  kw        LONGTEXT     NOT NULL
  COMMENT '贴吧名字',
  tbs       LONGTEXT     NOT NULL,
  title     LONGTEXT     NOT NULL,
  content   LONGTEXT     NOT NULL,
  timestamp LONG         NOT NULL
  COMMENT '爬虫更新时间',
  PRIMARY KEY (id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

DROP TABLE IF EXISTS Reply;

CREATE TABLE Reply (
  fid       VARCHAR(100) NOT NULL
  COMMENT '贴吧id',
  id        INT UNSIGNED AUTO_INCREMENT
  COMMENT '评论id',
  tid       VARCHAR(100) NOT NULL
  COMMENT '帖子id',
  kw        LONGTEXT     NOT NULL
  COMMENT '贴吧名字',
  tbs       LONGTEXT     NOT NULL,
  content   LONGTEXT     NOT NULL,
  timestamp LONG         NOT NULL
  COMMENT '爬虫更新时间',
  PRIMARY KEY (id)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_general_ci;

