#!/usr/bin/env python3
"""
第一个 Python 脚本 - Hello World
目标：在 WSL2 终端中成功运行并输出结果
"""

print("=" * 40)
print("Hello! This is my first Python script.")
print("=" * 40)

# 输出系统信息
import platform
import datetime

print(f"运行时间: {datetime.datetime.now()}")
print(f"Python 版本: {platform.python_version()}")
print(f"操作系统: {platform.system()} {platform.release()}")
print("=" * 40)
print("学习记录已启动，加油！")
