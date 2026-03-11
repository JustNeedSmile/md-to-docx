## ADDED Requirements

### Requirement: Manual conversion trigger
The system SHALL require users to manually click a "Convert" button to trigger the Markdown to DOCX conversion, rather than automatically converting upon file upload or content change.

#### Scenario: User uploads MD file
- **WHEN** user uploads a Markdown file via the file picker
- **THEN** the file content is loaded into the editor
- **AND** the system does NOT automatically convert to DOCX
- **AND** the preview area shows a prompt instructing user to click the Convert button

#### Scenario: User edits MD content
- **WHEN** user edits content in the Monaco editor
- **THEN** the system does NOT automatically convert to DOCX
- **AND** the existing DOCX preview remains unchanged until user clicks Convert

#### Scenario: User clicks Convert button
- **WHEN** user clicks the "Convert" button with valid Markdown content
- **THEN** the system calls the conversion API
- **AND** the DOCX preview is updated with the converted result
- **AND** the Convert button shows a loading state during conversion

#### Scenario: Convert button disabled state
- **WHEN** the Markdown content is empty
- **THEN** the Convert button SHALL be disabled
- **AND** clicking the button has no effect

#### Scenario: Convert button during conversion
- **WHEN** a conversion is in progress
- **THEN** the Convert button SHALL be disabled
- **AND** a "Converting..." indicator is displayed

### Requirement: Preview area prompt
The preview area SHALL display a helpful prompt to guide users to click the Convert button when no conversion has been performed yet.

#### Scenario: Initial empty preview
- **WHEN** no conversion has been performed (initial state or after content change)
- **THEN** the preview area displays: "请点击上方「转换」按钮开始转换"
