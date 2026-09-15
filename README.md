# Web to Markdown Converter

将网页或 HTML 文件转换为 Markdown 格式的工具。

## 功能特性

✨ **核心功能**
- 从 URL 获取网页内容
- 支持本地 HTML 文件转换
- 自动清理 HTML（移除脚本、样式、导航等干扰元素）
- 保留链接和图片引用
- 支持表格转换
- 输出到文件或标准输出

## 安装

### 前置要求
- Python 3.7+
- pip

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/xujingrong021218-ship-it/web-to-markdown.git
cd web-to-markdown

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基础用法

#### 1. 转换网页并输出到终端
```bash
python web_to_markdown.py https://example.com
```

#### 2. 转换网页并保存到文件
```bash
python web_to_markdown.py https://example.com -o output.md
```

#### 3. 转换本地 HTML 文件
```bash
python web_to_markdown.py input.html -f
```

#### 4. 转换本地文件并保存结果
```bash
python web_to_markdown.py input.html -f -o output.md
```

### 命令行选项

```
positional arguments:
  input                URL 或文件路径

optional arguments:
  -h, --help           显示帮助信息
  -o, --output OUTPUT  输出文件路径（默认：输出到终端）
  -f, --file           输入是本地 HTML 文件（默认：当作 URL）
  -t, --timeout TIMEOUT
                       请求超时时间，单位秒（默认：10）
```

## 实际示例

```bash
# 转换 GitHub 项目主页
python web_to_markdown.py https://github.com/xujingrong021218-ship-it/web-to-markdown -o github-page.md

# 转换技术文档
python web_to_markdown.py https://docs.python.org/3/ -o python-docs.md

# 批量转换（使用脚本）
for url in "https://example1.com" "https://example2.com"; do
    python web_to_markdown.py "$url" -o "$(echo $url | md5sum | cut -d' ' -f1).md"
done
```

## 在 Python 代码中使用

```python
from web_to_markdown import WebToMarkdownConverter

# 创建转换器实例
converter = WebToMarkdownConverter(timeout=10)

# 转换 URL
markdown = converter.convert_url('https://example.com')
print(markdown)

# 或转换本地文件
markdown = converter.convert_file('input.html')
print(markdown)
```

## 技术栈

- **requests** - HTTP 请求库
- **BeautifulSoup4** - HTML 解析
- **html2text** - HTML 到 Markdown 转换
- **markdownify** - 备选转换库

## 常见问题

### Q: 转换后格式不理想？
A: 可以调整 `web_to_markdown.py` 中的 `html2text.HTML2Text()` 配置参数来优化转换效果。

### Q: 如何只提取特定部分内容？
A: 修改 `clean_html()` 方法，添加更精确的 CSS 选择器来保留/移除特定元素。

### Q: 支持其他格式转换吗？
A: 当前专注于 Markdown，但可扩展支持其他格式（如 ReStructuredText、HTML 等）。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
