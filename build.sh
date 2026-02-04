#!/bin/bash
# PDF合并工具打包脚本

echo "🚀 开始打包PDF合并工具..."
echo "================================"

# 确保在正确的目录
cd "$(dirname "$0")"

# 激活虚拟环境
source /home/jing/study/pdf-venv/bin/activate

# 清理之前的打包文件
echo "🧹 清理旧文件..."
rm -rf build dist *.spec

# 使用PyInstaller打包
echo ""
echo "📦 打包中..."
pyinstaller --onefile \
    --name pdfmerge \
    --clean \
    --noconfirm \
    src/main.py

# 检查是否成功
if [ -f "dist/pdfmerge" ]; then
    echo ""
    echo "================================"
    echo "✅ 打包成功！"
    echo ""
    echo "📄 可执行文件位置: dist/pdfmerge"
    
    # 显示文件信息
    FILE_SIZE=$(du -h dist/pdfmerge | cut -f1)
    echo "📦 文件大小: $FILE_SIZE"
    
    # 测试运行
    echo ""
    echo "🧪 测试运行..."
    ./dist/pdfmerge --help
    
    echo ""
    echo "================================"
    echo "💡 使用方法:"
    echo "   ./dist/pdfmerge file1.pdf file2.pdf -o output.pdf"
    echo ""
    echo "🔧 安装到系统（可选）:"
    echo "   sudo cp dist/pdfmerge /usr/local/bin/"
    echo "   然后就可以全局使用: pdfmerge file1.pdf file2.pdf"
    echo ""
else
    echo ""
    echo "❌ 打包失败！请检查错误信息"
    exit 1
fi
