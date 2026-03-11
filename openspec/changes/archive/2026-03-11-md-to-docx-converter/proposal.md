## Why

在日常工作中，经常需要将Markdown格式的技术文档转换为Word(.docx)格式，以便于审阅、批注和打印。Markdown编辑器和Word各有优势，一个可靠的转换工具可以桥接两者之间的 gap，提高文档流转效率。用户需要一个Web界面来实时预览和编辑转换结果。

## What Changes

- 开发一个全Python技术的Web应用（FastAPI + Vue 3）
- 用户可以通过界面上传Markdown文件或在线编辑
- 左侧显示Markdown源码，右侧实时显示转换后的DOCX预览
- 支持在线编辑Markdown并即时更新预览
- 支持导出DOCX文件
- 支持自定义DOCX样式模板
- 支持打印预览和打印功能
- 不支持批量转换，仅支持单文件操作
- 优化大文档（100页左右）加载和渲染性能

## Capabilities

### New Capabilities

- **md-to-docx-web**: Web端Markdown转DOCX转换应用，支持实时预览、编辑、打印和自定义模板

### Modified Capabilities

无

## Impact

- 新增Web应用项目（全Python技术栈）
- 前端：Vue 3 + TypeScript
- 后端：FastAPI + Python转换服务
- 需要处理大文档性能问题
