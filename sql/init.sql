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
  is_td VARCHAR(150);
  is_label JSON;
  is_auth JSON;
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

  OPEN cur;
  LOOP
    FETCH cur INTO is_s, is_tn, is_c, is_t, is_r, is_l, is_d;
    EXIT WHEN NOT FOUND;

    IF is_s!='' AND is_tn!='' AND is_c!='' THEN
      SELECT is_s || '.' || is_tn INTO is_c_t;
      SELECT MAX(page_id) FROM mente.page_info WHERE page_key=is_c_t INTO is_t_exists;
      IF is_t_exists IS NULL OR is_t_exists <= 0 THEN
        SELECT pg_description.description FROM pg_stat_user_tables, pg_description
          WHERE pg_stat_user_tables.relname in (select relname from pg_stat_user_tables)
          AND pg_stat_user_tables.relid=pg_description.objoid AND pg_description.objsubid=0
          AND pg_stat_user_tables.schemaname=is_s AND pg_stat_user_tables.relname=is_tn INTO is_td;

		SELECT json_build_object('00_search', true, '01_view', true, '02_create', true, '03_edit', true, '04_upload', true, '05_download', true) INTO is_auth;
        SELECT 'INSERT INTO mente.page_info(page_key, company_id, page_auth) VALUES (' || chr(39) || is_c_t || chr(39) || ', ' || in_com || ',' || chr(39) || is_auth || chr(39) || ') RETURNING page_id;' INTO query;
        RAISE NOTICE '%', query;
        EXECUTE query INTO is_t_exists;

        IF is_t_exists > 0 THEN
          SELECT json_build_object('ja', is_tn, 'en', is_tn, 'vi', is_tn) INTO is_label;
          SELECT 'INSERT INTO mente.label_info(properties_name, object_label) VALUES (' || chr(39) || is_t_exists || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
          -- SELECT 'INSERT INTO mente.object_label_info(object_id, object_type, object_label) VALUES (' || is_t_exists || ', 1, ' || chr(39) || is_label || chr(39) || ' );' INTO query;
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
        SELECT 'INSERT INTO mente.label_info(properties_name, object_label) VALUES (' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
        RAISE NOTICE '%', query;
        EXECUTE query;
      END IF;

      SELECT 
        CASE
	        WHEN is_t = 'varchar' OR is_t = 'text' OR is_t = 'json' OR is_t = 'jsonb' THEN
		        'string'
	        WHEN is_t = 'int4' OR is_t = 'int2' THEN
		        'number'
	        WHEN is_t = 'timestamp' THEN
		        'datetime'
	        ELSE is_t
        END INTO is_s_t;
      IF RIGHT(is_t_c, 5) = '_memo' THEN
        SELECT 'textarea' INTO is_s_t;
      END IF;
      IF is_c = 'company_use_api'
        OR is_c = 'company_use_system_auth'
        OR is_c = 'company_theme'
        OR is_c = 'company_city'
        OR is_c = 'group_parent_id'
        OR is_c = 'user_theme'
        OR is_c = 'user_manager'
        OR is_c = 'user_city'
        OR (is_tn = 'users_info' AND is_c = 'group_id')
        OR (is_c = 'server_info' OR is_c = 'server_type') THEN
        SELECT 'select' INTO is_s_t;
      ELSIF is_c = 'company_cti_flag'
        OR is_c = 'company_global_locale'
        OR is_c = 'user_global_flag'
        OR is_c = 'user_cti_flag'
        OR RIGHT(is_c, 8) = '_deleted' THEN
        SELECT 'radio' INTO is_s_t;
      ELSIF (is_tn = 'company_info' AND is_c = 'company_id')
        OR (is_tn = 'group_info' AND is_c = 'group_id')
        OR (is_tn = 'users_info' AND is_c = 'user_id')
        OR (is_tn = 'server_info' AND is_c = 'server_id')
        OR (is_tn = 'api_info' AND is_c = 'api_id')
        OR (is_tn = 'group_info' AND is_c = 'company_id')
        OR (is_tn = 'api_info' AND is_c = 'company_id')
        OR (is_tn = 'server_info' AND is_c = 'company_id') THEN
        SELECT 'hidden' INTO is_s_t;
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
      ELSIF is_c = 'company_cti_flag' OR is_c = 'company_global_locale' OR is_c = 'user_global_flag' OR is_c = 'user_cti_flag' THEN
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
      ELSIF is_c = 'server_info' OR is_c = 'server_type' THEN
        SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'server_type', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
      ELSIF RIGHT(is_c, 8) = '_deleted' THEN
        SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'deleted', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;        
      -- ELSIF is_c = 'group_parent_id' THEN
      --   SELECT json_build_object('type', 'string', 'idx', is_c_idx, 'option_target', 'group_info', 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
      ELSE
        SELECT json_build_object('type', is_t, 'idx', is_c_idx, 'auth', json_build_object('create', true,'edit', true,'search', true,'view', true)) INTO is_auth;
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
        SELECT json_build_object('ja', is_c, 'en', is_c, 'vi', is_c) INTO is_label;
        SELECT 'INSERT INTO mente.label_info(properties_name, object_label) VALUES (' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_label || chr(39) || ' );' INTO query;
        RAISE NOTICE '%', query;
        EXECUTE query;
      END IF;

      SELECT count(properties_name) FROM mente.ui_info WHERE properties_name=is_t_c INTO is_c_exists;
      RAISE NOTICE '%', is_c_exists;
      IF RIGHT(is_t_c, 5) = '_memo' THEN
        SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'textarea') INTO is_auth;
      ELSIF is_t_c LIKE '%password%' THEN
        SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'password') INTO is_auth;
      ELSIF (is_tn = 'company_info' AND is_c = 'company_id')
        OR (is_tn = 'group_info' AND is_c = 'group_id')
        OR (is_tn = 'users_info' AND is_c = 'user_id')
        OR (is_tn = 'server_info' AND is_c = 'server_id')
        OR (is_tn = 'api_info' AND is_c = 'api_id')
        OR (is_tn = 'group_info' AND is_c = 'company_id')
        OR (is_tn = 'api_info' AND is_c = 'company_id')
        OR (is_tn = 'server_info' AND is_c = 'company_id') THEN
        SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80', 'ui:widget', 'hidden') INTO is_auth;
      ELSE
        SELECT json_build_object('classNames', 'div-box div-box-25 div-box-height-80') INTO is_auth;
      END IF;
      IF is_c_exists IS NULL OR is_c_exists <= 0 THEN
  	    SELECT 'INSERT INTO mente.ui_info(schema_id, properties_name, value) VALUES ' INTO query;
        SELECT '(' || is_s_exists || ', ' || chr(39) || is_t_c || chr(39) || ', ' || chr(39) || is_auth || chr(39) || ');' INTO query_val;
	      SELECT query || query_val INTO query;

        RAISE NOTICE '%', query;
        EXECUTE query;
	      SELECT '' INTO query;
      END IF;
    END IF;
  END LOOP;

  RETURN;
END;
$$ LANGUAGE plpgsql;
SELECT public.init_database('smartcrm', 1);
