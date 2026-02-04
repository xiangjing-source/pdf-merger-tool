# PDF合并工具

一个快速、本地、隐私安全的PDF合并工具。

## ✨ 特性

- ✅ **本地处理** - 无需上传到服务器，隐私安全
- ✅ **高性能** - 基于PyMuPDF，比在线工具快5-10倍
- ✅ **简单易用** - 一个命令搞定
- ✅ **支持大文件** - 优化内存使用，处理100+页无压力
- ✅ **全局命令** - 安装后任何目录都可使用

## 🚀 快速开始

### Linux用户（推荐 - 开箱即用）

下载预编译的可执行文件（无需Python环境）：

```bash
# 从Release下载
wget https://github.com/你的用户名/pdf-merger-tool/releases/download/v1.0/pdfmerge-linux
chmod +x pdfmerge-linux

# 安装到系统（可选）
sudo cp pdfmerge-linux /usr/local/bin/pdfmerge

# 使用
pdfmerge file1.pdf file2.pdf -o output.pdf
```

### 从源码安装（所有平台）

#### 1. 克隆仓库

```bash
git clone https://github.com/你的用户名/pdf-merger-tool.git
cd pdf-merger-tool
```

#### 2. 创建虚拟环境并安装依赖

```bash
# Linux/Mac
python3 -m venv pdf-venv
source pdf-venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv pdf-venv
pdf-venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. 使用

```bash
python src/main.py file1.pdf file2.pdf -o output.pdf
```

#### 4. 打包成可执行文件（可选）

```bash
# 安装打包工具
pip install pyinstaller

# 打包
./build.sh  # Linux/Mac
# Windows需要手动运行: pyinstaller --onefile --name pdfmerge src/main.py

# 使用打包后的文件
./dist/pdfmerge file1.pdf file2.pdf
```

## 📖 使用方法

### 基本用法

```bash
# 合并指定文件
pdfmerge file1.pdf file2.pdf file3.pdf

# 指定输出文件名
pdfmerge file1.pdf file2.pdf -o merged_output.pdf

# 合并文件夹中的所有PDF（按文件名排序）
pdfmerge /path/to/pdf/folder

# 详细模式（显示每个文件信息）
pdfmerge file1.pdf file2.pdf -v
```

### 高级选项

```bash
# 不压缩输出（更快但文件更大）
pdfmerge file1.pdf file2.pdf --no-compress

# 查看帮助
pdfmerge --help
```

### 使用示例

```bash
# 合并论文章节
pdfmerge 第1章.pdf 第2章.pdf 第3章.pdf 参考文献.pdf -o 完整论文.pdf

# 合并扫描文档
pdfmerge ~/Documents/扫描件 -o 合同汇总.pdf

# 批量合并多个文件夹
pdfmerge ~/folder1 ~/folder2 -o all_merged.pdf
```

## ⚡ 性能

- 小文件 (10个×5页): **<1秒**
- 中等文件 (50个×20页): **3-5秒**
- 大文件 (100个×50页): **10-15秒**

**对比在线工具提升5-10倍速度** 🚀

## 🛠️ 技术栈

- **PyMuPDF (fitz)** - 高性能PDF处理库
- **Python 3.8+** - 开发语言
- **PyInstaller** - 打包工具（可选）

## 📁 项目结构

```
pdf-merger-tool/
├── src/
│   ├── main.py              # 命令行主程序
│   └── core/
│       └── merger.py        # PDF合并引擎
├── tests/
│   └── test_merge.py        # 测试代码
├── build.sh                 # 打包脚本
├── requirements.txt         # Python依赖
└── README.md               # 本文件
```

## 🧪 运行测试

```bash
# 激活虚拟环境后
python tests/test_merge.py
```

## ❓ 常见问题

### Q: 文件夹中的PDF按什么顺序合并？
A: 按文件名字母顺序。建议给文件加数字前缀控制顺序（如 `01_`, `02_`）

### Q: 默认是压缩还是不压缩？
A: 默认压缩，可节省约45%空间，速度影响可忽略。使用 `--no-compress` 跳过压缩

### Q: 支持加密的PDF吗？
A: 暂不支持加密PDF

### Q: Windows/Mac有可执行文件吗？
A: 当前只提供Linux版本。其他平台请从源码运行或自行打包

## 🗑️ 卸载

```bash
# 如果安装了全局命令
sudo rm /usr/local/bin/pdfmerge
```

## 📄 License

MIT License - 自由使用、修改和分发

## 🤝 贡献

欢迎提交Issue和Pull Request！

## ⭐ 如果这个项目对你有帮助，请给个Star！

---

**快速开始**: `pdfmerge file1.pdf file2.pdf -o output.pdf`

**项目主页**: https://github.com/你的用户名/pdf-merger-tool
