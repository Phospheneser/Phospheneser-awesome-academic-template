#!/usr/bin/env python3
import http.server
import socketserver
import json
import urllib.parse
import sys
import os

# 添加当前目录到Python路径，确保能够正确导入divine_utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置工作目录为当前目录，确保能够正确加载JSON文件
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from divine_utils import JiuGongLiuRen, LiuYaoQiGua, Tarot
from llm_integration import llm_integrator


class DivineHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析URL参数
        parsed_path = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_path.query)

        # 检查是否是占卜API请求
        if parsed_path.path == "/divine":
            try:
                # 获取参数
                query = params.get("query", ["今日运势"])[0]
                div_type = params.get("type", ["JiuGongLiuRen"])[0]
                # 添加是否使用LLM生成哲理回复的参数，默认为False
                use_llm = params.get("use_llm", ["false"])[0].lower() == "true"

                # 设置返回结果的编码
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                # 添加CORS头
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                self.send_header(
                    "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
                )
                self.end_headers()

                # 根据占卜类型调用相应的函数
                if div_type == "JiuGongLiuRen":
                    # 调用九宫六壬占卜函数，获取返回结果
                    result = []

                    def capture_print(text):
                        result.append(text)

                    # 保存原始的print函数
                    original_stdout = sys.stdout
                    # 创建一个StringIO对象来捕获输出
                    from io import StringIO

                    sys.stdout = StringIO()

                    try:
                        # 调用占卜函数
                        JiuGongLiuRen(query, need_return=False, need_print=True)
                        # 获取捕获的输出
                        result_output = sys.stdout.getvalue()
                        result = result_output.strip().split("\n")
                    finally:
                        # 恢复原始的stdout
                        sys.stdout = original_stdout

                    # 构建返回结果
                    response = {
                        "success": True,
                        "query": query,
                        "type": div_type,
                        "result": "\n".join(result),
                    }

                    # 如果需要使用LLM生成哲理回复
                    if use_llm:
                        try:
                            philosophical_reply = (
                                llm_integrator.generate_philosophical_reply(
                                    query, "\n".join(result), div_type
                                )
                            )
                            response["philosophical_reply"] = philosophical_reply
                        except Exception as llm_error:
                            print(f"生成哲理回复时出错: {str(llm_error)}")
                            # 出错时不影响原始占卜结果的返回
                            response["philosophical_reply_error"] = str(llm_error)
                elif div_type == "LiuYaoQiGua":
                    # 调用六爻起卦占卜函数，获取返回结果
                    result = []

                    def capture_print(text):
                        result.append(text)

                    # 保存原始的print函数
                    original_stdout = sys.stdout
                    # 创建一个StringIO对象来捕获输出
                    from io import StringIO

                    sys.stdout = StringIO()

                    try:
                        # 调用占卜函数
                        LiuYaoQiGua(query, need_return=False, need_print=True)
                        # 获取捕获的输出
                        result_output = sys.stdout.getvalue()
                        result = result_output.strip().split("\n")
                    finally:
                        # 恢复原始的stdout
                        sys.stdout = original_stdout

                    # 构建返回结果
                    response = {
                        "success": True,
                        "query": query,
                        "type": div_type,
                        "result": "\n".join(result),
                    }

                    # 如果需要使用LLM生成哲理回复
                    if use_llm:
                        try:
                            philosophical_reply = (
                                llm_integrator.generate_philosophical_reply(
                                    query, "\n".join(result), div_type
                                )
                            )
                            response["philosophical_reply"] = philosophical_reply
                        except Exception as llm_error:
                            print(f"生成哲理回复时出错: {str(llm_error)}")
                            # 出错时不影响原始占卜结果的返回
                            response["philosophical_reply_error"] = str(llm_error)
                elif div_type == "Tarot":
                    # 调用塔罗牌占卜函数，获取返回结果
                    result = []

                    def capture_print(text):
                        result.append(text)

                    # 保存原始的print函数
                    original_stdout = sys.stdout
                    # 创建一个StringIO对象来捕获输出
                    from io import StringIO

                    sys.stdout = StringIO()

                    try:
                        # 调用占卜函数
                        Tarot(query, need_return=False, need_print=True)
                        # 获取捕获的输出
                        result_output = sys.stdout.getvalue()
                        result = result_output.strip().split("\n")
                    finally:
                        # 恢复原始的stdout
                        sys.stdout = original_stdout

                    # 构建返回结果
                    response = {
                        "success": True,
                        "query": query,
                        "type": div_type,
                        "result": "\n".join(result),
                    }

                    # 如果需要使用LLM生成哲理回复
                    if use_llm:
                        try:
                            philosophical_reply = (
                                llm_integrator.generate_philosophical_reply(
                                    query, "\n".join(result), div_type
                                )
                            )
                            response["philosophical_reply"] = philosophical_reply
                        except Exception as llm_error:
                            print(f"生成哲理回复时出错: {str(llm_error)}")
                            # 出错时不影响原始占卜结果的返回
                            response["philosophical_reply_error"] = str(llm_error)
                else:
                    response = {"success": False, "error": "未知的占卜类型"}

                # 发送JSON响应
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                response = {"success": False, "error": str(e)}
                self.wfile.write(
                    json.dumps(response, ensure_ascii=False).encode("utf-8")
                )
        else:
            # 其他请求返回404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    # 处理OPTIONS请求，用于CORS预检
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
        )
        self.end_headers()


def run_server(port=8000):
    # 获取本机IP地址
    import socket

    try:
        # 创建一个socket连接来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # 连接到公共DNS服务器
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"  # 如果无法获取，默认为localhost

    print(f"启动占卜API服务器，监听端口：{port}")
    print(f"本地访问地址：http://{local_ip}:{port}")
    print(f"localhost访问地址：http://localhost:{port}")
    print("请在浏览器中打开页面，并确保本服务器保持运行状态")
    print("使用方法：")
    print(f"  1. 运行此脚本")
    print(f"  2. 在浏览器中打开您的网页")
    print(f"  3. 点击占卜小人进行占卜")
    print(" ")
    print("如需停止服务器，请按 Ctrl+C")

    with socketserver.TCPServer(("", port), DivineHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")
            httpd.server_close()


if __name__ == "__main__":
    # 允许通过环境变量PORT指定端口（适应Render等平台）
    # 优先使用环境变量PORT，然后是命令行参数，最后是默认端口
    import os

    port = 8000

    # 首先检查环境变量PORT
    if "PORT" in os.environ:
        try:
            port = int(os.environ["PORT"])
            print(f"使用环境变量PORT指定的端口: {port}")
        except ValueError:
            print(
                f"环境变量PORT的值 '{os.environ['PORT']}' 不是有效的端口号，使用默认端口8000"
            )

    # 然后检查命令行参数
    elif len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("端口号必须是数字，使用默认端口8000")

    run_server(port)
