-- 在扣子「生产环境」→ SQL 查询 中整段复制运行
-- 说明：库里若已有网页用的 users 表（无 openid），本脚本改用 wechat_users，避免冲突

-- 1. 小程序微信用户表（与网页 users 表分开）
CREATE TABLE IF NOT EXISTS wechat_users (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  openid varchar(128) NOT NULL UNIQUE,
  unionid varchar(128),
  nickname varchar(128),
  avatar_url varchar(512),
  phone varchar(20),
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz
);

CREATE INDEX IF NOT EXISTS wechat_users_openid_idx ON wechat_users (openid);

-- 2. 软著采集表
CREATE TABLE IF NOT EXISTS software_copyright_forms (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES wechat_users(id) ON DELETE CASCADE,
  software_full_name varchar(256),
  software_short_name varchar(128),
  version varchar(64),
  software_category varchar(128),
  development_date varchar(32),
  is_published boolean DEFAULT false,
  development_hardware varchar(50),
  runtime_hardware varchar(50),
  development_os varchar(50),
  development_tools varchar(50),
  runtime_platform varchar(50),
  runtime_environment varchar(50),
  programming_language varchar(50),
  source_code_lines integer,
  development_purpose varchar(50),
  target_industry varchar(50),
  main_functions text,
  technical_features text,
  company_name varchar(256),
  credit_code varchar(32),
  query_code varchar(32),
  status varchar(20) NOT NULL DEFAULT 'draft',
  enriched_data jsonb,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz
);

CREATE INDEX IF NOT EXISTS software_copyright_forms_user_id_idx
  ON software_copyright_forms (user_id);

CREATE INDEX IF NOT EXISTS software_copyright_forms_created_at_idx
  ON software_copyright_forms (created_at);

CREATE UNIQUE INDEX IF NOT EXISTS software_copyright_forms_query_code_unique
  ON software_copyright_forms (query_code);

CREATE INDEX IF NOT EXISTS software_copyright_forms_query_code_idx
  ON software_copyright_forms (query_code);
