from typing import Any, Optional

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    code: int
    msg: str
    data: Any = None


class WechatLoginBody(BaseModel):
    code: str
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None


class CreateFormBody(BaseModel):
    user_id: str
    software_full_name: str
    software_short_name: Optional[str] = None
    version: str
    software_category: str
    development_date: str
    is_published: bool = False
    development_hardware: str
    runtime_hardware: str
    development_os: str
    development_tools: str
    runtime_platform: str
    runtime_environment: str
    programming_language: str
    source_code_lines: int
    development_purpose: str
    target_industry: str
    main_functions: str
    technical_features: str
    company_name: str
    credit_code: str


class UpdateFormBody(BaseModel):
    software_full_name: Optional[str] = None
    software_short_name: Optional[str] = None
    version: Optional[str] = None
    software_category: Optional[str] = None
    development_date: Optional[str] = None
    is_published: Optional[bool] = None
    development_hardware: Optional[str] = None
    runtime_hardware: Optional[str] = None
    development_os: Optional[str] = None
    development_tools: Optional[str] = None
    runtime_platform: Optional[str] = None
    runtime_environment: Optional[str] = None
    programming_language: Optional[str] = None
    source_code_lines: Optional[int] = None
    development_purpose: Optional[str] = None
    target_industry: Optional[str] = None
    main_functions: Optional[str] = None
    technical_features: Optional[str] = None
    company_name: Optional[str] = None
    credit_code: Optional[str] = None
    mark_enriched: bool = Field(
        default=True,
        description="保存为网页补全版本（status=enriched，写入 enriched_data）",
    )


FORM_FIELD_NAMES = [
    "software_full_name",
    "software_short_name",
    "version",
    "software_category",
    "development_date",
    "is_published",
    "development_hardware",
    "runtime_hardware",
    "development_os",
    "development_tools",
    "runtime_platform",
    "runtime_environment",
    "programming_language",
    "source_code_lines",
    "development_purpose",
    "target_industry",
    "main_functions",
    "technical_features",
    "company_name",
    "credit_code",
]


def extract_form_payload(row: dict) -> dict:
    """合并 enriched_data 与表字段，供网页展示与生成使用。"""
    if row.get("status") == "enriched" and row.get("enriched_data"):
        merged = {**row, **row["enriched_data"]}
        for key in FORM_FIELD_NAMES:
            if key in row["enriched_data"]:
                merged[key] = row["enriched_data"][key]
        return merged
    return row


def snapshot_form_fields(data: dict) -> dict:
    return {k: data[k] for k in FORM_FIELD_NAMES if k in data and data[k] is not None}
