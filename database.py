import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


def _get_env(*keys: str) -> str | None:
    for key in keys:
        value = os.getenv(key)
        if value:
            return value
    return None


@lru_cache
def get_supabase() -> Client:
    url = _get_env("COZE_SUPABASE_URL", "SUPABASE_URL")
    key = _get_env(
        "COZE_SUPABASE_SERVICE_ROLE_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
        "COZE_SUPABASE_ANON_KEY",
        "SUPABASE_ANON_KEY",
    )
    if not url or not key:
        raise RuntimeError(
            "请配置 COZE_SUPABASE_URL 与 COZE_SUPABASE_SERVICE_ROLE_KEY（或 SUPABASE_*）"
        )
    return create_client(url, key)
