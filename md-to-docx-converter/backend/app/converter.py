import os
import re
import base64
from io import BytesIO

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from mistune import Markdown, Renderer
import html


class DocxRenderer:
    """Renders Markdown content to DOCX document."""
    
    def __init__(self):
        self.options = {}
        self.placeholder = {}
        self.document = Document()
        self._setup_styles()
        self.current_paragraph = None

    def _setup_styles(self):
        """设置文档默认样式"""
        # 设置默认字体
        style = self.document.styles['Normal']
        font = style.font
        font.name = 'Microsoft YaHei'
        font.size = Pt(11)
        
        # 设置中文字体
        self._set_chinese_font(style, 'Microsoft YaHei')
        
        # 设置段落格式
        paragraph_format = style.paragraph_format
        paragraph_format.line_spacing = 1.5
        paragraph_format.space_after = Pt(8)
        paragraph_format.space_before = Pt(0)

    def _set_chinese_font(self, style, font_name):
        """设置中文字体"""
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:eastAsia'), font_name)
        style.element.rPr.append(rFonts)

    def _set_cell_shading(self, cell, color):
        """设置单元格背景色"""
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), color)
        cell._tc.get_or_add_tcPr().append(shading_elm)

    def _add_heading(self, text: str, level: int):
        """添加标题"""
        if level > 6:
            level = 6
        clean_text = self._strip_html(text)
        heading = self.document.add_heading(level=level)
        run = heading.add_run(clean_text)
        run.font.name = 'Microsoft YaHei'
        run.font.bold = True
        
        # 设置标题字体大小
        sizes = {1: Pt(20), 2: Pt(18), 3: Pt(16), 4: Pt(14), 5: Pt(12), 6: Pt(11)}
        run.font.size = sizes.get(level, Pt(11))
        
        # 设置中文字体
        self._set_run_chinese_font(run, 'Microsoft YaHei')
        
        # 设置标题颜色
        if level <= 2:
            run.font.color.rgb = RGBColor(0, 51, 102)  # 深蓝色
        
        # 设置段后间距
        heading.paragraph_format.space_after = Pt(12)
        heading.paragraph_format.space_before = Pt(12)
        
        return heading

    def _set_run_chinese_font(self, run, font_name):
        """设置 run 的中文字体"""
        r = run._element
        rPr = r.get_or_add_rPr()
        rFonts = OxmlElement('w:rFonts')
        rFonts.set(qn('w:eastAsia'), font_name)
        rPr.insert(0, rFonts)

    def _add_paragraph_with_html(self, html_text: str):
        """解析 HTML 文本并添加到段落，支持 <strong>, <code>, <a> 等标签"""
        p = self.document.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(8)
        
        # 解析内联 HTML 标签
        pattern = r'(<[^>]+>)|([^<]+)'
        tokens = re.findall(pattern, html_text)
        
        bold = False
        italic = False
        code = False
        
        for tag, text in tokens:
            if tag:
                tag_lower = tag.lower()
                if tag_lower in ['<strong>', '<b>']:
                    bold = True
                elif tag_lower in ['</strong>', '</b>']:
                    bold = False
                elif tag_lower in ['<em>', '<i>']:
                    italic = True
                elif tag_lower in ['</em>', '</i>']:
                    italic = False
                elif tag_lower == '<code>':
                    code = True
                elif tag_lower == '</code>':
                    code = False
            elif text:
                clean_text = html.unescape(text)
                if clean_text:
                    run = p.add_run(clean_text)
                    run.font.name = 'Microsoft YaHei'
                    self._set_run_chinese_font(run, 'Microsoft YaHei')
                    
                    if bold:
                        run.font.bold = True
                    if italic:
                        run.font.italic = True
                    if code:
                        run.font.name = 'Consolas'
                        run.font.size = Pt(10)
                        # 代码使用灰色
                        run.font.color.rgb = RGBColor(80, 80, 80)
        
        return p

    def _strip_html(self, html_text: str) -> str:
        """去除 HTML 标签"""
        clean = re.sub(r'<[^>]+>', '', html_text)
        return html.unescape(clean)

    def _add_paragraph(self, text: str):
        """添加段落，自动处理 HTML"""
        if '<' in text and '>' in text:
            return self._add_paragraph_with_html(text)
        else:
            p = self.document.add_paragraph()
            run = p.add_run(html.unescape(text))
            run.font.name = 'Microsoft YaHei'
            self._set_run_chinese_font(run, 'Microsoft YaHei')
            p.paragraph_format.line_spacing = 1.5
            p.paragraph_format.space_after = Pt(8)
            return p

    def _add_unordered_list_item(self, text: str):
        """添加无序列表项"""
        p = self.document.add_paragraph(style='List Bullet')
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        
        if '<' in text and '>' in text:
            clean_text = self._strip_html(text)
            run = p.add_run(clean_text)
        else:
            run = p.add_run(html.unescape(text))
        
        run.font.name = 'Microsoft YaHei'
        self._set_run_chinese_font(run, 'Microsoft YaHei')
        return p

    def _add_ordered_list_item(self, text: str, num: int):
        """添加有序列表项"""
        p = self.document.add_paragraph(style='List Number')
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.first_line_indent = Cm(-0.5)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(4)
        
        if '<' in text and '>' in text:
            clean_text = self._strip_html(text)
            run = p.add_run(clean_text)
        else:
            run = p.add_run(html.unescape(text))
        
        run.font.name = 'Microsoft YaHei'
        self._set_run_chinese_font(run, 'Microsoft YaHei')
        return p

    def _add_code_block(self, code: str, language: str = ""):
        """添加代码块"""
        # 添加语言标签
        if language:
            lang_p = self.document.add_paragraph()
            lang_run = lang_p.add_run(f'{language}')
            lang_run.font.name = 'Consolas'
            lang_run.font.size = Pt(9)
            lang_run.font.color.rgb = RGBColor(100, 100, 100)
            lang_p.paragraph_format.space_after = Pt(2)
        
        # 代码内容
        p = self.document.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.shading.background_pattern = None
        
        # 添加代码背景色
        shading_elm = OxmlElement('w:shd')
        shading_elm.set(qn('w:fill'), 'F5F5F5')
        p.paragraph_format.element.get_or_add_pPr().append(shading_elm)
        
        run = p.add_run(html.unescape(code))
        run.font.name = 'Consolas'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(50, 50, 50)
        
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(6)
        
        return p

    def _add_table(self, headers: list, rows: list):
        """添加表格"""
        table = self.document.add_table(rows=1, cols=len(headers))
        table.style = 'Table Grid'
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        
        # 设置表头
        hdr_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            clean_header = self._strip_html(header)
            cell = hdr_cells[i]
            cell.text = clean_header
            
            # 设置表头样式
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.name = 'Microsoft YaHei'
                    run.font.size = Pt(11)
                    self._set_run_chinese_font(run, 'Microsoft YaHei')
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # 设置表头背景色
            self._set_cell_shading(cell, 'E8F4FC')
        
        # 添加数据行
        for row_data in rows:
            row_cells = table.add_row().cells
            for i, cell_data in enumerate(row_data):
                clean_data = self._strip_html(cell_data)
                cell = row_cells[i]
                cell.text = clean_data
                
                # 设置单元格样式
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        run.font.name = 'Microsoft YaHei'
                        run.font.size = Pt(10)
                        self._set_run_chinese_font(run, 'Microsoft YaHei')
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
                # 设置单元格边距
                cell.vertical_alignment = 1  # 垂直居中
        
        # 设置表格整体边距
        for row in table.rows:
            for cell in row.cells:
                cell.paragraphs[0].paragraph_format.space_before = Pt(4)
                cell.paragraphs[0].paragraph_format.space_after = Pt(4)
        
        return table

    def _add_blockquote(self, text: str):
        """添加引用块"""
        p = self.document.add_paragraph()
        p.paragraph_format.left_indent = Cm(1)
        p.paragraph_format.right_indent = Cm(0.5)
        
        # 添加左边框效果
        pPr = p.paragraph_format.element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        left = OxmlElement('w:left')
        left.set(qn('w:val'), 'single')
        left.set(qn('w:sz'), '24')
        left.set(qn('w:space'), '4')
        left.set(qn('w:color'), 'CCCCCC')
        pBdr.append(left)
        pPr.append(pBdr)
        
        clean_text = self._strip_html(text)
        run = p.add_run(clean_text)
        run.font.italic = True
        run.font.color.rgb = RGBColor(100, 100, 100)
        run.font.name = 'Microsoft YaHei'
        self._set_run_chinese_font(run, 'Microsoft YaHei')
        
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(8)
        
        return p

    def _add_image(self, image_data: bytes, width: float | None = None):
        """添加图片"""
        image_stream = BytesIO(image_data)
        try:
            if width:
                self.document.add_picture(image_stream, width=Inches(width))
            else:
                self.document.add_picture(image_stream, width=Inches(5))
        except Exception:
            pass
        return self.document.paragraphs[-1]

    def render(self, markdown_text: str) -> bytes:
        renderer = CustomRenderer(self)
        md = Markdown(renderer=renderer)
        md(markdown_text)
        
        output = BytesIO()
        self.document.save(output)
        output.seek(0)
        return output.getvalue()


class CustomRenderer(Renderer):
    def __init__(self, docx_renderer: DocxRenderer):
        super().__init__()
        self.docx = docx_renderer

    def heading(self, text, level):
        self.docx._add_heading(text, level)
        return ""

    def paragraph(self, text):
        if text.strip():
            self.docx._add_paragraph(text)
        return ""

    def list_item(self, text):
        self.docx._add_unordered_list_item(text)
        return ""

    def code_block(self, text, lang=None, info=None):
        self.docx._add_code_block(text, lang or "")
        return ""

    def block_quote(self, text):
        self.docx._add_blockquote(text)
        return ""

    def table(self, header, body):
        import re
        
        # 从 header 中提取表头
        header_cells = re.findall(r'<th>(.*?)</th>', header)
        headers = [h.strip() for h in header_cells]
        
        # 从 body 中提取行数据
        rows = []
        row_matches = re.findall(r'<tr>(.*?)</tr>', body, re.DOTALL)
        for row_html in row_matches:
            cells = re.findall(r'<td>(.*?)</td>', row_html)
            if cells:
                rows.append([c.strip() for c in cells])
        
        if headers and rows:
            self.docx._add_table(headers, rows)
        return ""

    def link(self, link, title=None, text=None):
        # 链接显示为 "文本 (链接地址)"
        display_text = text or link
        full_text = f"{display_text} ({link})"
        self.docx._add_paragraph(full_text)
        return ""

    def image(self, src, title=None, text=None):
        try:
            if src.startswith('data:image'):
                base64_data = src.split(',')[1]
                image_data = base64.b64decode(base64_data)
                self.docx._add_image(image_data)
            elif os.path.exists(src):
                with open(src, 'rb') as f:
                    self.docx._add_image(f.read())
        except Exception:
            pass
        return ""

    def linebreak(self):
        self.docx.document.add_paragraph()
        return ""

    def inline_html(self, text):
        return text
    
    def text(self, text):
        return text


def convert_markdown_to_docx(markdown_text: str) -> bytes:
    """Convert Markdown text to DOCX document bytes.
    
    Args:
        markdown_text: The Markdown content to convert
        
    Returns:
        bytes: The generated DOCX file content
    """
    docx_renderer = DocxRenderer()
    renderer = CustomRenderer(docx_renderer)
    md = Markdown(renderer=renderer)
    md(markdown_text)
    
    output = BytesIO()
    docx_renderer.document.save(output)
    output.seek(0)
    return output.getvalue()
