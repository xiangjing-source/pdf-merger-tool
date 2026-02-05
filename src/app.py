"""
统一入口：无参数启动 GUI，有参数启动 CLI
"""
import sys


def main():
    if len(sys.argv) > 1:
        from main import run_cli
        return run_cli(sys.argv[1:])
    from gui import run_gui
    run_gui()
    return 0


if __name__ == "__main__":
    sys.exit(main())
