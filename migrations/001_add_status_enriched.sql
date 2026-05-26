-- 在 Supabase SQL Editor 中执行（若列已存在可跳过对应语句）

ALTER TABLE software_copyright_forms
  ADD COLUMN IF NOT EXISTS query_code varchar(32);

ALTER TABLE software_copyright_forms
  ADD COLUMN IF NOT EXISTS status varchar(20) NOT NULL DEFAULT 'draft';

ALTER TABLE software_copyright_forms
  ADD COLUMN IF NOT EXISTS enriched_data jsonb;

CREATE UNIQUE INDEX IF NOT EXISTS software_copyright_forms_query_code_unique
  ON software_copyright_forms (query_code);

CREATE INDEX IF NOT EXISTS software_copyright_forms_query_code_idx
  ON software_copyright_forms (query_code);
