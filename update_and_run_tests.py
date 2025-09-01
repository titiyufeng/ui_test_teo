#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从GitHub获取最新代码并运行测试的Python脚本
"""

import os
import subprocess
import sys


def run_command(command, continue_on_error=False):
    """
    运行命令并返回结果
    
    参数:
        command (str or list): 要运行的命令
        continue_on_error (bool): 命令失败时是否继续执行
    
    返回:
        tuple: (返回码, 标准输出, 错误输出)
    """
    try:
        print(f"正在执行: {' '.join(command) if isinstance(command, list) else command}")
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        
        if result.stdout:
            print(result.stdout)
            
        if result.stderr:
            print(f"错误输出: {result.stderr}", file=sys.stderr)
            
        if result.returncode != 0 and not continue_on_error:
            print(f"命令执行失败，返回码: {result.returncode}")
            
        return result.returncode, result.stdout, result.stderr
        
    except Exception as e:
        print(f"执行命令时发生异常: {e}")
        if not continue_on_error:
            sys.exit(1)
        return -1, "", str(e)


def main():
    """主函数：更新代码并运行测试"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    print(f"项目根目录: {project_root}")
    
    # 切换到项目目录
    os.chdir(project_root)
    
    # 从GitHub更新代码
    print("正在从GitHub更新代码...")
    git_return_code, _, _ = run_command("git pull", continue_on_error=True)
    
    # 无论git pull结果如何都继续执行
    if git_return_code != 0:
        print("Git pull失败，但继续执行测试...")
    else:
        print("Git pull成功")
    
    # 检查虚拟环境是否存在
    venv_python = os.path.join(project_root, ".venv", "Scripts", "python.exe")
    if not os.path.exists(venv_python):
        print("错误: 未找到虚拟环境，请先创建虚拟环境")
        sys.exit(1)
    
    # 使用虚拟环境中的Python运行测试
    print("正在使用虚拟环境运行测试...")
    test_command = f'"{venv_python}" run_tests.py'
    test_return_code, _, _ = run_command(test_command)
    
    if test_return_code != 0:
        print("测试运行失败")
        sys.exit(test_return_code)
    
    print("测试运行完成!")


if __name__ == "__main__":
    main()