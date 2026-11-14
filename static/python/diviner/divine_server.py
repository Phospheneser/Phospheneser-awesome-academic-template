#!/usr/bin/env python3
"""Small JSON API. Compute a complete response before sending its status."""
import http.server
import json
import logging
import os
import sys
import threading
import urllib.parse

from divine_utils import JiuGongLiuRen, LiuYaoQiGua, Tarot

logger = logging.getLogger(__name__)
# Legacy algorithms seed the process-wide random generator. Keep only the
# short local calculation under a lock; network I/O must never hold it.
calculation_lock = threading.Lock()
llm_slots = threading.BoundedSemaphore(2)


def build_result(query, div_type):
    with calculation_lock:
        if div_type == 'JiuGongLiuRen':
            values = JiuGongLiuRen(query, need_return=True, need_print=False)
            return f'对于你的问题：【{query}】  得到的卦象是\n【' + '】->【'.join(values) + '】'
        if div_type == 'Tarot':
            cards, records, _, orientations = Tarot(query, need_return=True, need_print=False)
            lines = [f'对于你的问题：【{query}】', '抽到的卡牌如下']
            for i, (card, record, orientation) in enumerate(zip(cards, records, orientations), 1):
                direction = '正位' if orientation else '逆位'
                lines.append(f'卡{i} :【{direction} {card} : {record[card][direction + "关键词"]} 】')
            return '\n'.join(lines)
        if div_type == 'LiuYaoQiGua':
            _, line, _, info, yaos = LiuYaoQiGua(query, need_return=True, need_print=False)
            symbols = {'老阳': '---------- o', '老阴': '----  ---- x', '阳': '----------', '阴': '----  ----'}
            lines = [f'对于你的问题：【{query}】', '卜卦结果如下', *[symbols[yao] for yao in reversed(yaos)]]
            lines.append(f'得到的是【{info["卦名"].split("(")[0]}({info["卦名直解"]})】')
            if line not in info:
                lines.append(f'资料未收录{line}，以下展示卦辞。')
                line = '卦辞'
            detail = info[line]
            lines.extend([f'{line}：【{"".join(detail["原文"])}】', f'解释为：【{"".join(detail["解释"])}】', f'吉凶/性质：【{detail["吉凶/性质"]}】'])
            return '\n'.join(lines)
    raise ValueError('未知的占卜类型')


def generate_reply(query, result, div_type):
    # Basic divination has no third-party package or LLM dependency.
    from llm_integration import llm_integrator
    return llm_integrator.generate_philosophical_reply(query, result, div_type)


class DivineHandler(http.server.BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass  # Closing a browser panel is not an application error.

    def do_GET(self):
        path = urllib.parse.urlparse(self.path)
        if path.path == '/health':
            self.send_json(200, {'success': True, 'status': 'ok'})
            return
        if path.path != '/divine':
            self.send_json(404, {'success': False, 'error': 'Not found'})
            return
        params = urllib.parse.parse_qs(path.query, keep_blank_values=True)
        query = params.get('query', ['今日运势'])[0].strip()
        div_type = params.get('type', ['JiuGongLiuRen'])[0]
        if not query or len(query) > 1000 or div_type not in {'JiuGongLiuRen', 'LiuYaoQiGua', 'Tarot'}:
            self.send_json(400, {'success': False, 'error': '问题不能为空、不能超过 1000 字，且必须选择有效的占卜方式。'})
            return
        try:
            result = build_result(query, div_type)
            response = {'success': True, 'query': query, 'type': div_type, 'result': result}
            if params.get('use_llm', ['false'])[0].lower() == 'true':
                if llm_slots.acquire(blocking=False):
                    try:
                        response['philosophical_reply'] = generate_reply(query, result, div_type)
                    except Exception:
                        # Keep the useful base result without leaking provider details.
                        response['philosophical_reply_error'] = 'AI 解读暂时不可用'
                    finally:
                        llm_slots.release()
                else:
                    response['philosophical_reply_error'] = 'AI 解读繁忙'
            self.send_json(200, response)
        except Exception:
            logger.exception('Divination calculation failed for %s', div_type)
            self.send_json(500, {'success': False, 'error': '占卜计算暂时失败，请稍后重试。'})

    def do_OPTIONS(self):
        self.send_json(200, {'success': True})

    def log_message(self, format, *args):
        # Do not put the visitor's question (query string) into access logs.
        logger.info('%s %s', self.command, urllib.parse.urlparse(self.path).path)


class DivineServer(http.server.ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def run_server(port=8000):
    logging.basicConfig(level=logging.INFO)
    with DivineServer(('', port), DivineHandler) as server:
        print(f'启动占卜API服务器，监听端口：{port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print('服务器已停止', flush=True)


if __name__ == '__main__':
    run_server(int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 8000)))
