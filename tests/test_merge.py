"""
快速测试脚本 - 生成测试PDF并测试合并功能
"""

import os
import sys
import fitz  # PyMuPDF

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.merger import PdfMerger


def create_test_pdf(filename: str, page_count: int = 3, content: str = None):
    """
    创建测试用的PDF文件
    
    Args:
        filename: 文件名
        page_count: 页数
        content: 页面内容（默认为文件名）
    """
    doc = fitz.open()
    
    for i in range(page_count):
        page = doc.new_page(width=595, height=842)  # A4大小
        
        # 添加文本
        text = content or f"测试文件: {filename}\n第 {i+1}/{page_count} 页"
        page.insert_text(
            (50, 50),
            text,
            fontsize=20,
            color=(0, 0, 0)
        )
        
        # 添加页码
        page.insert_text(
            (297, 800),  # 页面底部中央
            f"- {i+1} -",
            fontsize=12,
            color=(0.5, 0.5, 0.5)
        )
    
    doc.save(filename)
    doc.close()
    print(f"✅ 创建测试PDF: {filename} ({page_count}页)")


def test_basic_merge():
    """测试基本合并功能"""
    print("=" * 60)
    print("测试1: 基本合并功能")
    print("=" * 60)
    
    # 创建测试目录
    test_dir = "test_pdfs"
    os.makedirs(test_dir, exist_ok=True)
    
    # 创建测试文件
    test_files = []
    for i in range(1, 4):
        filename = os.path.join(test_dir, f"test_{i}.pdf")
        create_test_pdf(filename, page_count=i*2, content=f"这是测试文件 #{i}")
        test_files.append(filename)
    
    print(f"\n📁 创建了 {len(test_files)} 个测试文件\n")
    
    # 测试合并
    merger = PdfMerger()
    
    print("🔍 添加文件到合并列表...")
    results = merger.add_files(test_files)
    
    for info in results:
        status = "✅" if info['valid'] else "❌"
        print(f"{status} {os.path.basename(info['path'])}: {info['pages']}页")
    
    print(f"\n📊 {merger.get_file_info_summary()}")
    
    # 合并
    output_file = os.path.join(test_dir, "merged_test.pdf")
    print(f"\n🔄 合并到: {output_file}")
    
    def progress(current, total, msg):
        percent = (current / total) * 100 if total > 0 else 0
        print(f"  进度: {percent:.0f}% - {msg}")
    
    try:
        merger.merge(output_file, progress_callback=progress)
        
        # 验证结果
        doc = fitz.open(output_file)
        print(f"\n✅ 合并成功! 输出文件有 {len(doc)} 页")
        doc.close()
        
        # 显示文件大小
        size = os.path.getsize(output_file)
        print(f"📦 文件大小: {size / 1024:.2f}KB")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False


def test_large_file():
    """测试大文件处理"""
    print("\n" + "=" * 60)
    print("测试2: 大文件处理 (50页)")
    print("=" * 60)
    
    test_dir = "test_pdfs"
    filename = os.path.join(test_dir, "large_test.pdf")
    
    create_test_pdf(filename, page_count=50, content="大文件测试 (50页)")
    
    merger = PdfMerger()
    merger.add_file(filename)
    
    output = os.path.join(test_dir, "large_merged.pdf")
    
    try:
        merger.merge(output, compress=True)
        print(f"✅ 大文件处理成功")
        return True
    except Exception as e:
        print(f"❌ 大文件处理失败: {e}")
        return False


def test_error_handling():
    """测试错误处理"""
    print("\n" + "=" * 60)
    print("测试3: 错误处理")
    print("=" * 60)
    
    merger = PdfMerger()
    
    # 测试不存在的文件
    info = merger.add_file("nonexistent.pdf")
    assert not info['valid'], "应该检测到文件不存在"
    print("✅ 正确处理不存在的文件")
    
    # 测试空合并
    try:
        merger.merge("output.pdf")
        print("❌ 应该抛出异常（没有文件）")
        return False
    except ValueError:
        print("✅ 正确处理空文件列表")
        return True


if __name__ == '__main__':
    print("\n" + "🧪 PDF合并工具测试套件" + "\n")
    
    results = []
    
    # 运行测试
    results.append(("基本合并", test_basic_merge()))
    results.append(("大文件处理", test_large_file()))
    results.append(("错误处理", test_error_handling()))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{status}: {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        sys.exit(0)
    else:
        print(f"\n⚠️  有 {total - passed} 个测试失败")
        sys.exit(1)
