# 🚀 Render 部署指南

本项目已配置为可一键部署到 Render 平台。前端和后端将打包在同一个 Docker 容器中。

## 📋 前置要求

- GitHub 账号
- Render 账号（免费注册：https://render.com）
- Git 已安装

## 🎯 快速部署步骤

### 1. 推送代码到 GitHub

```bash
# 初始化 git（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Ready for Render deployment"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/YOUR_USERNAME/attention-surgery.git

# 推送
git push -u origin main
```

### 2. 在 Render 上创建 Web Service

#### 方式 A: 使用 render.yaml 自动部署（推荐 ⭐️）

1. 访问 https://dashboard.render.com
2. 点击 **"New +"** → **"Blueprint"**
3. 连接你的 GitHub 仓库
4. Render 会自动检测 `render.yaml` 文件并配置服务
5. 点击 **"Apply"** 开始部署

#### 方式 B: 手动创建 Web Service

1. 访问 https://dashboard.render.com
2. 点击 **"New +"** → **"Web Service"**
3. 连接你的 GitHub 仓库
4. 配置以下信息：
   - **Name**: `attention-surgery`
   - **Region**: `Oregon (US West)` 或任何地区
   - **Runtime**: `Docker`
   - **Plan**: `Starter` (推荐) 或 `Free`
   - **Dockerfile Path**: `./Dockerfile`
   - **Docker Context**: `.` (root)

5. 添加环境变量（可选）：
   - `PORT`: `7860` (默认)

6. 设置健康检查：
   - **Health Check Path**: `/health`

7. 点击 **"Create Web Service"**

### 3. 等待部署完成

- 首次部署大约需要 **5-10 分钟**（需要下载 PyTorch 和 GPT-2 模型）
- 你可以在 Render Dashboard 查看实时日志
- 部署成功后，会得到一个 URL：`https://attention-surgery.onrender.com`

### 4. 访问应用

部署完成后，直接访问分配的 URL 即可使用应用！

- 前端界面：`https://your-app.onrender.com/`
- 健康检查：`https://your-app.onrender.com/health`
- API 文档：`https://your-app.onrender.com/docs`

## 📦 项目结构

```
xai_final/
├── Dockerfile              # 多阶段构建：前端 + 后端
├── render.yaml             # Render 配置文件
├── frontend/               # React 前端
│   ├── src/
│   ├── package.json        # ✅ 已创建
│   └── vite.config.ts
├── attention_surgery/      # Python FastAPI 后端
│   ├── api.py              # ✅ 已添加静态文件服务
│   ├── core/
│   └── requirements.txt
└── DEPLOY.md               # 本文件
```

## 🔧 部署架构说明

### Dockerfile 多阶段构建

1. **Stage 1**: 使用 Node.js 构建前端（Vite + React）
   - 输出目录：`/frontend/dist`

2. **Stage 2**: Python 后端 + 前端静态文件
   - FastAPI 服务 API 请求（`/api/*`）
   - 同时服务前端静态文件（`/`, `/*`）

### API 路由策略

- `/health` → 健康检查
- `/api/surgery` → 后端 API
- `/` → 前端 index.html
- `/assets/*` → 前端静态资源（JS, CSS）
- 所有其他路由 → SPA 路由（返回 index.html）

## 💰 费用说明

### Free Plan (免费)
- ✅ 适合演示和测试
- ⚠️ 限制：512 MB RAM，服务会在 15 分钟无活动后休眠
- ⚠️ **注意**：GPT-2 模型可能需要更多内存，建议使用 Starter Plan

### Starter Plan ($7/月)
- ✅ 推荐用于此项目
- 1 GB RAM，不会休眠
- 足够运行 GPT-2 Small 模型

## 🐛 常见问题

### 1. 部署失败：Out of Memory

**解决方案**：
- 升级到 Starter Plan（1 GB RAM）
- 或修改代码延迟加载模型

### 2. 前端无法访问

**检查**：
- 确认 `frontend/dist` 目录在 Docker 中存在
- 查看 Render 日志：是否有 "Frontend dist directory not found" 警告

### 3. API 请求失败

**检查**：
- 前端是否正确配置 API URL（应该使用相对路径 `/api/surgery`）
- 查看 Network 标签的请求 URL

### 4. 服务启动慢

**原因**：
- 首次启动需要下载 GPT-2 模型（约 500MB）
- 使用 Render 的持久化存储（disk）缓存模型

## 🔄 更新部署

推送新代码到 GitHub 后，Render 会自动重新部署：

```bash
git add .
git commit -m "Update features"
git push
```

## 📚 参考资源

- [Render 文档](https://render.com/docs)
- [Docker 多阶段构建](https://docs.docker.com/build/building/multi-stage/)
- [FastAPI 静态文件](https://fastapi.tiangolo.com/tutorial/static-files/)

---

**祝部署顺利！** 🎉

如有问题，请查看 Render Dashboard 的日志输出。
