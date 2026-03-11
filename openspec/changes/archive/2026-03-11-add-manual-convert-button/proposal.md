## Why

当前用户在上传 MD 文档后，系统会自动立即转换为 DOCX。这种自动转换行为在用户需要先检查或编辑文档内容时不够灵活，尤其是在处理大型文档（100页）时，用户希望在确认内容正确后再进行转换操作。

## What Changes

- 移除 Markdown 上传后的自动转换行为
- 添加独立的"转换"按钮，用户上传 MD 或编辑内容后需手动点击才会执行转换
- 转换按钮在内容为空或正在转换时禁用
- 保留现有的模板上传功能和导出功能

## Capabilities

### New Capabilities
- `manual-convert-trigger`: 新增手动转换触发机制，用户需点击转换按钮才执行 MD 到 DOCX 的转换

### Modified Capabilities
- 无

## Impact

- 前端文件：`frontend/src/App.vue` - 修改上传和转换逻辑
- 现有功能不受影响：模板上传、导出 DOCX、打印预览功能保持不变
