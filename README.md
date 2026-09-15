# Web to Markdown Converter

将网页或 HTML 文件转换为 Markdown 格式的工具。**现已支持 JavaScript 动态内容、智能菜单移除和完整 URL 转换。**

## 功能特性

✨ **核心功能**
- ✅ 从 URL 获取网页内容
- ✅ 支持本地 HTML 文件转换
- ✅ 自动清理 HTML（移除脚本、样式、导航等干扰元素）
- ✅ 保留链接和图片引用
- ✅ 支持表格转换
- ✅ 输出到文件或标准输出

🚀 **增强功能（v2.0）**
- 🎯 **JavaScript 渲染** - 使用 Selenium 抓取动态加载的内容
- 🎯 **智能菜单移除** - 自动识别并移除导航、侧边栏、登录按钮等
- 🎯 **URL 自动转换** - 将相对链接自动转换为完整绝对 URL
- 🎯 **内容识别** - 智能查找文章主体内容

## 安装

### 前置要求
- Python 3.7+
- pip
- Chrome 浏览器（可选，用于 JavaScript 渲染）
- ChromeDriver（可选，用于 JavaScript 渲染）

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/xujingrong021218-ship-it/web-to-markdown.git
cd web-to-markdown

# 安装依赖
pip install -r requirements.txt

# （可选）安装 ChromeDriver 用于 JavaScript 渲染
# macOS
brew install chromedriver

# Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# 或从官方下载: https://chromedriver.chromium.org/
```

## 使用方法

### 基础用法

#### 1. 简单转换（无 JavaScript）
```bash
python web_to_markdown.py https://example.com
```

#### 2. 转换并保存到文件
```bash
python web_to_markdown.py https://example.com -o output.md
```

#### 3. 使用 JavaScript 渲染（处理动态内容）
```bash
python web_to_markdown.py https://example.com --js -o output.md
```

#### 4. 保留导航元素
```bash
python web_to_markdown.py https://example.com --keep-navbar -o output.md
```

#### 5. 转换本地 HTML 文件
```bash
python web_to_markdown.py input.html -f -o output.md
```

#### 6. 详细日志输出
```bash
python web_to_markdown.py https://example.com --js -v
```

### 命令行选项

```
positional arguments:
  input                     URL 或文件路径

optional arguments:
  -h, --help                显示帮助信息
  -o, --output OUTPUT       输出文件路径（默认：输出到终端）
  -f, --file                输入是本地 HTML 文件（默认：当作 URL）
  -t, --timeout TIMEOUT     请求超时时间，单位秒（默认：10）
  --js                      启用 JavaScript 渲染（需要 Selenium/ChromeDriver）
  --keep-navbar             保留导航/侧边栏元素（默认：移除）
  -v, --verbose             显示详细日志
```

## 实际示例

### 示例 1：抓取 GitHub 项目（带动态内容和菜单）
```bash
python web_to_markdown.py https://github.com/owner/repo --js -o github-page.md
```

### 示例 2：转换技术文档（相对链接自动转换）
```bash
python web_to_markdown.py https://docs.python.org/3/ -o python-docs.md
```

### 示例 3：抓取复杂网站（移除菜单和广告）
```bash
python web_to_markdown.py https://medium.com/article --js -v
```

### 示例 4：批量转换
```bash
for url in "https://example1.com" "https://example2.com"; do
    python web_to_markdown.py "$url" -o "$(echo $url | md5sum | cut -d' ' -f1).md"
done
```

## 在 Python 代码中使用

### 基础用法
```python
from web_to_markdown import WebToMarkdownConverter

# 创建转换器实例
converter = WebToMarkdownConverter(timeout=10)

# 转换 URL
markdown = converter.convert_url('https://example.com')
print(markdown)
```

### 启用 JavaScript 渲染
```python
# 启用 JavaScript 渲染以支持动态内容
converter = WebToMarkdownConverter(timeout=15, use_js=True)
markdown = converter.convert_url('https://example.com')
```

### 保留导航元素
```python
# 保留导航和侧边栏
converter = WebToMarkdownConverter(remove_navbar=False)
markdown = converter.convert_url('https://example.com')
```

### 转换本地文件
```python
# 本地文件相对链接会自动转换
markdown = converter.convert_file('input.html')
```

## 工作原理

### JavaScript 渲染流程
1. 使用 Selenium 启动无头浏览器
2. 等待页面加载完成
3. 获取渲染后的 HTML
4. 提取和转换内容

### 内容清理流程
1. 移除 `<script>`, `<style>`, `<meta>`, `<noscript>`, `<iframe>` 标签
2. 移除导航/侧边栏（可选）
3. 相对 URL 转换为绝对 URL
4. HTML 转换为 Markdown

### 智能导航识别
自动检测和移除：
- `<nav>`, `<header>`, `<footer>` 标签
- `.navbar`, `.sidebar`, `.navigation` 类
- `[role="navigation"]`, `[role="complementary"]` 属性
- 面包屑导航、搜索框、广告等

## 已知局限和改进方案

### ⚠️ 当前局限

| 问题 | 解决方案 |
|------|--------|
| JavaScript 动态加载内容 | 使用 `--js` 启用 Selenium 渲染 |
| GitHub 等复杂网页的菜单混入 | 自动启用 `remove_navbar`（默认行为） |
| 相对链接没转换 | 自动处理，支持 `file://` URI |
| 需要登录/验证码的网站 | ❌ 暂不支持（需手动处理 cookies） |

### 🔄 后续改进计划

- [ ] Cookie/Session 管理（支持登录状态）
- [ ] 代理支持（绕过 IP 限制）
- [ ] 自定义 CSS 选择器
- [ ] 输出格式选择（RST、Org、等）
- [ ] 图片下载和本地化
- [ ] 并发批量转换

## 技术栈

- **requests** - HTTP 请求库
- **BeautifulSoup4** - HTML 解析
- **html2text** - HTML 到 Markdown 转换
- **Selenium** - 浏览器自动化（JavaScript 渲染）
- **ChromeDriver** - Chrome 浏览器驱动

## 常见问题

### Q: 怎么安装 ChromeDriver？
A: 
```bash
# macOS
brew install chromedriver

# Ubuntu
sudo apt-get install chromium-chromedriver

# 或手动下载：https://chromedriver.chromium.org/
```

### Q: JavaScript 渲染很慢？
A: 正常现象。可调整 `--timeout` 参数或使用 `--keep-navbar` 加快处理。

### Q: 转换后格式不理想？
A: 可以修改 `web_to_markdown.py` 中的：
- `nav_selectors` - 调整要移除的元素
- `content_selectors` - 调整内容识别规则
- `html2text.HTML2Text()` 配置 - 调整 Markdown 输出格式

### Q: 如何处理需要登录的网站？
A: 目前不支持。可以：
1. 手动登录后保存 HTML 文件，用 `-f` 参数转换
2. 在自定义脚本中使用 Selenium 的 cookie 功能

### Q: 支持其他格式转换吗？
A: 当前专注于 Markdown。可扩展支持：
- reStructuredText (RST)
- Org Mode
- AsciiDoc
- 等其他格式

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 快速参考

```bash
# 最常用的命令
python web_to_markdown.py <url> --js -o output.md

# 调试模式
python web_to_markdown.py <url> --js -v

# 保持原样（不移除菜单）
python web_to_markdown.py <url> --keep-navbar
```
