#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
运行测试并生成报告的脚本
"""

import os
import subprocess
import sys

def run_tests():
    """运行测试并生成报告"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 切换到项目根目录
    os.chdir(project_root)
    
    # 确保日志目录存在
    os.makedirs("pytest_log", exist_ok=True)
    
    # 运行 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "--html=reports/report.html",
        "--self-contained-html",
        "-v",
        "--capture=sys",
        "--log-cli-level=INFO",
        "--log-file=pytest_log/pytest.log",
        "--log-file-level=DEBUG",
        "--tb=long",
        "-l",
        "--showlocals",
        "--strict-markers",
        "--log-level=INFO"
    ]
    
    print("正在运行测试...")
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n测试完成！")
        print(f"测试报告已生成到: {os.path.join(project_root, 'reports', 'report.html')}")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n测试运行失败，返回码: {e.returncode}")
        return e.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)