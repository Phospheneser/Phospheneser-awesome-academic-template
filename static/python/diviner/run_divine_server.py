#!/usr/bin/env python3
"""
占卜服务器启动脚本

这个脚本提供了一个简单的方式来启动占卜功能的API服务器。
它会自动运行divine_server.py，并显示服务器启动信息。
"""
import os
import sys
import subprocess
import time

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 检查divine_server.py文件是否存在
server_file = os.path.join(script_dir, 'divine_server.py')
if not os.path.exists(server_file):
    print(f"错误: 找不到服务器文件 {server_file}")
    sys.exit(1)

# 检查divine_utils.py文件是否存在
utils_file = os.path.join(script_dir, 'divine_utils.py')
if not os.path.exists(utils_file):
    print(f"错误: 找不到工具文件 {utils_file}")
    sys.exit(1)

# 检查JSON数据文件是否存在
info_dir = os.path.join(script_dir, 'info')
if not os.path.exists(info_dir):
    print(f"错误: 找不到数据目录 {info_dir}")
    sys.exit(1)

json_files = ['64gua.json', 'MergedTarot.json']
for json_file in json_files:
    full_path = os.path.join(info_dir, json_file)
    if not os.path.exists(full_path):
        print(f"警告: 找不到数据文件 {full_path}")

# 显示启动信息
print("===== 占卜服务器启动器 =====")
print(f"正在启动占卜API服务器...")
print(f"服务器文件: {server_file}")
print(f"数据目录: {info_dir}")
print("按Ctrl+C可以停止服务器")
print("==========================\n")

# 启动服务器进程
try:
    # 使用当前Python解释器运行divine_server.py
    process = subprocess.Popen(
        [sys.executable, server_file],
        cwd=script_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # 显示服务器输出
    for line in process.stdout:
        print(line.strip())
        
        # 检查服务器是否成功启动
        if 'Starting server on port' in line:
            print("\n服务器已成功启动！")
            print("您可以通过网页中的占卜小人访问占卜功能。")
            print("或者直接访问 http://localhost:8000/ 来测试API")
    
    # 等待进程结束
    process.wait()
    
except KeyboardInterrupt:
    print("\n正在停止服务器...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("服务器已停止")
except Exception as e:
    print(f"启动服务器时发生错误: {e}")
    sys.exit(1)