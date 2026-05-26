from fastapi import APIRouter, HTTPException

from database import get_supabase
from models import ApiResponse, WechatLoginBody

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/wechat-login")
def wechat_login(body: WechatLoginBody):
    """开发环境：用 code 模拟 openid；生产可接微信 jscode2session。"""
    # 开发环境：同一 code 对应同一用户，便于测试历史记录
    openid = f"dev_{body.code}"
    client = get_supabase()

    existing = (
        client.table("wechat_users")
        .select("*")
        .eq("openid", openid)
        .execute()
    )

    if existing.data and len(existing.data) > 0:
        user = existing.data[0]
        return ApiResponse(
            code=200,
            msg="登录成功",
            data={"user": user, "token": f"mock_token_{user['id']}"},
        )

    created = (
        client.table("wechat_users")
        .insert(
            {
                "openid": openid,
                "nickname": body.nickname or "微信用户",
                "avatar_url": body.avatar_url or "",
            }
        )
        .select()
        .single()
        .execute()
    )

    if created.data is None:
        raise HTTPException(status_code=500, detail="创建用户失败")

    user = created.data
    return ApiResponse(
        code=200,
        msg="注册成功",
        data={"user": user, "token": f"mock_token_{user['id']}"},
    )


@router.get("/info")
def get_user_info(user_id: str):
    client = get_supabase()
    result = (
        client.table("wechat_users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )
    if not result.data:
        return ApiResponse(code=404, msg="用户不存在", data=None)
    return ApiResponse(code=200, msg="获取成功", data=result.data[0])
