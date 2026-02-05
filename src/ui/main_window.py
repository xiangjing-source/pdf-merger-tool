import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import traceback
import os
import time

# 尝试导入拖拽支持库
try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False

import threading


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.file_list = []
        self.last_dir = os.path.expanduser("~")
        self._set_font()
        self._build_ui()

    def _set_font(self):
        from tkinter import font
        preferred_fonts = [
            "Source Han Sans SC",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "Noto Sans SC",
            "WenQuanYi Zen Hei",
            "SimHei",
            "Arial",
        ]
        available = list(font.families())
        chosen = None
        for f in preferred_fonts:
            if f in available:
                chosen = f
                break
        if chosen is None:
            # fallback to default
            default_font = font.nametofont("TkDefaultFont")
            default_font.config(size=13)
            self.ui_font = default_font
        else:
            self.ui_font = font.Font(family=chosen, size=13)
            # also set default for other widgets
            font.nametofont("TkDefaultFont").config(family=chosen, size=13)
        self.root.option_add("*Font", self.ui_font)

    def _build_ui(self):
        # 文件选择按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(btn_frame, text="选择PDF文件", command=self.open_file_browser).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="移除选中", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="上移", command=self.move_up).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下移", command=self.move_down).pack(side=tk.LEFT, padx=5)

        # 文件列表
        # 主文件列表，显式使用选定字体以改善中文显示
        try:
            self.listbox = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=60, height=10, font=self.ui_font)
        except Exception:
            self.listbox = tk.Listbox(self.root, selectmode=tk.EXTENDED, width=60, height=10)
        self.listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # （已隐藏拖拽提示）

        # 输出文件名
        out_frame = tk.Frame(self.root)
        out_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(out_frame, text="输出文件名:").pack(side=tk.LEFT)
        self.output_entry = tk.Entry(out_frame, width=30)
        self.output_entry.pack(side=tk.LEFT, padx=5)
        self.output_entry.insert(0, "merged_output.pdf")
        tk.Button(out_frame, text="浏览", command=self.browse_output).pack(side=tk.LEFT)

        # 合并按钮和进度条
        action_frame = tk.Frame(self.root)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        self.merge_btn = tk.Button(action_frame, text="开始合并", command=self.start_merge)
        self.merge_btn.pack(side=tk.LEFT)
        self.progress = ttk.Progressbar(action_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=10)

        # 注册拖拽（如果可用），不显示额外提示文本
        if DND_AVAILABLE:
            try:
                self.listbox.drop_target_register(DND_FILES)
                self.listbox.dnd_bind('<<Drop>>', self._on_drop)
            except Exception:
                # 忽略注册错误，拖拽功能降级到不可用
                pass

    def add_files(self):
        # 保留方法名，内部转向自定义可排序选择器
        self.open_file_browser()

    def open_file_browser(self, start_dir=None):
        """
        打开自定义文件浏览器对话，列出目录下的 PDF 文件，支持按名称或更新时间排序并多选添加。
        """
        if start_dir is None:
            start_dir = self.last_dir

        class FileBrowserDialog(tk.Toplevel):
            def __init__(self, parent, directory, add_callback, font=None):
                super().__init__(parent)
                self.parent = parent
                self.directory = directory
                self.add_callback = add_callback
                self.title("选择 PDF 文件")
                self.transient(parent)
                self.grab_set()
                self.geometry("700x420")
                self.configure(padx=8, pady=8)
                self.font = font
                self._debounce_id = None
                self._build()

            def _build(self):
                topbar = tk.Frame(self)
                topbar.pack(fill=tk.X)
                tk.Label(topbar, text="目录:", font=self.font).pack(side=tk.LEFT)
                self.dir_var = tk.StringVar(value=self.directory)
                self.dir_entry = tk.Entry(topbar, textvariable=self.dir_var, width=60, font=self.font)
                self.dir_entry.pack(side=tk.LEFT, padx=4)
                self.dir_entry.bind("<Return>", lambda e: self._cd(silent=False))
                self.dir_var.trace_add("write", self._on_dir_change)
                tk.Button(topbar, text="上级", command=self._go_up, font=self.font).pack(side=tk.RIGHT, padx=4)

                ctrlbar = tk.Frame(self)
                ctrlbar.pack(fill=tk.X, pady=(6,0))
                tk.Label(ctrlbar, text="排序:", font=self.font).pack(side=tk.LEFT)
                self.sort_var = tk.StringVar(value="name")
                # 使用单选按钮并在切换时自动刷新
                rb_name = tk.Radiobutton(ctrlbar, text="名称", variable=self.sort_var, value="name", command=self._refresh, font=self.font)
                rb_name.pack(side=tk.LEFT, padx=4)
                rb_time = tk.Radiobutton(ctrlbar, text="更新时间", variable=self.sort_var, value="mtime", command=self._refresh, font=self.font)
                rb_time.pack(side=tk.LEFT, padx=4)
                tk.Button(ctrlbar, text="刷新", command=self._refresh, font=self.font).pack(side=tk.LEFT, padx=6)

                # 文件列表：名称 + 修改时间（动态行高避免被裁剪）
                try:
                    from tkinter import font as tkfont
                    font_obj = self.font if isinstance(self.font, tkfont.Font) else tkfont.nametofont("TkDefaultFont")
                    linespace = font_obj.metrics("linespace")
                    rowheight = max(linespace + 8, 24)
                    style = ttk.Style(self)
                    style.configure("Custom.Treeview", rowheight=rowheight, font=font_obj)
                    style.configure("Custom.Treeview.Heading", font=font_obj)
                    tree_style = "Custom.Treeview"
                except Exception:
                    tree_style = "Treeview"

                self.tree = ttk.Treeview(self, columns=("name", "mtime"), show="headings", selectmode="extended", style=tree_style)
                self.tree.heading("name", text="文件名")
                self.tree.heading("mtime", text="修改时间")
                self.tree.column("name", width=420, anchor="w")
                self.tree.column("mtime", width=180, anchor="w")
                self.tree.pack(fill=tk.BOTH, expand=True, pady=6)
                self.tree.bind("<Double-1>", lambda e: self._add_selected())

                btnbar = tk.Frame(self)
                btnbar.pack(fill=tk.X)
                tk.Button(btnbar, text="打开", command=self._add_selected, font=self.font).pack(side=tk.RIGHT, padx=6)
                tk.Button(btnbar, text="取消", command=self._cancel, font=self.font).pack(side=tk.RIGHT)

                self._refresh()

            def _cd(self, silent=False):
                d = self.dir_var.get()
                if os.path.isdir(d):
                    self.directory = d
                    self._refresh()
                    # 记录最近使用目录
                    self.parent.last_dir = d
                else:
                    if not silent:
                        messagebox.showwarning("目录不存在", f"目录不存在: {d}")

            def _on_dir_change(self, *args):
                # 输入目录后延迟刷新，避免每次按键都刷新
                if self._debounce_id is not None:
                    self.after_cancel(self._debounce_id)
                self._debounce_id = self.after(300, lambda: self._cd(silent=True))

            def _go_up(self):
                parent_dir = os.path.dirname(self.directory.rstrip(os.sep))
                if parent_dir and os.path.isdir(parent_dir):
                    self.directory = parent_dir
                    self.dir_var.set(parent_dir)
                    self.parent.last_dir = parent_dir
                    self._refresh()

            def _refresh(self):
                try:
                    files = [os.path.join(self.directory, x) for x in os.listdir(self.directory)]
                except Exception as e:
                    messagebox.showerror("错误", f"无法读取目录: {e}")
                    return
                dirs = [p for p in files if os.path.isdir(p) and not os.path.basename(p).startswith('.')]
                pdfs = [p for p in files if os.path.isfile(p) and p.lower().endswith('.pdf') and not os.path.basename(p).startswith('.')]
                if self.sort_var.get() == 'name':
                    dirs.sort(key=lambda p: os.path.basename(p).lower())
                    pdfs.sort(key=lambda p: os.path.basename(p).lower())
                else:
                    dirs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                    pdfs.sort(key=lambda p: os.path.getmtime(p), reverse=True)
                entries = [(p, True) for p in dirs] + [(p, False) for p in pdfs]
                # 刷新树形列表
                for item in self.tree.get_children():
                    self.tree.delete(item)
                for p, is_dir in entries:
                    mtime = os.path.getmtime(p)
                    mtime_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(mtime))
                    name = os.path.basename(p) + ("/" if is_dir else "")
                    self.tree.insert("", tk.END, values=(name, mtime_str))
                # 保存 full paths for retrieval
                self._displayed = entries

            def _add_selected(self):
                sel_items = list(self.tree.selection())
                if not sel_items:
                    return
                indices = [self.tree.index(item) for item in sel_items]
                selected = [self._displayed[i] for i in indices]

                # 如果只选中一个目录，则进入该目录
                if len(selected) == 1 and selected[0][1] is True:
                    self._enter_dir(selected[0][0])
                    return

                # 否则只添加文件，忽略目录
                files = [p for p, is_dir in selected if not is_dir]
                if files:
                    self.add_callback(files)
                    self.parent.last_dir = self.directory
                    self.destroy()

            def _enter_dir(self, path):
                if os.path.isdir(path):
                    self.directory = path
                    self.dir_var.set(path)
                    self.parent.last_dir = path
                    self._refresh()

            def _cancel(self):
                # 取消也记录当前目录，便于下次打开
                self.parent.last_dir = self.directory
                self.destroy()

        # 使用主窗口选定的 UI 字体以提升中文显示
        dialog_font = getattr(self, 'ui_font', None)
        # 打开即进入最近使用目录
        FileBrowserDialog(self.root, start_dir, self.add_files_from_paths, font=dialog_font)

    def add_files_from_paths(self, paths):
        skipped = []
        for f in paths:
            if isinstance(f, bytes):
                try:
                    f = f.decode('utf-8')
                except Exception:
                    f = str(f)
            # 处理 file:// 前缀
            if f.startswith('file://'):
                f = f[7:]
            f = f.replace('%20', ' ')
            # 如果是目录，扫描目录下的 PDF（非递归）
            if os.path.isdir(f):
                try:
                    children = [os.path.join(f, x) for x in os.listdir(f)]
                except Exception:
                    skipped.append(f)
                    continue
                pdfs = [p for p in children if os.path.isfile(p) and p.lower().endswith('.pdf')]
                if not pdfs:
                    skipped.append(f)
                    continue
                for p in pdfs:
                    if p in self.file_list:
                        continue
                    self.file_list.append(p)
                    self.listbox.insert(tk.END, os.path.basename(p))
                continue
            if not os.path.isfile(f) or not f.lower().endswith('.pdf'):
                skipped.append(f)
                continue
            if f in self.file_list:
                continue
            self.file_list.append(f)
            self.listbox.insert(tk.END, os.path.basename(f))
        if skipped:
            messagebox.showwarning("忽略的文件", "以下文件未被添加（非PDF或无效）:\n" + "\n".join(skipped))

    def remove_selected(self):
        selected = list(self.listbox.curselection())
        for idx in reversed(selected):
            self.listbox.delete(idx)
            del self.file_list[idx]

    def move_up(self):
        selected = list(self.listbox.curselection())
        for idx in selected:
            if idx > 0:
                self.file_list[idx-1], self.file_list[idx] = self.file_list[idx], self.file_list[idx-1]
                self._refresh_listbox(selected_idx=idx-1)

    def move_down(self):
        selected = list(self.listbox.curselection())
        for idx in reversed(selected):
            if idx < len(self.file_list)-1:
                self.file_list[idx+1], self.file_list[idx] = self.file_list[idx], self.file_list[idx+1]
                self._refresh_listbox(selected_idx=idx+1)

    def _refresh_listbox(self, selected_idx=None):
        self.listbox.delete(0, tk.END)
        for f in self.file_list:
            self.listbox.insert(tk.END, os.path.basename(f))
        if selected_idx is not None:
            self.listbox.selection_set(selected_idx)

    def browse_output(self):
        f = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF文件", "*.pdf")])
        if f:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, f)

    def start_merge(self):
        if not self.file_list:
            messagebox.showwarning("提示", "请先添加PDF文件！")
            return
        output_path = self.output_entry.get().strip()
        if not output_path:
            messagebox.showwarning("提示", "请设置输出文件名！")
            return
        self.merge_btn.config(state=tk.DISABLED)
        self.progress['value'] = 0
        threading.Thread(target=self._merge_thread, args=(output_path,), daemon=True).start()

    def _merge_thread(self, output_path):
        err = None
        try:
            from core.merger import PdfMerger
            merger = PdfMerger()
            # 将文件添加到合并器
            merger.add_files(self.file_list)

            def progress_callback(current_page, total_pages, status):
                try:
                    percent = int(current_page / total_pages * 100) if total_pages else 0
                except Exception:
                    percent = 0
                # 使用 root.after 安全更新 UI
                self.root.after(0, self.progress.config, {'value': percent})

            merger.merge(output_path, progress_callback=progress_callback)
            self.root.after(0, lambda: messagebox.showinfo("完成", "PDF合并完成！"))
        except Exception as e:
            err = str(e)
        finally:
            self.root.after(0, lambda: self.merge_btn.config(state=tk.NORMAL))
            if err:
                self.root.after(0, lambda: messagebox.showerror("错误", err))

    def _on_drop(self, event):
        try:
            raw = event.data
            try:
                paths = self.root.splitlist(raw)
            except Exception:
                paths = [raw]
            self.add_files_from_paths(paths)
        except Exception:
            traceback.print_exc()
