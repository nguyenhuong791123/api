CREATE OR REPLACE FUNCTION public.drop_customize_sequence()
RETURNS VOID AS $$
DECLARE
  query TEXT;
  cur_seq CURSOR FOR SELECT 'DROP SEQUENCE IF EXISTS customize.' || relname || ' CASCADE;' AS is_query 
                   FROM pg_class WHERE relkind='S' AND relname LIKE 'seq_id_%';

BEGIN
  OPEN cur_seq;
  LOOP
    FETCH cur_seq INTO query;
    EXIT WHEN NOT FOUND;
    IF query!='' THEN
      RAISE NOTICE '%', query;
      EXECUTE query;
      SELECT '' INTO query;
    END IF;
  END LOOP;
  RETURN;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION public.init_database(in_db VARCHAR(50), in_com INT)
RETURNS VOID AS $$
DECLARE
  is_s VARCHAR(50);
  is_tn VARCHAR(100);
  is_c VARCHAR(100);
  is_c_t VARCHAR(200);
  is_t_c VARCHAR(200);
  is_t VARCHAR(20);
  is_s_t VARCHAR(20);
  is_r INTEGER;
  is_l INTEGER;
  is_d VARCHAR(150);
  is_t_exists INTEGER;
  is_f_exists INTEGER;
  is_s_exists INTEGER;
  is_c_exists INTEGER;
  is_c_idx INTEGER DEFAULT 0;
  is_id_seq VARCHAR(50);
  is_td VARCHAR(150);
  is_label JSON;
  is_auth JSON;
  is_edit_obj JSON;
  is_disabled BOOLEAN DEFAULT true;
  is_required BOOLEAN DEFAULT false;
  --is_r_id INTEGER;
  --RETURNING id

  query TEXT;
  query_val TEXT;
  cur CURSOR FOR SELECT is_schema, is_table, is_column, is_type, is_nullable, is_length
                   ,(SELECT pgd.description FROM pg_catalog.pg_statio_all_tables AS st INNER JOIN pg_catalog.pg_description pgd ON (pgd.objoid=st.relid) INNER JOIN information_schema.columns c ON (pgd.objsubid=c.ordinal_position AND c.table_schema=st.schemaname AND c.table_name=st.relname) WHERE c.table_schema=tbl.is_schema AND c.table_name=tbl.is_table AND c.column_name=tbl.is_column) AS is_description
                   FROM(SELECT table_schema AS is_schema, table_name AS is_table, column_name AS is_column, CASE WHEN is_nullable='NO' THEN 0 ELSE 1 END AS is_nullable, COALESCE(null, udt_name, data_type) AS is_type, character_maximum_length AS is_length
                   FROM information_schema.columns
                     WHERE table_schema NOT IN ('public','pg_catalog', 'information_schema', 'mente') AND table_name NOT IN('company_basic_session_info', 'one_time_pass_info') AND table_name NOT LIKE('%_rel') OR (table_schema='mente' AND table_name='page_info')) AS tbl;

BEGIN
  IF in_db IS NULL OR in_db = '' THEN
    RAISE EXCEPTION 'Please set databases !!!';
  END IF;
  IF in_com IS NULL OR in_com <= 0 THEN
    RAISE EXCEPTION 'Please set company id !!!';
  END IF;

  TRUNCATE TABLE mente.label_info CASCADE;
  TRUNCATE TABLE mente.edit_object_info CASCADE;
  TRUNCATE TABLE mente.default_data_info CASCADE;
  TRUNCATE TABLE mente.ui_info CASCADE;
  TRUNCATE TABLE mente.properties_info CASCADE;
  TRUNCATE TABLE mente.schema_info CASCADE;
  TRUNCATE TABLE mente.default_data_info CASCADE;
  TRUNCATE TABLE mente.form_info CASCADE;
  TRUNCATE TABLE mente.page_info CASCADE;

  OPEN cur;
  LOOP
    FETCH cur INTO is_s, is_tn, is_c, is_t, is_r, is_l, is_d;
    EXIT WHEN NOT FOUND;

    IF is_s!='' AND is_tn!='' AND is_c!='' THEN
      SELECT is_s || '.' || is_tn INTO is_c_t;
      IF is_s = 'customize' THEN
        SELECT 'DROP TABLE IF EXISTS ' || is_c_t || ';' INTO query;
        RAISE NOTICE '%', query;
        EXECUTE query;
      ELSE

        SELECT MAX(page_id) FROM mente.page_info WHERE page_key=is_c_t INTO is_t_exists;
        IF is_t_exists IS NULL OR is_t_exists <= 0 THEN
          SELECT pg_description.description FROM pg_stat_user_tables, pg_description
            WHERE pg_stat_user_tables.relname in (select relname from pg_stat_user_tables)
            AND pg_stat_user_tables.relid=pg_description.objoid AND pg_description.objsubid=0
            AND pg_stat_user_tables.schemaname=is_s AND pg_stat_user_tables.relname=is_tn INTO is_td;

          IF is_c_t = 'company.company_info' THEN
            SELECT 'integer_company_info_company_id' INTO is_id_seq;
            -- SELECT 'hidden_company_info_company_id' INTO is_id_seq;
          ELSIF is_c_t = 'company.group_info' THEN
            SELECT 'integer_group_info_group_id' INTO is_id_seq;
            -- SELECT 'hidden_group_info_group_id' INTO is_id_seq;
          ELSIF is_c_t = 'company.users_info' THEN
            SELECT 'integer_users_info_user_id' INTO is_id_seq;
            -- SELECT 'hidden_users_info_user_id' INTO is_id_seq;
          ELSIF is_c_t = 'mente.page_info' THEN
            SELECT 'integer_page_info_page_id' INTO is_id_seq;
            -- SELECT 'hidden_page_info_page_id' INTO is_id_seq;
          ELSIF is_c_t = 'system.server_info' THEN
            SELECT 'integer_server_info_server_id' INTO is_id_seq;
            -- SELECT 'hidden_server_info_server_id' INTO is_id_seq;
          ELSIF is_c_t = 'system.api_info' THEN
            SELECT 'integer_api_info_api_id' INTO is_id_seq;
            -- SELECT 'hidden_api_info_api_id' INTO is_id_seq;
          ELSE
            SELECT '' INTO is_id_seq;
          END IF;

          SELECT json_build_object('00_search', true, '01_view', true, '02_create', true, '03_edit', true, '04_upload', true, '05_download', true) INTO is_auth;
          SELECT 'INSERT INTO mente.page_info(page_key, page_id_seq, company_id, page_auth) VALUES (' || chr(39) || is_c_t || chr(39) || ', ' || chr(39) || is_id_seq || chr(39) || ', ' || in_com || ',' || chr(39) || is_auth || chr(39) || ') RETURNING page_id;' INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query INTO is_t_exists;

          IF is_t_exists > 0 AND is_c_t = 'company.users_info' THEN
            SELECT 'UPDATE ' || is_c_t || ' SET user_default_page_id=' || is_t_exists || ';' INTO query;
            RAISE NOTICE '%', query;
            EXECUTE query;
          END IF;

          IF is_t_exists > 0 THEN
            IF (is_s = 'company' AND is_tn = 'company_info') THEN
              SELECT json_build_object('ja', '会社情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
            ELSIF (is_s = 'company' AND is_tn = 'group_info') THEN
              SELECT json_build_object('ja', '部署情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
            ELSIF (is_s = 'company' AND is_tn = 'users_info') THEN
              SELECT json_build_object('ja', 'ユーザー情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
            ELSIF (is_s = 'system' AND is_tn = 'api_info') THEN
              SELECT json_build_object('ja', 'API情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
            ELSIF (is_s = 'system' AND is_tn = 'server_info') THEN
              SELECT json_build_object('ja', 'サーバー情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
            ELSE
              SELECT json_build_object('ja', is_tn, 'en', is_tn, 'vi', is_tn) INTO is_label;
            END IF;

            SELECT 'INSERT INTO mente.label_info(schema_id, properties_name, object_label) VALUES (' || is_t_exists || ', ' || chr(39) || is_t_exists || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
            RAISE NOTICE '%', query;
            EXECUTE query;
          END IF;
        END IF;

        RAISE NOTICE '%', is_t_exists;
        IF is_t_exists IS NULL OR is_t_exists <= 0 THEN
          RAISE EXCEPTION 'Page info is not exists !!!';
        END IF;

        SELECT MAX(form_id) FROM mente.form_info WHERE page_id=is_t_exists INTO is_f_exists;
        IF is_f_exists IS NULL OR is_f_exists <= 0 THEN
          SELECT 'INSERT INTO mente.form_info(page_id, object_type, object_key, class_name) VALUES (' || is_t_exists || ', ' || chr(39) || 'div' || chr(39) || ', ' || chr(39) || 'form_' || is_tn || chr(39) || ', ' || chr(39) || 'div-box-100' || chr(39) || ') RETURNING form_id;' INTO query;
          EXECUTE query INTO is_f_exists;
        END IF;

        IF is_f_exists IS NULL OR is_f_exists <= 0 THEN
          RAISE EXCEPTION 'Form info is not exists !!!';
        END IF;

        SELECT 'shcema_' || is_s || '_' || is_tn INTO is_t_c;
        SELECT MAX(schema_id) FROM mente.schema_info WHERE form_id=is_f_exists INTO is_s_exists;
        IF is_s_exists IS NULL OR is_s_exists <= 0 THEN
          SELECT 'INSERT INTO mente.schema_info(form_id, schema_type, schema_key, object_type) VALUES (' || is_f_exists || ', ' || chr(39) || 'DIV' || chr(39) || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || 'object' || chr(39) || ') RETURNING schema_id;' INTO query;
          EXECUTE query INTO is_s_exists;
        END IF;
        IF is_s_exists IS NULL OR is_s_exists <= 0 THEN
          RAISE EXCEPTION 'Schema info is not exists !!!';
        END IF;

        SELECT count(properties_name) FROM mente.label_info WHERE properties_name=is_t_c INTO is_c_exists;
        IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
          SELECT json_build_object('ja', '基本情報', 'en', is_tn, 'vi', is_tn) INTO is_label;
          SELECT 'INSERT INTO mente.label_info(schema_id, properties_name, object_label) VALUES (' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;

          SELECT json_build_object('box_width', 100, 'item_name', is_t_c, 'label', is_label) INTO is_edit_obj;
          SELECT 'INSERT INTO mente.edit_object_info(schema_id, properties_name, value) VALUES ' INTO query;
          SELECT '(' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_edit_obj || chr(39) || ');' INTO query_val;
          SELECT query || query_val INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
        END IF;

        SELECT 
          CASE
            WHEN is_t = 'varchar' OR is_t = 'text' THEN
              'text'
            WHEN is_t = 'json' OR is_t = 'jsonb' THEN
              'string'
            WHEN is_t = 'int4' OR is_t = 'int2' THEN
              'integer'
            WHEN is_t = 'timestamp' THEN
              'datetime'
            ELSE is_t
          END INTO is_s_t;

        IF is_c = 'company_memo' OR is_c = 'group_memo' OR is_c = 'user_memo' THEN
          SELECT 'textarea' INTO is_s_t;
        ELSIF is_c = 'company_use_api'
          OR is_c = 'company_use_system_auth'
          OR is_c = 'company_theme'
          OR is_c = 'company_city'
          OR is_c = 'group_parent_id'
          OR is_c = 'user_theme'
          OR is_c = 'user_manager'
          OR is_c = 'user_city'
          OR is_c = 'user_default_page_id'
          OR (is_tn = 'users_info' AND is_c = 'group_id')
          OR (is_c = 'server_info' OR is_c = 'server_type')
          OR (is_tn = 'group_info' AND is_c = 'company_id')
          OR (is_tn = 'api_info' AND is_c = 'company_id')
          OR (is_tn = 'server_info' AND is_c = 'company_id') THEN
          SELECT 'select' INTO is_s_t;
        ELSIF is_c = 'company_cti_flag'
          OR is_c = 'company_global_locale'
          OR is_c = 'user_global_flag'
          OR is_c = 'user_cti_flag'
          OR is_c = 'user_firewall'
          OR is_c = 'user_view_menu'
          OR RIGHT(is_c, 8) = '_deleted' THEN
          SELECT 'radio' INTO is_s_t;
        ELSIF (is_tn = 'company_info' AND is_c = 'company_id')
          OR (is_tn = 'group_info' AND is_c = 'group_id')
          OR (is_tn = 'users_info' AND is_c = 'user_id')
          OR (is_tn = 'server_info' AND is_c = 'server_id')
          OR (is_tn = 'api_info' AND is_c = 'api_id')THEN
          SELECT 'integer' INTO is_s_t;
          -- SELECT 'hidden' INTO is_s_t;
        ELSIF is_c = 'company_logo' OR is_c = 'user_image' THEN
          SELECT 'image' INTO is_s_t;
        ELSIF is_c = 'company_basic_password'
          OR is_c = 'user_password'
          OR (is_tn = 'server_info' AND is_c = 'password') THEN
          SELECT 'password' INTO is_s_t;
        END IF;
        SELECT is_s_t || '_' || is_tn || '_' || is_c INTO is_t_c;

        SELECT
          CASE
            WHEN is_t = 'varchar' OR is_t = 'text' OR is_t = 'json' OR is_t = 'jsonb' OR is_t = 'timestamp' OR is_t = 'date' OR is_t = 'datetime' OR is_t = 'time' THEN
              'string'
            WHEN is_t = 'int4' OR is_t = 'int2' THEN
              'number'
            ELSE is_t
          END INTO is_t;

        IF is_c = 'company_use_api' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'sys_api', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF is_c = 'company_use_system_auth' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'sys_auth', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF is_c = 'company_cti_flag' OR is_c = 'company_global_locale' OR is_c = 'user_global_flag' OR is_c = 'user_cti_flag' OR is_c = 'user_firewall' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'flag', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;        
        ELSIF is_c = 'group_parent_id' OR (is_tn = 'users_info' AND is_c = 'group_id') THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'group_info', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF (is_tn = 'group_info' AND is_c = 'company_id') OR (is_tn = 'server_info' AND is_c = 'company_id') OR (is_tn = 'api_info' AND is_c = 'company_id') THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'company_info', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;      
        ELSIF is_c = 'company_city' OR is_c = 'user_city' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'city_info', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF is_c = 'company_theme' OR is_c = 'user_theme' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'themes', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF is_c = 'user_manager' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'user_manager', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;      
        ELSIF is_c = 'user_view_menu' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'menus', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;      
        ELSIF is_c = 'user_default_page_id' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'pages', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;      
        ELSIF is_c = 'server_info' OR is_c = 'server_type' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'server_type', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
        ELSIF RIGHT(is_c, 8) = '_deleted' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'deleted', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;        
        ELSIF is_c = 'company_logo' OR is_c = 'user_image' THEN
          SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'changed', true, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;        
        ELSE
          SELECT false INTO is_disabled;
          IF is_s_t = 'datetime' OR is_s_t = 'date' OR is_s_t = 'time' THEN
            SELECT json_build_object('type', is_t, 'idx', is_c_idx, 'datetype', is_s_t, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
          ELSE
            SELECT json_build_object('type', is_t, 'idx', is_c_idx, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
          END IF;
        END IF;

        SELECT count(properties_name) FROM mente.properties_info WHERE properties_name=is_t_c INTO is_c_exists;
        RAISE NOTICE '%', is_c_exists;
        IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
          SELECT 'INSERT INTO mente.properties_info(schema_id, properties_name, value) VALUES ' INTO query;
          SELECT '(' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_auth || chr(39) || ');' INTO query_val;
          SELECT query || query_val INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
          SELECT '' INTO query;
          SELECT is_c_idx+1 INTO is_c_idx;
        ELSE
          SELECT 'UPDATE mente.properties_info SET value=' || chr(39) || is_auth || chr(39) || ' WHERE properties_name=' || chr(39) || is_t_c || chr(39) INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
          SELECT '' INTO query;
        END IF;

        SELECT count(properties_name) FROM mente.label_info WHERE properties_name=is_t_c INTO is_c_exists;
        IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
          IF (is_tn = 'company_info' AND is_c = 'company_id')
            OR (is_tn = 'group_info' AND is_c = 'group_id')
            OR (is_tn = 'users_info' AND is_c = 'user_id')
            OR (is_tn = 'server_info' AND is_c = 'server_id')
            OR (is_tn = 'api_info' AND is_c = 'api_id') THEN
            SELECT json_build_object('ja', 'ID', 'en', 'ID', 'vi', 'ID') INTO is_label;
          ELSIF (is_tn != 'company_info' AND is_c = 'company_id') THEN
            SELECT json_build_object('ja', '会社ID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_name' THEN
            SELECT json_build_object('ja', '会社名', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_logo' THEN
            SELECT json_build_object('ja', 'ロゴ', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_home_page' THEN
            SELECT json_build_object('ja', 'ホームページ', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_copy_right' THEN
            SELECT json_build_object('ja', '著作権', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_global_ip' THEN
            SELECT json_build_object('ja', 'グローバルIP', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_home_page' THEN
            SELECT json_build_object('ja', 'ホームページ', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_global_locale' THEN
            SELECT json_build_object('ja', 'グローバル言語', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_basic_login_id' THEN
            SELECT json_build_object('ja', 'Basic Login ID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_basic_password' THEN
            SELECT json_build_object('ja', 'Basic Login Password', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_use_system_auth' THEN
            SELECT json_build_object('ja', 'システムログインモード', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_use_api' THEN
            SELECT json_build_object('ja', 'システムAPI', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'company_start_use_date' OR is_c = 'api_start_date' THEN
            SELECT json_build_object('ja', '使用開始日', 'en', is_c, 'vi', is_c) INTO is_label;

          ELSIF (is_tn != 'group_info' AND is_c = 'group_id') THEN
            SELECT json_build_object('ja', 'グループID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'group_name' THEN
            SELECT json_build_object('ja', 'グループ名', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'group_parent_id' THEN
            SELECT json_build_object('ja', '親部署', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'group_tree_id' THEN
            SELECT json_build_object('ja', '部署ツリー', 'en', is_c, 'vi', is_c) INTO is_label;

          ELSIF (is_tn != 'users_info' AND is_c = 'user_id') THEN
            SELECT json_build_object('ja', 'ユーザーID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_code' OR is_c = 'group_code' THEN
            SELECT json_build_object('ja', 'コード', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_login_id' THEN
            SELECT json_build_object('ja', 'ログインID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_password' THEN
            SELECT json_build_object('ja', 'パスワード', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_name_first' THEN
            SELECT json_build_object('ja', '名字', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_name_last' THEN
            SELECT json_build_object('ja', '名前', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_kana_first' THEN
            SELECT json_build_object('ja', '名字(カナ)', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_kana_last' THEN
            SELECT json_build_object('ja', '名前(カナ)', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_post' OR is_c = 'company_post' THEN
            SELECT json_build_object('ja', '郵便番号', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_city' OR is_c = 'company_city' THEN
            SELECT json_build_object('ja', '都道府県', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_address' OR is_c = 'company_address' THEN
            SELECT json_build_object('ja', '住所', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_address_kana' OR is_c = 'company_address_kana' THEN
            SELECT json_build_object('ja', '住所(カナ)', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_image' THEN
            SELECT json_build_object('ja', '画像', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_mail' THEN
            SELECT json_build_object('ja', 'メールアドレス', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_firewall' THEN
            SELECT json_build_object('ja', '外部から接続', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_cti_flag' OR is_c = 'company_cti_flag' THEN
            SELECT json_build_object('ja', '電話オプション', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_manager' THEN
            SELECT json_build_object('ja', 'ユーザーモード', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_global_flag' THEN
            SELECT json_build_object('ja', 'グローバル言語', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_theme' OR is_c = 'company_theme' THEN
            SELECT json_build_object('ja', 'レイアウト', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_memo' OR is_c = 'group_memo' OR is_c = 'company_memo' THEN
            SELECT json_build_object('ja', '備考', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_order' OR is_c = 'group_order' THEN
            SELECT json_build_object('ja', '表示順', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_deleted' OR is_c = 'group_deleted' OR is_c = 'company_deleted' OR is_c = 'api_deleted' THEN
            SELECT json_build_object('ja', '削除', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_view_menu' THEN
            SELECT json_build_object('ja', 'メニューモード', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'user_default_page_id' THEN
            SELECT json_build_object('ja', 'デフォルトページ', 'en', is_c, 'vi', is_c) INTO is_label;

          ELSIF (is_tn != 'server_info' AND is_c = 'server_id') THEN
            SELECT json_build_object('ja', 'サーバーID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'server_name' THEN
            SELECT json_build_object('ja', 'サーバー名', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'server_type' THEN
            SELECT json_build_object('ja', '種類', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'host' THEN
            SELECT json_build_object('ja', 'ホスト', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'port' THEN
            SELECT json_build_object('ja', 'ポート', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'database' THEN
            SELECT json_build_object('ja', 'データベース', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'username' THEN
            SELECT json_build_object('ja', 'ユーザー名', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'password' THEN
            SELECT json_build_object('ja', 'パスワード', 'en', is_c, 'vi', is_c) INTO is_label;

          ELSIF (is_tn = 'api_info' AND is_c = 'api_id') THEN
            SELECT json_build_object('ja', 'API ID', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'api_name' THEN
            SELECT json_build_object('ja', 'API名', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'api_expiration_date' THEN
            SELECT json_build_object('ja', '使用終了日', 'en', is_c, 'vi', is_c) INTO is_label;

          ELSIF is_c = 'created_id' THEN
            SELECT json_build_object('ja', '作成者', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'created_time' THEN
            SELECT json_build_object('ja', '作成日時', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'updated_id' THEN
            SELECT json_build_object('ja', '更新者', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSIF is_c = 'updated_time' THEN
            SELECT json_build_object('ja', '更新日時', 'en', is_c, 'vi', is_c) INTO is_label;
          ELSE
            SELECT json_build_object('ja', is_c, 'en', is_c, 'vi', is_c) INTO is_label;
          END IF;

          SELECT 'INSERT INTO mente.label_info(schema_id, properties_name, object_label) VALUES (' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
        END IF;

        IF is_disabled THEN
          SELECT json_build_object('box_height', 80, 'box_width', 25, 'item_name', is_t_c, 'item_type', is_s_t, 'label', is_label, 'option_disabled', true, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_edit_obj;
        ELSE
          SELECT json_build_object('box_height', 80, 'box_width', 25, 'item_name', is_t_c, 'item_type', is_s_t, 'label', is_label, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_edit_obj;
        END IF;
        SELECT true INTO is_disabled;
        SELECT count(properties_name) FROM mente.edit_object_info WHERE properties_name=is_t_c INTO is_c_exists;
        RAISE NOTICE '%', is_c_exists;
        IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
          SELECT 'INSERT INTO mente.edit_object_info(schema_id, properties_name, value) VALUES ' INTO query;
          SELECT '(' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_edit_obj || chr(39) || ');' INTO query_val;
          SELECT query || query_val INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
          SELECT '' INTO query;
        ELSE
          SELECT 'UPDATE mente.edit_object_info SET value=' || chr(39) || is_edit_obj || chr(39) || ' WHERE properties_name=' || chr(39) || is_t_c || chr(39) INTO query;
          RAISE NOTICE '%', query;
          EXECUTE query;
          SELECT '' INTO query;
        END IF;

        IF is_c = ANY(ARRAY[
          'company_name',
          'company_cti_flag',
          'company_basic_login_id',
          'company_basic_password',
          'company_use_system_auth',
          'group_name',
          'group_code',
          'user_login_id',
          'user_password',
          'user_name_first',
          'user_name_last',
          'user_manager',
          'user_view_menu',
          'server_name',
          'host',
          'port',
          'database',
          'username',
          'password',
          'api_name',
          'api_start_date',
          'api_expiration_date',
          'page_key'
        ])
        OR ((is_tn = 'group_info' OR is_tn = 'server_info' OR is_tn = 'api_info') AND is_c = 'company_id')
        OR (is_tn = 'users_info' AND is_c = 'group_id') THEN
          SELECT true INTO is_required;
        END IF;

        SELECT count(properties_name) FROM mente.ui_info WHERE properties_name=is_t_c INTO is_c_exists;
        RAISE NOTICE '%', is_c_exists;
        IF is_s_t = 'radio' THEN
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80 div-inline', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80 div-inline') INTO is_auth;
          END IF;
        ELSIF is_c = 'company_logo' OR is_c = 'user_image' THEN
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80 div-image-box', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80 div-image-box') INTO is_auth;
          END IF;
        ELSIF RIGHT(is_t_c, 5) = '_memo' THEN
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'textarea', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'textarea') INTO is_auth;
          END IF;
        ELSIF is_t_c LIKE '%password%' THEN
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'password', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'password') INTO is_auth;
          END IF;
        ELSIF (is_tn = 'company_info' AND is_c = 'company_id')
          OR (is_tn = 'group_info' AND is_c = 'group_id')
          OR (is_tn = 'users_info' AND is_c = 'user_id')
          OR (is_tn = 'server_info' AND is_c = 'server_id')
          OR (is_tn = 'api_info' AND is_c = 'api_id') THEN
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'hidden', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'hidden') INTO is_auth;
          END IF;
        ELSE
          IF is_required THEN
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'required', true) INTO is_auth;
          ELSE
            SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80') INTO is_auth;
          END IF;
        END IF;
        IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
          SELECT 'INSERT INTO mente.ui_info(schema_id, properties_name, value) VALUES ' INTO query;
          SELECT '(' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_auth || chr(39) || ');' INTO query_val;
          SELECT query || query_val INTO query;

          RAISE NOTICE '%', query;
          EXECUTE query;
          SELECT false INTO is_required;
          SELECT '' INTO query;
        END IF;

      END IF;
    END IF;
  END LOOP;

  DROP SEQUENCE IF EXISTS customize.varchar_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.varchar_field_datas_id_seq;
  CREATE TABLE customize.varchar_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.varchar_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value varchar(50),
    CONSTRAINT pk_varchar_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_varchar_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.text_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.text_field_datas_id_seq;
  CREATE TABLE customize.text_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.text_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value TEXT,
    CONSTRAINT pk_text_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_text_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.date_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.date_field_datas_id_seq;
  CREATE TABLE customize.date_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.date_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value DATE,
    CONSTRAINT pk_date_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_date_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.datetime_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.datetime_field_datas_id_seq;
  CREATE TABLE customize.datetime_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.date_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value TIMESTAMP,
    CONSTRAINT pk_datetime_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_datetime_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.time_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.time_field_datas_id_seq;
  CREATE TABLE customize.time_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.time_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value TIME,
    CONSTRAINT pk_time_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_time_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.file_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.file_field_datas_id_seq;
  CREATE TABLE customize.file_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.file_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value JSON,
    CONSTRAINT pk_file_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_file_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.integer_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.integer_field_datas_id_seq;
  CREATE TABLE customize.integer_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.integer_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value INTEGER,
    CONSTRAINT pk_integer_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_integer_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  DROP SEQUENCE IF EXISTS customize.double_field_datas_id_seq CASCADE;
  CREATE SEQUENCE customize.double_field_datas_id_seq;
  CREATE TABLE customize.double_field_datas (
    field_id INTEGER NOT NULL DEFAULT nextval('customize.double_field_datas_id_seq'::regclass),
    page_id INTEGER NOT NULL DEFAULT 0,
    row_id INTEGER NOT NULL DEFAULT 0,
    properties_name varchar(50) NOT NULL DEFAULT '',
    value DECIMAL(20, 3),
    CONSTRAINT pk_double_field_datas_properties_name_row_id PRIMARY KEY (properties_name, row_id),
    CONSTRAINT fk_double_field_datas_page_id FOREIGN KEY (page_id) REFERENCES mente.page_info(page_id) MATCH SIMPLE ON UPDATE NO ACTION ON DELETE NO ACTION
  );

  RETURN;
END;
$$ LANGUAGE plpgsql;
SELECT public.drop_customize_sequence();
SELECT public.init_database('smartcrm', 1);
