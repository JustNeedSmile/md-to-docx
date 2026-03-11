## Context

本项目旨在开发一个Web应用，将Markdown文档转换为Word(.docx)格式，并提供实时预览功能。用户可以通过界面上传Markdown文件，在左侧编辑源码，右侧实时查看转换结果。

## Goals / Non-Goals

**Goals:**
- 实现Markdown到DOCX的高质量转换，保持文档结构和格式
- 支持常见的Markdown元素：标题、段落、列表、代码块、表格、链接、图片、引用块
- 提供Web界面，左侧Markdown编辑器，右侧DOCX预览
- 支持在线编辑Markdown并即时更新预览
- 优化大文档（100页左右）加载和渲染性能
- 支持导出DOCX文件
- 支持自定义DOCX样式模板
- 支持打印预览和打印功能
- 全Python技术栈，确保稳定可靠

**Non-Goals:**
- 不支持批量转换
- 不支持DOCX反向转换回Markdown
- 不支持多人协作编辑
- 不需要用户认证

## Decisions

### 1. 技术栈选择: 全Python方案

**选择: FastAPI + Vue 3**
- 后端：FastAPI（高性能异步框架）+ Python转换服务一体化
- 前端：Vue 3 + TypeScript（保持前端体验）
- Python生态成熟，python-docx、mistune等库稳定可靠
- 避免Java/Python混合带来的复杂度

### 2. 后端架构

**选择: FastAPI一体化架构**
- FastAPI提供Web服务，同时处理转换逻辑
- 使用python-docx生成DOCX
- 使用mistune解析Markdown
- 使用pygments处理代码高亮
- 单一Python进程，无需进程间通信

### 3. 大文档性能优化策略

**选择: 分页加载 + 虚拟滚动 + 增量更新**
- DOCX预览采用分页渲染，避免一次性加载全部内容
- Markdown编辑器使用虚拟滚动处理大文件
- 转换请求使用防抖处理，避免频繁请求
- 后端使用异步处理转换大文档

### 4. DOCX预览方案

**选择: 使用docx-preview库在前端渲染**
- `docx-preview` 可以在浏览器中直接渲染DOCX
- 无需后端返回完整DOCX即可预览
- 支持实时更新预览

### 5. 图片处理策略

**选择: Base64编码传输**
- Markdown中的本地图片转换为Base64编码
- 转换时内嵌到DOCX中
- 避免路径问题

### 6. 样式模板方案

**选择: 使用python-docx模板**
- 提供默认样式模板
- 支持用户上传自定义.docx模板
- 模板中的样式（标题、正文、字体）会被应用到转换结果

### 7. 打印方案

**选择: 浏览器打印 + docx-preview**
- 使用docx-preview在浏览器中渲染DOCX
- 调用浏览器原生打印功能
- 支持打印预览

## Risks / Trade-offs

| 风险 | 描述 | 缓解措施 |
|------|------|----------|
| 大文档性能 | 100页文档加载和转换耗时 | 分页渲染、防抖、进度提示 |
| 预览同步延迟 | 编辑与预览存在延迟 | 使用防抖+增量更新优化 |
| 图片丢失 | Markdown引用外部图片 | 提示用户使用本地图片或Base64 |

## Migration Plan

1. 创建前端项目（Vue 3 + TypeScript）
2. 创建后端项目（FastAPI）
3. 实现Python转换引擎
4. 前后端联调
5. 添加样式模板支持
6. 添加打印功能
7. 性能优化（分页、防抖）
8. 部署测试
