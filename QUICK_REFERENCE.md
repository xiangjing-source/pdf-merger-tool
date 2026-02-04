# 快速参考

## 一分钟上手

```bash
# 最基本的用法
pdfmerge file1.pdf file2.pdf

# 指定输出文件名
pdfmerge file1.pdf file2.pdf -o output.pdf

# 合并文件夹
pdfmerge ~/Documents/PDFs

# 查看帮助
pdfmerge --help
```

## 所有选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `inputs` | PDF文件或文件夹路径 | `pdfmerge a.pdf b.pdf` |
| `-o, --output` | 输出文件名 | `-o result.pdf` |
| `-v, --verbose` | 显示详细信息 | `pdfmerge a.pdf -v` |
| `--no-compress` | 不压缩（更快但更大） | `--no-compress` |
| `-h, --help` | 显示帮助 | `pdfmerge --help` |

## 常见场景

### 场景1: 合并论文
```bash
pdfmerge 摘要.pdf 第1章.pdf 第2章.pdf 参考文献.pdf -o 完整论文.pdf
```

### 场景2: 合并扫描件
```bash
pdfmerge ~/Documents/扫描件 -o 合同汇总.pdf
```

### 场景3: 快速合并（不压缩）
```bash
pdfmerge file1.pdf file2.pdf --no-compress
```

### 场景4: 查看文件信息
```bash
pdfmerge file1.pdf file2.pdf -v
```

## 提示

- ✅ 文件夹中的PDF按**文件名排序**
- ✅ 默认**自动压缩**，节省45%空间
- ✅ 可在**任何目录**使用
- ✅ 支持**中文文件名**
