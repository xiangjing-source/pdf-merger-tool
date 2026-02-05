# PDF合并工具

一个快速、本地、隐私安全的PDF合并工具。

## ✨ 特性

- ✅ **本地处理** - 无需上传到服务器，隐私安全
- ✅ **高性能** - 基于PyMuPDF，比在线工具快5-10倍
- ✅ **简单易用** - 一个命令搞定
- ✅ **支持大文件** - 优化内存使用，处理100+页无压力
- ✅ **全局命令** - 安装后任何目录都可使用
- ✅ **跨平台支持** - 提供 Windows、macOS、Linux 三平台安装包

## 🚀 快速开始

### 方式1：下载预编译安装包（推荐 - 开箱即用）

> 📦 **无需安装 Python 环境，下载即用！**

前往 [Releases](https://github.com/xiangjing-source/pdf-merger-tool/releases) 下载对应平台的安装包：

#### Windows 用户
1. 下载 `pdfmerge-windows.exe` 到任意文件夹
2. **在命令提示符（CMD）或 PowerShell 中使用**：
   ```cmd
   # 切换到 pdfmerge-windows.exe 所在目录
   cd C:\path\to\download\folder
   
   # 运行合并命令
   pdfmerge-windows.exe file1.pdf file2.pdf -o output.pdf
   ```
   
   > ⚠️ **注意**：这是命令行工具，**不要双击运行**（会闪退）！必须在 CMD/PowerShell 中使用。
   
   > 💡 提示：首次运行可能被 Windows Defender 拦截，选择"仍要运行"即可

#### macOS 用户
```bash
# 下载安装包
curl -L -o pdfmerge https://github.com/xiangjing-source/pdf-merger-tool/releases/latest/download/pdfmerge-macos
chmod +x pdfmerge

# 使用
./pdfmerge file1.pdf file2.pdf -o output.pdf
```
> 💡 提示：首次运行需右键选择"打开"以绕过安全限制

#### Linux 用户
```bash
# 下载安装包
wget https://github.com/xiangjing-source/pdf-merger-tool/releases/latest/download/pdfmerge-linux
chmod +x pdfmerge-linux

# 安装到系统（可选）
sudo cp pdfmerge-linux /usr/local/bin/pdfmerge

# 使用
pdfmerge file1.pdf file2.pdf -o output.pdf
```

### 方式2：从源码安装

#### 1. 克隆仓库

```bash
git clone https://github.com/xiangjing-source/pdf-merger-tool.git
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

### Q: Windows 版本双击后闪退怎么办？
A: **这是正常的！** 这是一个命令行工具（CLI），不是图形界面程序。必须在 CMD 或 PowerShell 中使用命令运行，不能直接双击。

**正确使用方法**：
```cmd
# 1. 按 Win + R，输入 cmd，回车打开命令提示符
# 2. 切换到 exe 所在目录
cd C:\Users\YourName\Downloads

# 3. 运行命令
pdfmerge-windows.exe file1.pdf file2.pdf -o output.pdf
```

**可选**：如果想要图形界面，可以考虑使用批处理脚本包装，或等待未来的 GUI 版本。

### Q: 文件夹中的PDF按什么顺序合并？
A: 按文件名字母顺序。建议给文件加数字前缀控制顺序（如 `01_`, `02_`）

### Q: 默认是压缩还是不压缩？
A: 默认压缩，可节省约45%空间，速度影响可忽略。使用 `--no-compress` 跳过压缩

### Q: 支持加密的PDF吗？
A: 暂不支持加密PDF

### Q: 如何在 Windows 上全局使用（任意目录都能运行）？
A: 将 `pdfmerge-windows.exe` 复制到系统 PATH 目录，或添加自定义目录到 PATH 环境变量。

**快速方法**：
```cmd
# 复制到 Windows\System32 目录（需要管理员权限）
copy pdfmerge-windows.exe C:\Windows\System32\pdfmerge.exe

# 之后在任意目录都可以直接使用
pdfmerge file1.pdf file2.pdf -o output.pdf
```

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

**项目主页**: https://github.com/xiangjing-source/pdf-merger-tool
