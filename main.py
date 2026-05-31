import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import software_copyright, user
from database import get_supabase

load_dotenv()

app = FastAPI(title="软著自动化申报系统-后端")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api")
app.include_router(software_copyright.router, prefix="/api")


@app.get("/")
def root():
    return {
        "status": "软著后端正在运行中",
        "docs": "/docs",
        "api_prefix": "/api",
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/debug/db")
def debug_db():
    try:
        client = get_supabase()
        # 获取数据库连接信息
        url = os.getenv("COZE_SUPABASE_URL") or os.getenv("SUPABASE_URL")
        key_set = os.getenv("COZE_SUPABASE_SERVICE_ROLE_KEY") is not None or os.getenv("SUPABASE_SERVICE_ROLE_KEY") is not None
        
        # 尝试查询表
        result = client.table("software_copyright_forms").select("id").limit(1).execute()
        return {
            "status": "connected",
            "url": url[:30] + "..." if url else None,
            "has_key": key_set,
            "table_exists": True,
            "sample_data": result.data[:1] if result.data else []
        }
    except Exception as e:
        return {
            "status": "error",
            "url": os.getenv("COZE_SUPABASE_URL")[:30] + "..." if os.getenv("COZE_SUPABASE_URL") else None,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
