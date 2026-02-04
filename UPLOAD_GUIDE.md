# GitHub上传指南

## 📋 准备工作清单

### ✅ 已完成:
- [x] 源代码准备好
- [x] README.md 编写完成
- [x] .gitignore 配置完成
- [x] LICENSE 文件创建
- [x] 测试代码包含

### 📂 当前目录内容:
```
pdf-merger-tool-github/
├── src/                    # 源代码
├── tests/                  # 测试代码
├── build.sh               # 打包脚本
├── requirements.txt       # 依赖清单
├── README.md              # 项目说明
├── QUICK_REFERENCE.md     # 快速参考
├── .gitignore            # Git忽略配置
└── LICENSE               # MIT许可证
```

---

## 🚀 上传步骤

### 步骤1: 初始化Git仓库

```bash
cd /home/jing/study/pdf-merger-tool-github

# 初始化Git
git init

# 添加所有文件
git add .

# 查看将要提交的文件
git status

# 提交
git commit -m "Initial commit: PDF Merger Tool

- 高性能PDF合并工具
- 基于PyMuPDF实现
- 支持命令行使用
- 包含打包脚本"
```

### 步骤2: 在GitHub创建仓库

1. 访问 https://github.com/new
2. 仓库名称: `pdf-merger-tool`
3. 描述: `快速、本地、隐私安全的PDF合并工具`
4. 选择 **Public**（公开）
5. **不要**勾选 "Add a README"（我们已经有了）
6. **不要**勾选 "Add .gitignore"（我们已经有了）
7. **不要**选择License（我们已经有了）
8. 点击 **Create repository**

### 步骤3: 关联远程仓库并推送

```bash
# 关联GitHub仓库（替换成你的用户名）
git remote add origin https://github.com/你的用户名/pdf-merger-tool.git

# 设置默认分支名
git branch -M main

# 推送代码
git push -u origin main
```

如果需要输入用户名密码，可以使用Personal Access Token。

---

## 📦 创建Release（发布可执行文件）

### 步骤1: 准备可执行文件

```bash
# 从本地项目复制可执行文件
cp /home/jing/study/pdf-merger-tool/dist/pdfmerge ~/pdfmerge-linux-v1.0

# 或者重新打包
cd /home/jing/study/pdf-merger-tool
./build.sh
cp dist/pdfmerge ~/pdfmerge-linux-v1.0
```

### 步骤2: 在GitHub创建Release

1. 访问你的仓库页面
2. 点击右侧的 **Releases**
3. 点击 **Create a new release**
4. 填写信息:
   - Tag version: `v1.0`
   - Release title: `v1.0 - 首次发布`
   - 描述:
     ```
     ## PDF合并工具 v1.0
     
     首次发布！
     
     ### ✨ 功能特性
     - 高性能PDF合并（基于PyMuPDF）
     - 命令行工具，简单易用
     - 支持批量处理和文件夹合并
     - 自动文件压缩
     
     ### 📦 下载
     - **Linux用户**: 下载 `pdfmerge-linux` 直接使用
     - **其他平台**: 请从源码安装
     
     ### 🚀 使用方法
     ```bash
     chmod +x pdfmerge-linux
     sudo cp pdfmerge-linux /usr/local/bin/pdfmerge
     pdfmerge file1.pdf file2.pdf -o output.pdf
     ```
     
     ### 📊 性能
     - 比在线工具快5-10倍
     - 支持大文件处理
     ```
5. 上传文件: 拖拽 `~/pdfmerge-linux-v1.0` 到附件区
6. 点击 **Publish release**

---

## 📝 后续更新

### 更新代码
```bash
cd /home/jing/study/pdf-merger-tool-github

# 修改代码后
git add .
git commit -m "更新说明"
git push
```

### 发布新版本
1. 重新打包可执行文件
2. 创建新的Release
3. 标签使用 `v1.1`, `v1.2` 等

---

## 🎯 推广建议

### README徽章（可选）

在README.md顶部添加：
```markdown
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)
```

### 添加截图（可选）

1. 截取命令行使用的截图
2. 保存为 `screenshots/demo.png`
3. 在README中引用:
   ```markdown
   ## 📸 演示
   ![演示](screenshots/demo.png)
   ```

---

## ✅ 完成检查清单

上传前确认：

- [ ] README.md 写清楚了使用方法
- [ ] 所有源代码都已包含
- [ ] .gitignore 配置正确
- [ ] 测试代码可以运行
- [ ] LICENSE 文件存在
- [ ] 没有包含敏感信息（密码、密钥等）
- [ ] 没有包含巨大的二进制文件

发布Release前确认：

- [ ] 可执行文件已测试
- [ ] Release说明清晰
- [ ] 版本号正确
- [ ] 下载链接有效

---

## 🎉 完成！

上传成功后，你的项目将在：
- **代码仓库**: https://github.com/你的用户名/pdf-merger-tool
- **Release页面**: https://github.com/你的用户名/pdf-merger-tool/releases

其他人可以：
- 查看源代码
- 下载可执行文件（Linux）
- 从源码安装（所有平台）
- 提交Issue和PR

---

**需要帮助?** 查看GitHub文档: https://docs.github.com/
