# PDF合并工具

一个快速、本地、隐私安全的PDF合并工具。

## 特性
- ✅ 本地处理，无需上传到服务器
- ✅ 高性能合并（基于PyMuPDF）
- ✅ 支持大文件处理
- ✅ 简单易用
- ✅ 全局命令，任何目录可用
- ✅ 无需Python环境（打包版本）

## 快速开始

### 方式1: 直接下载 Release（推荐）

在 GitHub Release 页面下载对应系统的可执行文件：
- Windows：`pdfmerge.exe`
- Linux：`pdfmerge`
- macOS：`pdfmerge`

下载后即可直接运行，无需安装 Python。

如果已经安装到系统：
```bash
# 在任何目录下直接使用
pdfmerge file1.pdf file2.pdf -o output.pdf

# 合并整个文件夹
pdfmerge ~/Documents/PDFs -o merged.pdf

# 查看帮助
pdfmerge --help
```

如果已安装 GUI 版：
```bash
pdfview
```

### 方式2: 从源码运行（开发者）

#### 1. 克隆仓库
```bash
git clone https://github.com/你的用户名/pdf-merger-tool
cd pdf-merger-tool
```

```bash
# 创建虚拟环境
python3 -m venv pdf-venv
source pdf-venv/bin/activate  # Linux/Mac
# 或 pdf-venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行
python src/main.py file1.pdf file2.pdf -o output.pdf
```

运行 GUI：
```bash
python src/gui.py
```

## 安装指南（按系统）

### Linux
1. 进入 Release 页面下载 `pdfmerge`
2. 赋予可执行权限并移动到 PATH：
```bash
chmod +x pdfmerge
mkdir -p ~/.local/bin
mv pdfmerge ~/.local/bin/
```
3. 确保 `~/.local/bin` 在 PATH（如无则加入到 `~/.bashrc`）：
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Windows
1. 进入 Release 页面下载 `pdfmerge.exe`
2. 将它们放到任意目录（例如 `C:\Tools\pdf`）
3. 将该目录加入系统环境变量 `Path`

### macOS
1. 进入 Release 页面下载 `pdfmerge`
2. 赋予可执行权限并移动到 PATH：
```bash
chmod +x pdfmerge
mkdir -p ~/.local/bin
mv pdfmerge ~/.local/bin/
```
3. 确保 `~/.local/bin` 在 PATH（如无则加入到 `~/.zshrc` 或 `~/.bashrc`）

## 使用方法

### 合并指定文件
```bash
pdfmerge file1.pdf file2.pdf file3.pdf
```

### 合并文件夹中的所有PDF
```bash
pdfmerge /path/to/pdf/folder
```

### 指定输出文件名
```bash
pdfmerge file1.pdf file2.pdf -o merged_output.pdf
```

### 详细模式（显示文件信息）
```bash
pdfmerge file1.pdf file2.pdf -v
```

### 不压缩输出（更快但文件更大）
```bash
pdfmerge file1.pdf file2.pdf --no-compress
```

## 性能
- 小文件(10个×5页): <1秒
- 中等文件(50个×20页): 3-5秒
- 大文件(100个×50页): 10-15秒

## 技术栈
- **PyMuPDF (fitz)**: 高性能PDF处理
- **Python 3.8+**: 开发语言
- **PyInstaller**: 打包工具

## 文件说明
- `src/main.py` - 命令行主程序
- `src/gui.py` - 图形界面入口
- `src/app.py` - 单一入口（GUI + CLI）
- `src/core/merger.py` - PDF合并引擎
> 本仓库不包含本地打包脚本，打包产物通过 GitHub Actions 生成。

## GitHub Actions（跨平台打包）
项目已提供 `.github/workflows/build.yml`，可在打 Tag 或手动触发后生成：
- Windows：`pdfmerge.exe`
- Linux：`pdfmerge`
- macOS：`pdfmerge`

使用方式：
1. 推送 Tag（如 `v2.0.0`）
2. 在 Actions 下载构建产物，或在 Release 页面下载

## 开发路线
- [x] 阶段1: 命令行版本
- [x] 打包成可执行文件
- [x] 全局命令安装
- [ ] 阶段2: GUI版本（可选）
- [ ] 阶段3: 高级功能（可选）

## 卸载

```bash
sudo rm /usr/local/bin/pdfmerge
```

## License
MIT
