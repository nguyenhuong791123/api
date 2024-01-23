DROP SEQUENCE IF EXISTS mente.schema_id_seq CASCADE;
DROP TABLE IF EXISTS mente.schema_info;
DROP SEQUENCE IF EXISTS mente.properties_id_seq CASCADE;
DROP TABLE IF EXISTS mente.properties_info;

CREATE SEQUENCE mente.form_id_seq;
CREATE TABLE mente.form_info (
  form_id INTEGER NOT NULL DEFAULT nextval('mente.form_id_seq'::regclass),
  object_type varchar(10) NOT NULL DEFAULT '',
  object_key varchar(50) NOT NULL DEFAULT '',
  class_name varchar(50) NOT NULL DEFAULT '',
  idx INTEGER NOT NULL DEFAULT 0,
  page_id INTEGER NOT NULL DEFAULT 0,
  CONSTRAINT pk_form_id PRIMARY KEY (form_id),
  CONSTRAINT fk_form_info_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.form_info IS 'フォーム情報';
COMMENT ON COLUMN mente.form_info.form_id IS 'フォームID';
COMMENT ON COLUMN mente.form_info.page_id IS 'ページID';

CREATE SEQUENCE mente.schema_id_seq;
CREATE TABLE mente.schema_info (
  schema_id INTEGER NOT NULL DEFAULT nextval('mente.schema_id_seq'::regclass),
  schema_type varchar(10) NOT NULL DEFAULT '',
  schema_key varchar(50) NOT NULL DEFAULT '',
  idx INTEGER NOT NULL DEFAULT 0,
  form_id INTEGER NOT NULL DEFAULT 0,
  object_type varchar(10) NOT NULL DEFAULT '',
  CONSTRAINT pk_schema_id PRIMARY KEY (schema_id),
  CONSTRAINT fk_shcema_info_form_id FOREIGN KEY (form_id) REFERENCES mente.form_info(form_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.schema_info IS 'スキーマ情報';
COMMENT ON COLUMN mente.schema_info.schema_id IS 'スキーマID';
COMMENT ON COLUMN mente.schema_info.form_id IS 'フォームID';

CREATE SEQUENCE mente.properties_id_seq;
CREATE TABLE mente.properties_info (
  properties_id INTEGER NOT NULL DEFAULT nextval('mente.properties_id_seq'::regclass),
  properties_name varchar(50) NOT NULL DEFAULT '',
  value jsonb,
  schema_id INTEGER NOT NULL DEFAULT 0,
  CONSTRAINT pk_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
  CONSTRAINT fk_properties_info_schema_id FOREIGN KEY (schema_id) REFERENCES mente.schema_info(schema_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.properties_info IS 'Field情報';
COMMENT ON COLUMN mente.properties_info.schema_id IS 'スキーマID';

-- CREATE SEQUENCE mente.ui_id_seq;
CREATE TABLE mente.ui_info (
  -- ui_id INTEGER NOT NULL DEFAULT nextval('mente.ui_id_seq'::regclass),
  schema_id INTEGER NOT NULL,
  properties_name varchar(50) NOT NULL DEFAULT '',
  value jsonb,
  -- updated_id INTEGER DEFAULT NULL,
  -- updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- CONSTRAINT pk_ui_schema_id PRIMARY KEY (schema_id),
  CONSTRAINT pk_ui_info_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
  CONSTRAINT fk_ui_info_schema_id FOREIGN KEY (schema_id) REFERENCES mente.schema_info(schema_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.ui_info IS 'Field UI情報';
COMMENT ON COLUMN mente.ui_info.schema_id IS 'スキーマID';

-- CREATE SEQUENCE mente.data_id_seq;
CREATE TABLE mente.default_data_info (
  -- data_id INTEGER NOT NULL DEFAULT nextval('mente.data_id_seq'::regclass),
  schema_id INTEGER NOT NULL,
  properties_name varchar(50) NOT NULL DEFAULT '',
  type INTEGER NOT NULL DEFAULT 0,
  value jsonb,
  -- updated_id INTEGER DEFAULT NULL,
  -- updated_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- CONSTRAINT pk_default_data_schema_id PRIMARY KEY (schema_id),
  CONSTRAINT pk_default_data_info_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
  CONSTRAINT fk_default_data_info_schema_id FOREIGN KEY (schema_id) REFERENCES mente.schema_info(schema_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.default_data_info IS 'Default Data情報';
COMMENT ON COLUMN mente.default_data_info.schema_id IS 'スキーマID';

CREATE TABLE mente.base64_info (
  properties_name varchar(50) NOT NULL DEFAULT '',
  name varchar(50) NOT NULL DEFAULT '',
  size INTEGER NOT NULL DEFAULT 0,
  data TEXT NOT NULL DEFAULT '',
  schema_id INTEGER NOT NULL,
  CONSTRAINT pk_base64_info_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
  CONSTRAINT fk_base64_info_schema_id FOREIGN KEY (schema_id) REFERENCES mente.schema_info(schema_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);
COMMENT ON TABLE mente.base64_info IS 'ファイルをBase64に変換情報';
COMMENT ON COLUMN mente.base64_info.properties_name IS 'FieldID';
COMMENT ON COLUMN mente.base64_info.name IS 'ファイル名';
COMMENT ON COLUMN mente.base64_info.size IS 'ファイルSize';
COMMENT ON COLUMN mente.base64_info.data IS '変換した、Base64 Data';

-- CREATE SEQUENCE mente.edit_id_seq;
CREATE TABLE mente.edit_object_info (
  -- edit_id INTEGER NOT NULL DEFAULT nextval('mente.edit_id_seq'::regclass),
  schema_id INTEGER NOT NULL,
  properties_name varchar(50) NOT NULL,
  edit_type INTEGER NOT NULL DEFAULT 0,
  value jsonb,
  CONSTRAINT pk_edit_object_info_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
  CONSTRAINT fk_edit_object_info_schema_id FOREIGN KEY (schema_id) REFERENCES mente.schema_info(schema_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- CREATE SEQUENCE mente.label_id_seq;
CREATE TABLE mente.label_info (
  -- label_id INTEGER NOT NULL DEFAULT nextval('mente.label_id_seq'::regclass),
  schema_id INTEGER NOT NULL,
  properties_name varchar(50) NOT NULL,
  -- object_type INTEGER NOT NULL DEFAULT 0,
  object_label jsonb,
  CONSTRAINT pk_label_info_properties_name_schema_id PRIMARY KEY (properties_name, schema_id),
);
