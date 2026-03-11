<template>
  <div class="app-container">
    <header class="app-header">
      <h1>MD to DOCX Converter</h1>
      <div class="header-actions">
        <label class="btn btn-primary">
          <input type="file" accept=".md" @change="handleFileUpload" hidden />
          上传 Markdown
        </label>

        <button class="btn btn-warning" @click="handleConvert" :disabled="isConverting || !markdownContent.trim()">
          转换
        </button>
        <button class="btn btn-success" @click="exportDocx" :disabled="isConverting">
          导出 DOCX
        </button>
        <button class="btn btn-info" @click="printPreview" :disabled="isConverting">
          打印预览
        </button>
      </div>
    </header>
    
    <main class="main-content">
      <div class="editor-panel">
        <div class="panel-header">Markdown 编辑器</div>
        <div ref="editorContainer" class="editor-container"></div>
      </div>
      
      <div class="preview-panel">
        <div class="panel-header">
          DOCX 预览
          <span v-if="isConverting" class="converting-badge">转换中...</span>
        </div>
        <div class="preview-container" ref="previewContainer">
          <div v-show="!docxBlob" class="empty-preview">
            <p>请点击上方「转换」按钮开始转换</p>
          </div>
        </div>
      </div>
    </main>

    <div v-if="error" class="error-toast" @click="error = ''">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as monaco from 'monaco-editor'
import axios from 'axios'
import { renderAsync } from 'docx-preview'

const editorContainer = ref<HTMLElement | null>(null)
const previewContainer = ref<HTMLElement | null>(null)
const markdownContent = ref('# 欢迎使用 MD to DOCX 转换器\n\n开始编辑您的 Markdown 文档...\n')
const docxBlob = ref<Blob | null>(null)
const isConverting = ref(false)
const error = ref('')

let editor: monaco.editor.IStandaloneCodeEditor | null = null

const API_URL = 'http://localhost:6062'

onMounted(async () => {
  if (editorContainer.value) {
    editor = monaco.editor.create(editorContainer.value, {
      value: markdownContent.value,
      language: 'markdown',
      theme: 'vs',
      automaticLayout: true,
      minimap: { enabled: false },
      wordWrap: 'on',
      fontSize: 14,
      lineNumbers: 'on',
      scrollBeyondLastLine: false,
    })

    editor.onDidChangeModelContent(() => {
      const content = editor?.getValue() || ''
      markdownContent.value = content
    })
  }

})

onUnmounted(() => {
  editor?.dispose()
})

async function convertMarkdown(content: string) {
  if (!content.trim()) return
  
  isConverting.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('markdown', content)
    
    const response = await axios.post(`${API_URL}/convert`, formData, {
      responseType: 'blob',
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    docxBlob.value = new Blob([response.data], { 
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
    })
    
    console.log('Blob created:', docxBlob.value.size, 'bytes')
    
    await nextTick()
    
    if (previewContainer.value && docxBlob.value) {
      console.log('Rendering to:', previewContainer.value)
      previewContainer.value.innerHTML = ''
      try {
        const arrayBuffer = await docxBlob.value.arrayBuffer()
        console.log('ArrayBuffer:', arrayBuffer.byteLength, 'bytes')
        await renderAsync(arrayBuffer, previewContainer.value, null, {
          className: 'docx-preview',
          inWrapper: true
        })
        console.log('Render complete')
      } catch (renderError) {
        console.error('Render error:', renderError)
        error.value = '预览渲染失败: ' + String(renderError)
      }
    } else {
      console.log('Missing:', { preview: previewContainer.value, blob: docxBlob.value })
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || '转换失败，请重试'
  } finally {
    isConverting.value = false
  }
}

function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  
  if (!file.name.endsWith('.md')) {
    error.value = '仅支持 Markdown (.md) 文件'
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    const content = e.target?.result as string
    markdownContent.value = content
    editor?.setValue(content)
  }
  reader.readAsText(file)
}

function handleConvert() {
  if (!markdownContent.value.trim()) return
  convertMarkdown(markdownContent.value)
}

async function exportDocx() {
  if (!docxBlob.value) {
    error.value = '请先生成 DOCX 文件'
    return
  }
  
  const url = URL.createObjectURL(docxBlob.value)
  const a = document.createElement('a')
  a.href = url
  a.download = 'document.docx'
  a.click()
  URL.revokeObjectURL(url)
}

async function printPreview() {
  if (!docxBlob.value) {
    error.value = '请先生成 DOCX 文件'
    return
  }

  const printWindow = window.open('', '_blank')
  if (!printWindow) return

  const arrayBuffer = await docxBlob.value.arrayBuffer()
  
  // 将 ArrayBuffer 转换为 Base64（分块处理避免栈溢出）
  const uint8Array = new Uint8Array(arrayBuffer)
  let base64Data = ''
  const chunkSize = 0x8000 // 32KB chunks
  for (let i = 0; i < uint8Array.length; i += chunkSize) {
    const chunk = uint8Array.subarray(i, i + chunkSize)
    base64Data += String.fromCharCode.apply(null, chunk as any)
  }
  base64Data = btoa(base64Data)

  printWindow.document.write(`
    <html>
      <head>
        <title>打印预览</title>
        <script src="https://unpkg.com/jszip@3.10.1/dist/jszip.min.js"><\/script>
        <script src="https://unpkg.com/docx-preview@0.3.7/dist/docx-preview.min.js"><\/script>
        <style>
          body { margin: 20px; }
          .docx-preview { font-family: Calibri, sans-serif; }
          @media print { body { margin: 0; } }
        </style>
      </head>
      <body>
        <div id="container"></div>
        <script>
          try {
            const base64Data = '${base64Data}';
            const binaryString = atob(base64Data);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
              bytes[i] = binaryString.charCodeAt(i);
            }
            const arrayBuffer = bytes.buffer;
            
            function waitForDocxAndRender() {
              if (typeof docx !== 'undefined' && typeof JSZip !== 'undefined') {
                docx.renderAsync(arrayBuffer, document.getElementById('container'), null, {
                  className: 'docx-preview',
                  inWrapper: true
                }).then(() => {
                  setTimeout(() => window.print(), 500);
                }).catch(err => {
                  console.error('渲染失败:', err);
                  document.getElementById('container').innerHTML = '<p style="color: red;">文档渲染失败: ' + err.message + '</p>';
                });
              } else {
                setTimeout(waitForDocxAndRender, 100);
              }
            }
            waitForDocxAndRender();
          } catch (err) {
            console.error('初始化失败:', err);
            document.getElementById('container').innerHTML = '<p style="color: red;">初始化失败: ' + err.message + '</p>';
          }
        <\/script>
      </body>
    </html>
  `)
  printWindow.document.close()
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f5f5f5;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  z-index: 100;
}

.app-header h1 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary { background: #409eff; color: white; }
.btn-primary:hover:not(:disabled) { background: #66b1ff; }

.btn-secondary { background: #909399; color: white; }
.btn-secondary:hover:not(:disabled) { background: #a6a9ad; }

.btn-success { background: #67c23a; color: white; }
.btn-success:hover:not(:disabled) { background: #85ce61; }

.btn-warning { background: #e6a23c; color: white; }
.btn-warning:hover:not(:disabled) { background: #ebb563; }

.btn-info { background: #909399; color: white; }
.btn-info:hover:not(:disabled) { background: #a6a9ad; }

.template-name {
  font-size: 12px;
  color: #666;
  padding: 4px 8px;
  background: #f0f0f0;
  border-radius: 4px;
}

.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.editor-panel, .preview-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-panel { border-right: 1px solid #ddd; }

.panel-header {
  padding: 12px 16px;
  background: #fff;
  border-bottom: 1px solid #ddd;
  font-weight: 600;
  font-size: 14px;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.converting-badge {
  font-size: 12px;
  color: #e6a23c;
  font-weight: normal;
}

.editor-container { flex: 1; overflow: hidden; }

.preview-container {
  flex: 1;
  overflow: auto;
  padding: 16px;
  background: #fff;
}

.empty-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.empty-preview .hint {
  font-size: 12px;
  margin-top: 8px;
}

.error-toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  padding: 12px 24px;
  background: #f56c6c;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  z-index: 1000;
}
</style>
