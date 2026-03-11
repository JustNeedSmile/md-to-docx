## Why

当前前端界面包含一个"上传模板"按钮，允许用户上传自定义 DOCX 模板文件。根据用户反馈，此功能不再需要，应当移除以简化用户界面并减少功能复杂度。

## What Changes

- **移除前端"上传模板"按钮** - 删除 App.vue 中的模板上传按钮及相关 UI 元素
- **移除模板文件处理逻辑** - 删除前端 templateFile、templateName 等状态变量及相关处理函数
- **移除后端模板参数支持** - 从 API 接口中移除 template 参数处理
- **简化转换逻辑** - 转换器不再需要处理模板路径参数

## Capabilities

### New Capabilities
- 无新增功能

### Modified Capabilities
- 无修改的功能规范（仅移除已有功能，不涉及行为变更）

## Impact

- **前端**: App.vue 文件需要修改，移除模板相关 UI 和逻辑
- **后端**: main.py 和 converter.py 需要简化，移除模板参数处理
- **API**: /convert 接口不再接受 template 参数
- **用户体验**: 界面更简洁，功能更聚焦
