"""
PDF合并工具 GUI 入口
"""
import tkinter as tk
try:
    from tkinterdnd2 import TkinterDnD
    DND_ROOT = True
except Exception:
    TkinterDnD = None
    DND_ROOT = False

from ui.main_window import MainWindow


def run_gui():
    if DND_ROOT and TkinterDnD is not None:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    root.title("PDF合并工具")
    app = MainWindow(root)
    root.mainloop()


def main():
    run_gui()

if __name__ == "__main__":
    main()
