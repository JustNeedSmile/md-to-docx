# md-to-docx

本项目使用 OpenSpec 开发流程进行管理和开发。包含前后端开发。

## 前端开发

This template should help get you started developing with Vue 3 in Vite.


## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

## 后端开发

本项目后端使用 FastAPI 框架开发。

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
