import random
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from database import get_supabase
from models import (
    ApiResponse,
    CreateFormBody,
    UpdateFormBody,
    extract_form_payload,
    snapshot_form_fields,
)

router = APIRouter(prefix="/software-copyright", tags=["software-copyright"])


def _generate_query_code() -> str:
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    random_num = random.randint(100, 999)
    return f"RJ{date_str}{random_num}"


def _row_response(row: dict) -> dict:
    payload = extract_form_payload(row)
    return {**row, "effective_form": payload}


@router.post("/form")
def create_form(body: CreateFormBody):
    client = get_supabase()
    query_code = _generate_query_code()
    insert_data = {
        **body.model_dump(),
        "query_code": query_code,
        "status": "draft",
    }

    result = (
        client.table("software_copyright_forms")
        .insert(insert_data)
        .select()
        .execute()
    )

    if not result.data:
        # 兼容未执行迁移、无 status 列的库
        insert_data.pop("status", None)
        result = (
            client.table("software_copyright_forms")
            .insert(insert_data)
            .select()
            .execute()
        )

    if not result.data:
        raise HTTPException(status_code=500, detail="创建失败")

    return ApiResponse(code=200, msg="创建成功", data=result.data[0])


@router.get("/forms")
def list_forms(user_id: str):
    client = get_supabase()
    result = (
        client.table("software_copyright_forms")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return ApiResponse(code=200, msg="获取成功", data=result.data or [])


@router.get("/form/{form_id}")
def get_form(form_id: str):
    client = get_supabase()
    result = (
        client.table("software_copyright_forms")
        .select("*")
        .eq("id", form_id)
        .execute()
    )
    if not result.data:
        return ApiResponse(code=404, msg="申请表不存在", data=None)
    return ApiResponse(code=200, msg="获取成功", data=_row_response(result.data[0]))


@router.get("/query/{code}")
def query_by_code(code: str):
    client = get_supabase()
    result = (
        client.table("software_copyright_forms")
        .select("*")
        .eq("query_code", code.strip().upper())
        .execute()
    )
    if not result.data:
        return ApiResponse(code=404, msg="查询码不存在或已过期", data=None)
    return ApiResponse(code=200, msg="查询成功", data=_row_response(result.data[0]))


@router.put("/form/{form_id}")
def update_form(form_id: str, body: UpdateFormBody):
    client = get_supabase()
    existing = (
        client.table("software_copyright_forms")
        .select("*")
        .eq("id", form_id)
        .execute()
    )
    if not existing.data:
        return ApiResponse(code=404, msg="申请表不存在", data=None)

    row = existing.data[0]
    updates = body.model_dump(exclude_none=True, exclude={"mark_enriched"})
    mark_enriched = body.mark_enriched

    if mark_enriched:
        merged = {**row, **updates}
        updates["enriched_data"] = snapshot_form_fields(merged)
        updates["status"] = "enriched"

    updates["updated_at"] = datetime.now(timezone.utc).isoformat()

    result = (
        client.table("software_copyright_forms")
        .update(updates)
        .eq("id", form_id)
        .select()
        .execute()
    )

    if not result.data:
        updates.pop("enriched_data", None)
        updates.pop("status", None)
        result = (
            client.table("software_copyright_forms")
            .update(updates)
            .eq("id", form_id)
            .select()
            .execute()
        )

    if not result.data:
        raise HTTPException(status_code=500, detail="更新失败")

    return ApiResponse(code=200, msg="更新成功", data=_row_response(result.data[0]))


@router.delete("/form/{form_id}")
def delete_form(form_id: str):
    client = get_supabase()
    client.table("software_copyright_forms").delete().eq("id", form_id).execute()
    return ApiResponse(code=200, msg="删除成功", data=None)
