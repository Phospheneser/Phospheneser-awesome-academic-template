#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
占卜服务器保活工具

该模块提供了一个保活机制，用于定期向服务器发送请求，防止服务器因长时间不活跃而被强制掉盘。
"""
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - 保活服务 - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class KeepAliveService:
    def __init__(self, server_url="http://localhost:8000", interval=600):
        """
        初始化保活服务

        参数:
        server_url (str): 服务器基础URL，默认是'http://localhost:8000'
        interval (int): 发送请求的间隔时间（秒），默认是600秒（10分钟）
        """
        self.server_url = server_url
        self.interval = interval
        self.thread = None
        self.running = False

        # 默认请求参数
        self.default_request = {
            "path": "/divine",
            "params": {"type": "JiuGongLiuRen", "query": "保活请求"},
        }

    def start(self):
        """启动保活服务"""
        if self.running:
            logger.info("保活服务已经在运行中")
            return

        self.running = True
        self.thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.thread.start()
        logger.info(
            f"保活服务已启动，将每{self.interval//60}分钟发送一次请求到{self.server_url}"
        )

    def stop(self):
        """停止保活服务"""
        if not self.running:
            logger.info("保活服务未在运行")
            return

        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
        logger.info("保活服务已停止")

    def _keep_alive_loop(self):
        """保活循环，定期发送请求"""
        while self.running:
            try:
                self._send_keep_alive_request()
            except Exception as e:
                logger.error(f"保活请求发送失败: {e}")

            # 等待指定的时间间隔
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)

    def _send_keep_alive_request(self):
        """发送保活请求到服务器"""
        # 构造请求URL
        path = self.default_request["path"]
        params = self.default_request["params"]

        # 构建查询字符串
        query_string = "&".join(
            [f"{key}={urllib.parse.quote(str(value))}" for key, value in params.items()]
        )
        request_url = f"{self.server_url}{path}?{query_string}"

        logger.info(f"发送保活请求: {request_url}")

        # 设置请求头
        headers = {
            "User-Agent": "Divine-Server-KeepAlive/1.0",
            "Content-Type": "application/json",
        }

        # 发送请求
        try:
            req = urllib.request.Request(request_url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                status_code = response.getcode()
                if status_code == 200:
                    # 尝试解析响应内容
                    try:
                        response_data = json.loads(response.read().decode("utf-8"))
                        logger.info(f"保活请求成功，服务器返回状态码: {status_code}")
                    except json.JSONDecodeError:
                        logger.warning(
                            f"保活请求成功，但无法解析响应内容，状态码: {status_code}"
                        )
                else:
                    logger.warning(f"保活请求失败，状态码: {status_code}")
        except urllib.error.URLError as e:
            logger.error(f"保活请求URL错误: {e}")
        except urllib.error.HTTPError as e:
            logger.error(f"保活请求HTTP错误: {e.code} - {e.reason}")
        except Exception as e:
            logger.error(f"保活请求发生未知错误: {e}")


# 如果作为主程序运行，则启动一个简单的测试
if __name__ == "__main__":
    print("保活服务测试模式")
    keep_alive = KeepAliveService(interval=30)  # 测试时使用30秒间隔
    try:
        keep_alive.start()
        print("按Ctrl+C停止测试")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n停止测试...")
        keep_alive.stop()
        print("测试已停止")
