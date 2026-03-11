# md-to-docx

本项目使用 OpenSpec 开发流程进行管理和开发，包含前后端开发。

## 项目简介

Markdown 转 DOCX 工具是一个在线转换工具，支持将 Markdown 文档实时转换为 Word 文档。主要功能包括：

- **文件上传**：支持文件选择上传和拖拽上传
- **Markdown 编辑**：左侧实时编辑区域，支持大文档虚拟滚动
- **DOCX 预览**：右侧实时预览，支持分页加载
- **元素转换**：支持标题、有序/无序列表、代码块、表格、链接、图片、引用块等
- **样式模板**：支持默认模板和自定义模板
- **DOCX 导出**：一键下载转换后的 Word 文档

## 技术栈

- **前端**：Vue 3 + TypeScript + Vite
- **后端**：FastAPI (Python)

## 前端开发

### 环境要求

- Node.js 18+
- npm 9+

### 项目 Setup

```sh
cd frontend
npm install
```

### 启动开发服务器

```sh
npm run dev
```

前端服务默认运行在 http://localhost:5173

### 生产环境构建

```sh
npm run build
```

## 后端开发

### 环境要求

- Python 3.11+

### 项目 Setup

```sh
cd backend
pip install -r requirements.txt
```

### 启动开发服务器

```sh
cd backend
uvicorn app.main:app --reload
```

后端服务默认运行在 http://localhost:8000

### 生产环境部署

```sh
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API 接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/convert` | POST | 将 Markdown 转换为 DOCX |

### 请求示例

```bash
curl -X POST "http://localhost:8000/convert" \
  -F "markdown=# Hello World\n\nThis is a test."
```
