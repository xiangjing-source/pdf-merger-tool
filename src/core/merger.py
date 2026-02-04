"""
PDF合并核心引擎
使用PyMuPDF (fitz)实现高性能PDF合并
"""

import os
import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Callable, Optional


class PdfMerger:
    """PDF合并器类"""
    
    def __init__(self):
        """初始化PDF合并器"""
        self.file_list = []
        self.total_pages = 0
        
    def add_file(self, pdf_path: str) -> dict:
        """
        添加PDF文件到合并列表
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            dict: 文件信息 {path, pages, size, valid, error}
        """
        file_info = {
            'path': pdf_path,
            'pages': 0,
            'size': 0,
            'valid': False,
            'error': None
        }
        
        # 检查文件是否存在
        if not os.path.exists(pdf_path):
            file_info['error'] = f"文件不存在: {pdf_path}"
            return file_info
            
        # 获取文件大小
        try:
            file_info['size'] = os.path.getsize(pdf_path)
        except Exception as e:
            file_info['error'] = f"无法读取文件大小: {e}"
            return file_info
        
        # 验证PDF文件
        try:
            doc = fitz.open(pdf_path)
            file_info['pages'] = len(doc)
            doc.close()
            file_info['valid'] = True
            
            # 添加到列表
            self.file_list.append(file_info)
            self.total_pages += file_info['pages']
            
        except Exception as e:
            file_info['error'] = f"无效的PDF文件: {e}"
            
        return file_info
    
    def add_files(self, pdf_paths: List[str]) -> List[dict]:
        """
        批量添加PDF文件
        
        Args:
            pdf_paths: PDF文件路径列表
            
        Returns:
            List[dict]: 所有文件的信息列表
        """
        results = []
        for path in pdf_paths:
            result = self.add_file(path)
            results.append(result)
        return results
    
    def clear(self):
        """清空文件列表"""
        self.file_list = []
        self.total_pages = 0
    
    def get_file_count(self) -> int:
        """获取文件数量"""
        return len(self.file_list)
    
    def get_total_pages(self) -> int:
        """获取总页数"""
        return self.total_pages
    
    def merge(self, 
              output_path: str, 
              progress_callback: Optional[Callable[[int, int, str], None]] = None,
              compress: bool = True) -> bool:
        """
        合并所有PDF文件
        
        Args:
            output_path: 输出文件路径
            progress_callback: 进度回调函数 (current_page, total_pages, current_file)
            compress: 是否压缩输出文件
            
        Returns:
            bool: 是否成功
        """
        if not self.file_list:
            raise ValueError("没有可合并的PDF文件")
        
        # 创建输出目录
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        try:
            # 创建新的PDF文档
            output_doc = fitz.open()
            processed_pages = 0
            
            # 依次合并每个PDF
            for idx, file_info in enumerate(self.file_list):
                if not file_info['valid']:
                    continue
                
                file_path = file_info['path']
                
                # 报告进度
                if progress_callback:
                    progress_callback(
                        processed_pages, 
                        self.total_pages, 
                        f"正在处理: {os.path.basename(file_path)}"
                    )
                
                # 打开并插入PDF
                try:
                    doc = fitz.open(file_path)
                    output_doc.insert_pdf(doc)
                    processed_pages += len(doc)
                    doc.close()
                    
                except Exception as e:
                    print(f"警告: 跳过文件 {file_path}, 原因: {e}")
                    continue
            
            # 保存合并后的PDF
            if progress_callback:
                progress_callback(
                    self.total_pages, 
                    self.total_pages, 
                    "正在保存文件..."
                )
            
            # 保存选项: garbage=4(最大压缩), deflate=True(压缩流)
            save_options = {
                'garbage': 4 if compress else 0,
                'deflate': compress,
                'clean': compress
            }
            
            output_doc.save(output_path, **save_options)
            output_doc.close()
            
            if progress_callback:
                progress_callback(
                    self.total_pages, 
                    self.total_pages, 
                    "完成!"
                )
            
            return True
            
        except Exception as e:
            raise Exception(f"合并失败: {e}")
    
    def get_file_info_summary(self) -> str:
        """
        获取文件列表摘要信息
        
        Returns:
            str: 格式化的摘要信息
        """
        if not self.file_list:
            return "没有文件"
        
        valid_count = sum(1 for f in self.file_list if f['valid'])
        total_size = sum(f['size'] for f in self.file_list if f['valid'])
        
        # 格式化文件大小
        if total_size < 1024:
            size_str = f"{total_size}B"
        elif total_size < 1024 * 1024:
            size_str = f"{total_size / 1024:.2f}KB"
        else:
            size_str = f"{total_size / (1024 * 1024):.2f}MB"
        
        summary = f"""
文件数量: {valid_count}/{len(self.file_list)}
总页数: {self.total_pages}
总大小: {size_str}
"""
        return summary.strip()


def merge_pdfs_simple(input_files: List[str], output_file: str) -> bool:
    """
    简化的PDF合并函数（一行调用）
    
    Args:
        input_files: 输入PDF文件列表
        output_file: 输出文件路径
        
    Returns:
        bool: 是否成功
    """
    merger = PdfMerger()
    merger.add_files(input_files)
    return merger.merge(output_file)
