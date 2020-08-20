CREATE SCHEMA system;
CREATE SCHEMA company;
CREATE SCHEMA mente;


CREATE EXTENSION pgcrypto;
DROP TABLE IF EXISTS system.company_api_rel;
DROP SEQUENCE IF EXISTS system.api_id_seq CASCADE;
DROP TABLE IF EXISTS system.api_info;
DROP SEQUENCE IF EXISTS company.users_id_seq CASCADE;
DROP TABLE IF EXISTS company.users_info;
DROP SEQUENCE IF EXISTS company.group_id_seq CASCADE;
DROP TABLE IF EXISTS company.group_info;
DROP SEQUENCE IF EXISTS company.company_id_seq CASCADE;
DROP TABLE IF EXISTS company.company_info;
DROP TABLE IF EXISTS company.company_basic_session_info;
DROP SEQUENCE IF EXISTS system.server_id_seq CASCADE;
DROP TABLE IF EXISTS system.server_info;

CREATE SEQUENCE company.company_id_seq;
CREATE TABLE company.company_info (
  company_id INTEGER NOT NULL DEFAULT nextval('company.company_id_seq'::regclass),
  company_name varchar(80) NOT NULL DEFAULT '',
  company_post varchar(8) DEFAULT NULL,
  company_city INTEGER DEFAULT NULL,
  company_address varchar(150) DEFAULT NULL,
  company_address_kana varchar(200) DEFAULT NULL,
  company_logo varchar(150) DEFAULT NULL,
  company_home_page varchar(150) DEFAULT NULL,
  company_copy_right varchar(150) DEFAULT NULL,
  company_global_ip varchar(120) DEFAULT NULL,
  company_cti_flag SMALLINT NOT NULL DEFAULT 0,
  company_memo varchar(500) DEFAULT NULL,
  company_global_locale SMALLINT DEFAULT NULL,
  company_theme varchar(15) DEFAULT NULL,
  company_basic_login_id varchar(30) NOT NULL,
  company_basic_password varchar(70) NOT NULL,
  company_use_system_auth SMALLINT NOT NULL DEFAULT 0,
  company_use_api SMALLINT DEFAULT 0,
  company_start_use_date DATE NULL,
  company_deleted SMALLINT DEFAULT 0,
  updated_id INTEGER DEFAULT NULL,
  updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_company_id PRIMARY KEY (company_id),
  CONSTRAINT un_company_basic_login_id UNIQUE (company_basic_login_id)
);
COMMENT ON TABLE company.company_info IS '会社情報';
COMMENT ON COLUMN company.company_info.company_id IS '会社ID';
COMMENT ON COLUMN company.company_info.company_name IS '会社名';
COMMENT ON COLUMN company.company_info.company_post IS '郵便番号';
COMMENT ON COLUMN company.company_info.company_city IS '都道府県';
COMMENT ON COLUMN company.company_info.company_address IS '住所';
COMMENT ON COLUMN company.company_info.company_address_kana IS '住所カナ';
COMMENT ON COLUMN company.company_info.company_logo IS 'ロゴ';
COMMENT ON COLUMN company.company_info.company_home_page IS 'ホームページ';
COMMENT ON COLUMN company.company_info.company_copy_right IS 'Copyright';
COMMENT ON COLUMN company.company_info.company_global_ip IS '会社グロバールIP';
COMMENT ON COLUMN company.company_info.company_memo IS 'メモ';
COMMENT ON COLUMN company.company_info.company_global_locale IS '１は他言語使用可能';
COMMENT ON COLUMN company.company_info.company_basic_login_id IS 'Basic認証ID';
COMMENT ON COLUMN company.company_info.company_basic_password IS 'Basic認証パスワード';
COMMENT ON COLUMN company.company_info.company_use_system_auth IS '０はログイン、１は顔認証、２はQRコード認証、３はOneTimePassword使用';
COMMENT ON COLUMN company.company_info.company_use_api IS 'API使用フラグ';
COMMENT ON COLUMN company.company_info.company_start_use_date IS '使用開始日';
COMMENT ON COLUMN company.company_info.company_deleted IS '存在フラグ、１は削除';
COMMENT ON COLUMN company.company_info.updated_id IS '更新者';
COMMENT ON COLUMN company.company_info.updated_time IS '更新日';

INSERT INTO company.company_info (
  company_id, company_name, company_basic_login_id, company_basic_password, company_use_api
) VALUES (
  nextval('company.company_id_seq'::regclass), '管理会社', 'admin', ENCODE(DIGEST('admin', 'sha256'), 'hex'), 2
);

CREATE TABLE company.company_basic_session_info (
  company_basic_login_id VARCHAR(90) NOT NULL,
  company_basic_session_key VARCHAR(90) NOT NULL,
  company_basic_date DATE NOT NULL DEFAULT DATE(TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD')),
  CONSTRAINT pk_session_company_basic_login_id PRIMARY KEY (company_basic_login_id, company_basic_session_key)
);
COMMENT ON TABLE company.company_basic_session_info IS '会社Basicセクション情報';
COMMENT ON COLUMN company.company_basic_session_info.company_basic_login_id IS '会社BasicID';
COMMENT ON COLUMN company.company_basic_session_info.company_basic_session_key IS 'Basicセクションキー';

CREATE SEQUENCE company.group_id_seq;
CREATE TABLE company.group_info (
  group_id INTEGER NOT NULL DEFAULT nextval('company.group_id_seq'::regclass),
  group_name varchar(45) NOT NULL DEFAULT '',
  group_code varchar(45) NOT NULL DEFAULT '',
  group_parent_id INTEGER DEFAULT NULL,
  group_tree_id varchar(500) DEFAULT NULL,
  group_order INTEGER DEFAULT NULL,
  group_memo varchar(500) DEFAULT NULL,
  group_deleted SMALLINT DEFAULT 0,
  company_id INTEGER NOT NULL DEFAULT 0,
  -- created_id INTEGER DEFAULT NULL COMMENT '作成者',
  -- created_time timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日',
  updated_id INTEGER DEFAULT NULL,
  updated_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_group_id PRIMARY KEY (group_id),
  CONSTRAINT un_group_name_code UNIQUE (group_name, group_code),
  CONSTRAINT fk_group_info_company_id FOREIGN KEY (company_id) REFERENCES company.company_info(company_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE INDEX idx_group_tree_id ON company.group_info (group_tree_id);
COMMENT ON TABLE company.group_info IS '部署情報（グループ）';
COMMENT ON COLUMN company.group_info.group_id IS '部署ID';
COMMENT ON COLUMN company.group_info.group_name IS '部署名';
COMMENT ON COLUMN company.group_info.group_code IS '部署コード';
COMMENT ON COLUMN company.group_info.group_parent_id IS '親ID';
COMMENT ON COLUMN company.group_info.group_tree_id IS '部署ツリー';
COMMENT ON COLUMN company.group_info.group_order IS '表示順';
COMMENT ON COLUMN company.group_info.group_memo IS 'メモ';
COMMENT ON COLUMN company.group_info.group_deleted IS '存在フラグ、１は削除';
COMMENT ON COLUMN company.group_info.company_id IS '会社ID';
COMMENT ON COLUMN company.group_info.company_id IS '更新者';
COMMENT ON COLUMN company.group_info.company_id IS '更新日';

INSERT INTO company.group_info (
  group_id, group_name, group_code, company_id
) VALUES (
  nextval('company.group_id_seq'::regclass), '管理グールブ', 'ADMIN_CODE', 1
);

CREATE SEQUENCE system.api_id_seq;
CREATE TABLE system.api_info (
  api_id INTEGER NOT NULL DEFAULT nextval('system.api_id_seq'::regclass),
  -- api_key VARCHAR(80) NOT NULL DEFAULT UPPER(ENCODE(DIGEST(TO_CHAR(CURRENT_TIMESTAMP, 'YYYY-DD-MM HH24:MI:SS'), 'sha256'), 'hex')),
  api_name VARCHAR(80) NOT NULL DEFAULT '',
  api_start_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  api_expiration_date TIMESTAMP,
  api_deleted SMALLINT DEFAULT 1,
  company_id INT NOT NULL DEFAULT 0,
  CONSTRAINT pk_api_id PRIMARY KEY (api_id),
  -- CONSTRAINT un_api_key UNIQUE (api_key),
  CONSTRAINT fk_api_info_api_id FOREIGN KEY (company_id) REFERENCES company.company_info(company_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE system.api_info IS 'API情報';
COMMENT ON COLUMN system.api_info.api_id IS 'APIID';
COMMENT ON COLUMN system.api_info.api_name IS 'API名';
--COMMENT ON COLUMN system.api_info.api_key IS 'APIキー';
COMMENT ON COLUMN system.api_info.company_id IS '会社ID';
COMMENT ON COLUMN system.api_info.api_deleted IS '削除フラグ０は有効';

CREATE TABLE system.company_api_rel (
  company_id INTEGER NOT NULL,
  api_id INTEGER NOT NULL,
  CONSTRAINT un_company_api_rel_id UNIQUE (company_id, api_id),
  CONSTRAINT fk_company_api_rel_company_id FOREIGN KEY (company_id) REFERENCES company.company_info(company_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT fk_company_api_rel_api_id FOREIGN KEY (company_id) REFERENCES system.api_info(api_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE SEQUENCE company.user_id_seq;
CREATE TABLE company.users_info (
  user_id INTEGER NOT NULL DEFAULT nextval('company.user_id_seq'::regclass),
  user_code varchar(30) DEFAULT NULL,
  user_login_id varchar(50) NOT NULL DEFAULT '',
  user_password varchar(70) NOT NULL DEFAULT '',
  user_name_first varchar(70) NOT NULL DEFAULT '',
  user_name_last varchar(70) NOT NULL DEFAULT '',
  user_kana_first varchar(70) DEFAULT NULL,
  user_kana_last varchar(70) DEFAULT NULL,
  user_post varchar(8) DEFAULT '',
  user_city INTEGER DEFAULT NULL,
  user_address varchar(150) DEFAULT NULL,
  user_address_kana varchar(200) DEFAULT NULL,
  user_image varchar(150) DEFAULT NULL,
  user_mail varchar(150) DEFAULT '',
  user_firewall SMALLINT DEFAULT 0,
  user_global_flag SMALLINT DEFAULT 0,
  user_cti_flag SMALLINT DEFAULT 0,
  user_manager SMALLINT NOT NULL DEFAULT 0,
  user_global_locale SMALLINT DEFAULT NULL,
  user_theme varchar(15) DEFAULT NULL,
  user_memo varchar(500) DEFAULT NULL,
  user_order INTEGER DEFAULT NULL,
  user_deleted SMALLINT DEFAULT 0,
  group_id INTEGER NOT NULL DEFAULT 0,
  created_id INTEGER NOT NULL DEFAULT 0,
  created_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  updated_id INTEGER DEFAULT NULL,
  updated_time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_user_id PRIMARY KEY (user_id),
  CONSTRAINT un_user_code UNIQUE (user_code),
  CONSTRAINT fk_user_info_group_id FOREIGN KEY (group_id) REFERENCES company.group_info(group_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE company.users_info IS 'メンバー情報';
COMMENT ON COLUMN company.users_info.user_id IS 'ID';
COMMENT ON COLUMN company.users_info.user_code IS 'メンバーコード';
COMMENT ON COLUMN company.users_info.user_login_id IS 'ログインID';
COMMENT ON COLUMN company.users_info.user_password IS 'パスワード';

INSERT INTO company.users_info (
  user_id, user_login_id, user_password, user_name_first, user_name_last, group_id
) VALUES (
  nextval('company.user_id_seq'::regclass), 'admin', ENCODE(DIGEST('admin', 'sha256'), 'hex'), 'NGUYEN', 'VAMHUONG', 1
);

CREATE TABLE system.one_time_pass_info (
  company_basic_login_id varchar(30) NOT NULL,
  user_mail_login_id varchar(8) NULL,
  one_time_pass varchar(6) NOT NULL,
  one_time_date DATE NOT NULL DEFAULT DATE(TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDD')),
  CONSTRAINT pk_one_time_pass_info PRIMARY KEY (company_basic_login_id, one_time_pass, user_mail_login_id, one_time_date)
);

CREATE SEQUENCE system.server_id_seq;
CREATE TABLE system.server_info (
  server_id INTEGER NOT NULL DEFAULT nextval('system.server_id_seq'::regclass),
  server_name varchar(45) NOT NULL DEFAULT '',
  server_type SMALLINT DEFAULT 0,
  host varchar(45) NOT NULL,
  port INTEGER NOT NULL DEFAULT 0,
  database varchar(20) NOT NULL DEFAULT '',
  username varchar(15) NOT NULL,
  password varchar(70) NOT NULL,
  company_id INTEGER NOT NULL DEFAULT 0,
  CONSTRAINT pk_server_server_id PRIMARY KEY (server_id),
  CONSTRAINT fk_server_info_company_id FOREIGN KEY (company_id) REFERENCES company.company_info(company_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE system.server_info IS '各会社DB情報';
COMMENT ON COLUMN system.server_info.server_name IS 'ラベル表示名';
COMMENT ON COLUMN system.server_info.host IS 'サーバIP又はドメイn名';
COMMENT ON COLUMN system.server_info.port IS 'PORT';
COMMENT ON COLUMN system.server_info.database IS 'DB名';
COMMENT ON COLUMN system.server_info.username IS 'ログインID';
COMMENT ON COLUMN system.server_info.password IS 'パースワード';
COMMENT ON COLUMN system.server_info.company_id IS '会社ID';
--select ENCRYPT(CONVERT_TO('admin1'::text, 'UTF8'), 'crm_001'::bytea, 'aes')
--select CONVERT_FROM(DECRYPT(ENCRYPT(CONVERT_TO('admin1'::text, 'UTF8'), 'crm_001'::bytea, 'aes'), 'crm_001'::bytea, 'aes'), 'UTF8')
