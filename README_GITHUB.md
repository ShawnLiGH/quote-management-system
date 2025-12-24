# 设备报价单管理系统

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

一个完整的Streamlit应用，用于管理和分析设备报价单，集成PDF处理、Claude AI分析和SQLite数据库。

![Dashboard Screenshot](docs/screenshot.png)

## ✨ 主要功能

- 📄 **PDF处理中心** - 批量上传、文本提取、OCR识别
- 🤖 **AI智能分析** - Claude自动提取供应商、设备、价格信息
- 🗄️ **数据库管理** - SQLite存储、高级搜索、批量操作
- 📊 **数据可视化** - 统计图表、多维度分析
- 📈 **多视图展示** - 表格/卡片/对比三种视图
- ⚙️ **灵活配置** - API配置、参数设置、数据备份

## 🚀 快速开始

### 方法1：从GitHub克隆运行

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/quote-management-system.git
cd quote-management-system

# 2. 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置API密钥
cp .env.example .env
# 编辑 .env 文件，添加你的 Anthropic API 密钥

# 5. 运行应用
streamlit run app.py
```

### 方法2：部署到Streamlit Cloud（免费）

1. Fork这个仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 点击"New app"
4. 选择你的仓库和分支
5. 在Secrets中添加：
   ```toml
   ANTHROPIC_API_KEY = "your_api_key_here"
   ```
6. 部署完成！

### 方法3：使用Docker

```bash
# 构建镜像
docker-compose up -d

# 或者手动构建
docker build -t quote-manager .
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_key quote-manager
```

## 📋 系统要求

- Python 3.9+
- 操作系统：Windows/Linux/MacOS
- 内存：建议4GB以上
- 磁盘：100MB以上

## 🛠️ 安装依赖

### Python包
```bash
pip install -r requirements.txt
```

主要依赖：
- streamlit
- pandas
- plotly
- PyMuPDF
- anthropic
- pytesseract（可选，用于OCR）

### OCR支持（可选）

如需处理扫描版PDF，请安装Tesseract：

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
从 [这里](https://github.com/UB-Mannheim/tesseract/wiki) 下载安装

## 🔑 配置

### API密钥

获取Anthropic API密钥：https://console.anthropic.com/

**方法1：环境变量**
```bash
# .env文件
ANTHROPIC_API_KEY=your_api_key_here
```

**方法2：应用内配置**
启动应用后在"系统设置"页面配置

### 数据库

默认使用SQLite，数据库文件位于 `data/quotes.db`

## 📚 使用指南

### 典型工作流程

1. **上传PDF** → PDF处理中心 → 选择文件 → 开始处理
2. **AI分析** → AI分析界面 → 选择文件 → 开始分析
3. **保存数据** → 查看结果 → 保存到数据库
4. **数据管理** → 数据库管理 → 搜索/查看/导出

### 6大功能模块

#### 📊 概览仪表板
- 实时统计（总数、金额、趋势）
- 供应商分布图表
- 月度趋势分析
- 最近处理记录

#### 📄 PDF处理中心
- 单个/批量上传
- 文本提取（支持OCR）
- 图片提取
- 处理进度显示

#### 🤖 AI分析界面
- 智能提取供应商信息
- 识别设备项目和规格
- 提取价格和日期
- JSON/Excel导出

#### 🗄️ 数据库管理
- 高级搜索和筛选
- 详细信息查看
- 批量操作
- 数据导入导出

#### 📈 结果查看
- 表格视图
- 卡片视图
- 对比视图

#### ⚙️ 系统设置
- API配置
- 数据库管理
- PDF处理参数
- 界面设置

## 📁 项目结构

```
quote-management-system/
├── app.py                      # 主应用
├── requirements.txt            # 依赖包
├── .env.example                # 环境变量模板
├── Dockerfile                  # Docker配置
├── docker-compose.yml          # Docker Compose
├── .gitignore                  # Git忽略规则
├── LICENSE                     # MIT许可证
├── src/                        # 源代码
│   ├── pdf_processor.py       # PDF处理
│   ├── claude_analyzer.py     # AI分析
│   └── database.py            # 数据库
├── data/                       # 数据目录（自动创建）
│   └── quotes.db              # SQLite数据库
└── docs/                       # 文档
    ├── README.md
    ├── INSTALL_GUIDE.md
    ├── GITHUB_DEPLOYMENT.md
    └── CONTRIBUTING.md
```

## 🔒 安全提示

**⚠️ 重要：切勿提交敏感信息到GitHub！**

- ✅ 已包含 `.gitignore` 保护敏感文件
- ❌ 不要提交 `.env` 文件
- ❌ 不要提交包含真实API密钥的文件
- ❌ 不要提交 `data/` 目录（包含用户数据）

## 🚢 部署选项

### Streamlit Cloud（推荐）
- ✅ 免费托管
- ✅ 自动部署
- ✅ HTTPS支持
- 📖 [部署指南](GITHUB_DEPLOYMENT.md)

### Heroku
```bash
heroku create your-app-name
heroku config:set ANTHROPIC_API_KEY=your_key
git push heroku main
```

### AWS/GCP/Azure
使用Docker部署到任何云平台

### 本地/内网
适合企业内部使用

## 🐛 问题排查

### 常见问题

**Q: 无法启动应用**
```bash
# 检查Python版本
python --version  # 需要 3.9+

# 重新安装依赖
pip install -r requirements.txt --upgrade
```

**Q: PDF处理失败**
- 启用OCR选项（适用于扫描版PDF）
- 检查文件是否损坏
- 查看错误日志

**Q: API调用失败**
- 验证API密钥正确性
- 检查网络连接
- 确认API配额

**Q: 数据库错误**
```bash
# 重建数据库
rm data/quotes.db
streamlit run app.py
```

## 🤝 贡献

欢迎贡献！请查看 [贡献指南](CONTRIBUTING.md)

### 如何贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 待办事项

- [ ] 支持更多文件格式（Word、Excel）
- [ ] 添加用户认证
- [ ] 多语言支持
- [ ] 集成更多AI模型
- [ ] 移动端优化
- [ ] 单元测试覆盖

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - 优秀的Python Web框架
- [Anthropic](https://www.anthropic.com/) - Claude AI能力
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF处理库
- [Plotly](https://plotly.com/) - 数据可视化

## 📞 联系方式

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/YOUR_USERNAME/quote-management-system/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/YOUR_USERNAME/quote-management-system/discussions)

## ⭐ Star History

如果这个项目对你有帮助，请给个Star ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/quote-management-system&type=Date)](https://star-history.com/#YOUR_USERNAME/quote-management-system&Date)

---

**使用愉快！** 🎉

如有问题，请查看 [详细文档](docs/) 或提交 [Issue](https://github.com/YOUR_USERNAME/quote-management-system/issues)
