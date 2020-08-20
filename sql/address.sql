CREATE OR REPLACE FUNCTION public.mask_zip_codes_info(work_path VARCHAR(50))
RETURNS VOID AS $$
DECLARE
  r_code RECORD;
  query TEXT;

BEGIN
  IF work_path IS NOT NULL AND work_path != '' THEN
    --CSVから全データ導入テーブルを作成
    CREATE TABLE public.address_info_copy (
      col0 varchar(10), col1 varchar(10), col2 TEXT, col3 TEXT, col4 TEXT, col5 TEXT, col6 TEXT, col7 TEXT
      , col8 TEXT, col9 TEXT, col10 varchar(10), col11 varchar(10), col12 varchar(10), col13 varchar(10), col14 varchar(10)
    );
    --CSVから全データ導入
    SELECT 'COPY public.address_info_copy FROM ''' || work_path || 'KEN_ALL.CSV'' DELIMITER ''' || ',' || ''' CSV;' INTO query;
    EXECUTE query;
    --RAISE NOTICE 'COPY CSV -> %', query;

    SELECT 'DROP TABLE IF EXISTS mente.city_info;' || chr(13)
      || 'CREATE TABLE mente.city_info (' || chr(13)
      || '  code VARCHAR(3) NOT NULL DEFAULT '''',' || chr(13)
      || '  name VARCHAR(30) NOT NULL DEFAULT '''',' || chr(13)
      || '  CONSTRAINT un_city_code UNIQUE (code)' || chr(13)
      || ');' || chr(13)
      || 'COMMENT ON TABLE mente.city_info IS ''都道府県情報'';' || chr(13)
      || 'COMMENT ON COLUMN mente.city_info.code IS ''都道府県コード'';' || chr(13)
      || 'COMMENT ON COLUMN mente.city_info.name IS ''都道府県名'';' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''01'', ''北海道'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''02'', ''青森県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''03'', ''岩手県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''04'', ''宮城県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''05'', ''秋田県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''06'', ''山形県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''07'', ''福島県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''08'', ''茨城県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''09'', ''栃木県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''10'', ''群馬県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''11'', ''埼玉県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''12'', ''千葉県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''13'', ''東京都'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''14'', ''神奈川県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''15'', ''新潟県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''16'', ''富山県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''17'', ''石川県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''18'', ''福井県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''19'', ''山梨県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''20'', ''長野県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''21'', ''岐阜県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''22'', ''静岡県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''23'', ''愛知県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''24'', ''三重県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''25'', ''滋賀県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''26'', ''京都府'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''27'', ''大阪府'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''28'', ''兵庫県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''29'', ''奈良県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''30'', ''和歌山県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''31'', ''鳥取県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''32'', ''島根県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''33'', ''岡山県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''34'', ''広島県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''35'', ''山口県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''36'', ''徳島県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''37'', ''香川県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''38'', ''愛媛県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''39'', ''高知県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''40'', ''福岡県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''41'', ''佐賀県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''42'', ''長崎県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''43'', ''熊本県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''44'', ''大分県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''45'', ''宮崎県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''46'', ''鹿児島県'');' || chr(13)
      || 'INSERT INTO mente.city_info (code, name) VALUES (''47'', ''沖縄県'');'
    INTO query;
    EXECUTE query;
    --RAISE NOTICE 'CREATE TABLE -> %', query;

    SELECT 'DROP TABLE IF EXISTS mente.address_info;' || chr(13)
      || 'CREATE TABLE mente.address_info(' || chr(13)
      || '  post VARCHAR(8) NOT NULL DEFAULT '''',' || chr(13)
      || '  city_code VARCHAR(3) NOT NULL DEFAULT '''',' || chr(13)
      || '  city VARCHAR(50) NOT NULL DEFAULT '''',' || chr(13)
      || '  district VARCHAR(70) NOT NULL DEFAULT '''',' || chr(13)
      || '  address VARCHAR(150) NOT NULL DEFAULT '''',' || chr(13)
      || '  city_kana VARCHAR(100) NOT NULL DEFAULT '''',' || chr(13)
      || '  district_kana VARCHAR(100) NOT NULL DEFAULT '''',' || chr(13)
      || '  address_kana VARCHAR(200) NOT NULL DEFAULT ''''' || chr(13)
      || ') PARTITION BY LIST (city_code);' || chr(13)
      || 'COMMENT ON TABLE mente.address_info IS ''住所情報'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.post IS ''郵便番号'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.city IS ''都道府県'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.city_code IS ''都道府県コード'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.district IS ''市区町村'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.address IS ''住所'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.city_kana IS ''都道府県カナ'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.district_kana IS ''市区町村カナ'';' || chr(13)
      || 'COMMENT ON COLUMN mente.address_info.address_kana IS ''住所カナ'';' || chr(13)
      INTO query;
      EXECUTE query;
      --RAISE NOTICE 'CREATE TABLE PARTITION -> %', query;

   SELECT '' INTO query;
   FOR r_code IN SELECT code AS city FROM mente.city_info LOOP
     SELECT query || 'CREATE TABLE mente.' || 'city_' || r_code.city || ' PARTITION OF mente.address_info FOR VALUES IN (''' || r_code.city || ''');'  || chr(13) INTO query;
   END LOOP;
   EXECUTE query;
   RAISE NOTICE 'CREATE TABLE PARTITION -> %', query;

   --全データ導入
   INSERT INTO mente.address_info(
     post, city_code, city, district, address, city_kana, district_kana, address_kana
   ) SELECT col2, (SELECT code FROM mente.city_info WHERE TRIM(name)=TRIM(col6)), col6, col7, col8, col5, col4, col5 FROM public.address_info_copy;
   DROP TABLE IF EXISTS public.address_info_copy;

  ELSE
    RAISE NOTICE 'You must setting work_path if you want add Address info !!!';
  END IF;

  RETURN;
END;
$$ LANGUAGE plpgsql;
--SELECT public.mask_zip_codes_info('C://home//');
