-- 開発用ユーザとデータベース
CREATE DATABASE dev_db;
GRANT ALL PRIVILEGES ON DATABASE dev_db TO dev_user;

-- テスト用ユーザとデータベース
CREATE DATABASE test_db;
CREATE USER test_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE test_db TO test_user;

-- dev_user にスキーマ変更権限を付与
ALTER DATABASE dev_db OWNER TO dev_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO dev_user;

-- test_user にスキーマ変更権限を付与
ALTER DATABASE test_db OWNER TO test_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO test_user;
