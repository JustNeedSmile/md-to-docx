## ADDED Requirements

### Requirement: 移除模板上传功能
该应用 SHALL 不再支持用户上传自定义 DOCX 模板文件，简化系统功能。

#### Scenario: 前端移除模板按钮
- **WHEN** 用户访问应用界面
- **THEN** 不显示"上传模板"按钮
- **AND** 不显示模板文件名

#### Scenario: 后端移除模板参数
- **WHEN** 调用转换 API `/convert`
- **THEN** 不再接收 `template` 参数
- **AND** 使用默认样式进行转换

#### Scenario: 转换器简化
- **WHEN** 执行 Markdown 到 DOCX 转换
- **AND** 不指定模板文件
- **THEN** 使用系统内置默认样式生成文档
- **AND** DocxRenderer 不接收 template_path 参数

### Requirement: 转换功能 SHALL 保持正常
移除模板功能后，核心转换功能 SHALL 保持正常工作。

#### Scenario: Markdown 转换
- **WHEN** 用户提供有效的 Markdown 内容
- **THEN** 正确转换为 DOCX 格式
- **AND** 应用默认样式

#### Scenario: 导出功能
- **WHEN** 用户点击导出按钮
- **THEN** 下载的 DOCX 文件使用默认样式
