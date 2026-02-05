"""
统一入口：无参数启动 GUI，有参数启动 CLI
"""
import sys


def main():
    if len(sys.argv) > 1:
        from main import run_cli
        return run_cli(sys.argv[1:])

    # 无参数启动 GUI 时，Windows 上隐藏控制台窗口
    if sys.platform.startswith("win"):
        try:
            import ctypes
            ctypes.windll.kernel32.FreeConsole()
        except Exception:
            pass

    from gui import run_gui
    run_gui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
