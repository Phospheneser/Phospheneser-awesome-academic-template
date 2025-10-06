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

# 导入保活服务模块
from keep_alive_utils import KeepAliveService

# 获取脚本所在目录的绝对路径
script_dir = os.path.dirname(os.path.abspath(__file__))

# 检查divine_server.py文件是否存在
server_file = os.path.join(script_dir, "divine_server.py")
if not os.path.exists(server_file):
    print(f"错误: 找不到服务器文件 {server_file}")
    sys.exit(1)

# 检查divine_utils.py文件是否存在
utils_file = os.path.join(script_dir, "divine_utils.py")
if not os.path.exists(utils_file):
    print(f"错误: 找不到工具文件 {utils_file}")
    sys.exit(1)

# 检查JSON数据文件是否存在
info_dir = os.path.join(script_dir, "info")
if not os.path.exists(info_dir):
    print(f"错误: 找不到数据目录 {info_dir}")
    sys.exit(1)

json_files = ["64gua.json", "MergedTarot.json"]
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
    # 检查是否在Render环境中运行
    import os

    is_render_env = "RENDER" in os.environ or "RENDER_SERVICE_NAME" in os.environ

    if is_render_env:
        # 在Render环境中，直接导入并运行divine_server.py的主函数，以减少启动时间
        print("在Render环境中运行，直接启动divine_server...")
        from divine_server import run_server

        # 使用环境变量PORT或默认端口
        port = int(os.environ.get("PORT", 8000))
        print(f"使用端口: {port}")

        # 不启动保活服务，因为Render环境中保活服务可能导致额外的复杂性
        print("在Render环境中，跳过保活服务启动")

        # 直接运行服务器
        run_server(port)
    else:
        # 在本地环境中，使用子进程方式运行
        # 使用当前Python解释器运行divine_server.py
        process = subprocess.Popen(
            [sys.executable, server_file],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        # 显示服务器输出
        for line in process.stdout:
            print(line.strip())

            # 检查服务器是否成功启动 - 修改为匹配中文输出
            if "启动占卜API服务器" in line:
                print("\n服务器已成功启动！")
                print("您可以通过网页中的占卜小人访问占卜功能。")
                print("或者直接访问 http://localhost:8000/ 来测试API")

                # 启动保活服务
                try:
                    # 尝试从输出中提取端口号
                    import re

                    port_match = re.search(
                        r"端口：(\d+)", line
                    )  # 修改正则表达式以匹配中文输出
                    port = int(port_match.group(1)) if port_match else 8000

                    # 初始化并启动保活服务
                    # 在本地环境中，使用localhost
                    keep_alive = KeepAliveService(server_url=f"http://localhost:{port}")
                    print(
                        f"\n保活服务已启动，将每10分钟发送一次保活请求到 http://localhost:{port}"
                    )

                    keep_alive.start()
                except Exception as e:
                    print(f"启动保活服务时发生错误: {e}")

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
