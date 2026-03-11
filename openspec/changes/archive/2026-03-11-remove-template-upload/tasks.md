## 1. 前端修改

- [x] 1.1 移除 App.vue 中的"上传模板"按钮及相关 label 元素
- [x] 1.2 移除 templateFile、templateName 响应式变量
- [x] 1.3 移除 handleTemplateUpload 函数
- [x] 1.4 从 convertMarkdown 函数中移除模板文件处理逻辑
- [x] 1.5 移除模板名称显示的 span 元素

## 2. 后端 API 修改

- [x] 2.1 修改 main.py 的 /convert 接口，移除 template 参数
- [x] 2.2 简化 convert 端点，不再接收模板文件

## 3. 转换器简化

- [x] 3.1 修改 converter.py 的 DocxRenderer.__init__，移除 template_path 参数
- [x] 3.2 简化 convert_markdown_to_docx 函数签名，移除 template_path 参数
- [x] 3.3 更新函数文档字符串

## 4. 测试验证

- [x] 4.1 验证前端界面不再显示模板上传按钮
- [x] 4.2 验证 Markdown 转换功能正常工作
- [x] 4.3 验证 DOCX 导出功能正常
