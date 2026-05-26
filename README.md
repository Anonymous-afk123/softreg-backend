# softreg-backend

软著登记系统后端服务，基于 FastAPI 构建。

## 技术栈

- **框架**: FastAPI 0.115.0
- **语言**: Python 3.11+
- **数据库**: Supabase (PostgreSQL)
- **认证**: JWT
- **部署**: Railway

## 快速开始

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量（复制 .env.example 为 .env）
cp .env.example .env

# 启动开发服务器
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 生产部署

已部署至 Railway:
- 线上地址: `https://web-production-2c115.up.railway.app`
- API 文档: `https://web-production-2c115.up.railway.app/docs`

### 环境变量

```bash
# .env 文件
COZE_SUPABASE_URL=your-supabase-url
COZE_SUPABASE_SERVICE_ROLE_KEY=your-supabase-key
SECRET_KEY=your-secret-key
```

## API 接口

### 软件著作权

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/software-copyright/form` | 提交采集表 |
| GET | `/api/software-copyright/query/{query_code}` | 查询登记信息 |
| GET | `/api/software-copyright/records` | 获取所有记录 |

### 用户认证

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/register` | 用户注册 |
| GET | `/api/auth/me` | 获取当前用户 |

## 项目结构

```
softreg-backend/
├── main.py                 # 应用入口
├── requirements.txt        # 依赖列表
├── .env.example           # 环境变量模板
├── app/                   # 应用目录
│   ├── __init__.py
│   ├── api/               # API 路由
│   ├── core/              # 核心配置
│   ├── models/            # 数据模型
│   ├── schemas/           # 数据校验
│   └── utils/             # 工具函数
```
