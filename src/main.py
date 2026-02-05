"""
PDF合并工具 - 命令行版本
阶段1: 最小可用版本
"""

import sys
import os
import argparse
from pathlib import Path
from core.merger import PdfMerger


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f}KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f}MB"


def progress_callback(current: int, total: int, message: str):
    """进度回调函数"""
    if total > 0:
        percent = (current / total) * 100
        bar_length = 40
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        print(f'\r进度: [{bar}] {percent:.1f}% - {message}', end='', flush=True)
    else:
        print(f'\r{message}', end='', flush=True)


def find_pdfs_in_directory(directory: str) -> list:
    """
    在目录中查找所有PDF文件
    
    Args:
        directory: 目录路径
        
    Returns:
        list: PDF文件路径列表（已排序）
    """
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    # 按文件名排序
    pdf_files.sort()
    return pdf_files


def run_cli(argv=None):
    """命令行入口（可复用）"""
    parser = argparse.ArgumentParser(
        description='PDF合并工具 - 快速、本地、隐私安全',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 合并指定文件
  python main.py file1.pdf file2.pdf file3.pdf
  
  # 合并文件夹中的所有PDF
  python main.py /path/to/pdf/folder
  
  # 指定输出文件名
  python main.py file1.pdf file2.pdf -o my_merged.pdf
  
  # 不压缩输出文件（更快但文件更大）
  python main.py file1.pdf file2.pdf --no-compress
        """
    )
    
    parser.add_argument(
        'inputs',
        nargs='+',
        help='PDF文件路径或包含PDF的文件夹路径'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='merged_output.pdf',
        help='输出文件名（默认: merged_output.pdf）'
    )
    
    parser.add_argument(
        '--no-compress',
        action='store_true',
        help='不压缩输出文件（更快但文件更大）'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args(argv)
    
    # 收集所有PDF文件
    pdf_files = []
    for input_path in args.inputs:
        if os.path.isdir(input_path):
            # 如果是目录，查找所有PDF
            found_pdfs = find_pdfs_in_directory(input_path)
            if found_pdfs:
                print(f"📁 在目录 '{input_path}' 中找到 {len(found_pdfs)} 个PDF文件")
                pdf_files.extend(found_pdfs)
            else:
                print(f"⚠️  警告: 目录 '{input_path}' 中没有找到PDF文件")
        elif os.path.isfile(input_path):
            # 如果是文件，直接添加
            if input_path.lower().endswith('.pdf'):
                pdf_files.append(input_path)
            else:
                print(f"⚠️  警告: '{input_path}' 不是PDF文件，已跳过")
        else:
            print(f"❌ 错误: '{input_path}' 不存在")
            return 1
    
    if not pdf_files:
        print("❌ 错误: 没有找到可合并的PDF文件")
        return 1
    
    # 创建合并器
    print(f"\n🔍 正在验证 {len(pdf_files)} 个PDF文件...")
    merger = PdfMerger()
    
    # 添加文件并显示信息
    results = merger.add_files(pdf_files)
    
    # 显示文件列表
    if args.verbose:
        print("\n文件列表:")
        print("-" * 80)
        for idx, info in enumerate(results, 1):
            status = "✅" if info['valid'] else "❌"
            size = format_size(info['size'])
            pages = f"{info['pages']}页" if info['valid'] else info['error']
            filename = os.path.basename(info['path'])
            print(f"{status} {idx:2d}. {filename:40s} {size:>10s} {pages}")
        print("-" * 80)
    
    # 检查是否有有效文件
    valid_count = sum(1 for r in results if r['valid'])
    if valid_count == 0:
        print("❌ 错误: 没有有效的PDF文件可以合并")
        return 1
    
    # 显示摘要
    print(f"\n📊 {merger.get_file_info_summary()}")
    
    # 开始合并
    print(f"\n🔄 开始合并到 '{args.output}'...")
    
    try:
        success = merger.merge(
            args.output,
            progress_callback=progress_callback,
            compress=not args.no_compress
        )
        
        if success:
            output_size = os.path.getsize(args.output)
            print(f"\n\n✅ 合并成功!")
            print(f"📄 输出文件: {args.output}")
            print(f"📦 文件大小: {format_size(output_size)}")
            return 0
        else:
            print("\n\n❌ 合并失败")
            return 1
            
    except Exception as e:
        print(f"\n\n❌ 合并过程中出错: {e}")
        return 1


def main():
    """兼容旧入口"""
    return run_cli()


if __name__ == '__main__':
    sys.exit(run_cli())
