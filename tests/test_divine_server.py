"""Real local HTTP tests; no external provider calls or API keys required."""
import concurrent.futures
import itertools
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'static/python/diviner'))
import divine_server as api
import divine_utils as algorithms


class DivineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = api.DivineServer(('127.0.0.1', 0), api.DivineHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get(self, path='/divine', **params):
        url = self.base + path + '?' + urllib.parse.urlencode(params)
        try:
            response = urllib.request.urlopen(url, timeout=2)
        except urllib.error.HTTPError as error:
            response = error
        with response:
            body = response.read()
            self.assertEqual(int(response.headers['Content-Length']), len(body))
            self.assertEqual(response.headers['Access-Control-Allow-Origin'], '*')
            return response.status, json.loads(body)

    def test_all_three_methods_work_from_any_working_directory(self):
        for mode in ['JiuGongLiuRen', 'LiuYaoQiGua', 'Tarot']:
            status, result = self.get(type=mode, query='local test')
            self.assertEqual(status, 200)
            self.assertTrue(result['success'])
            self.assertIn('local test', result['result'])

    def test_invalid_inputs_and_internal_errors_are_single_json_responses(self):
        self.assertEqual(self.get(type='invalid')[0], 400)
        self.assertEqual(self.get(query='')[0], 400)
        self.assertEqual(self.get('/missing')[0], 404)
        with patch.object(api, 'build_result', side_effect=RuntimeError('private detail')):
            with self.assertLogs(api.logger, level='ERROR'):
                status, body = self.get(query='test')
            self.assertEqual(status, 500)
            self.assertFalse(body['success'])
            self.assertNotIn('private detail', str(body))

    def test_slow_ai_does_not_block_other_requests_or_health(self):
        entered, release = threading.Event(), threading.Event()
        def slow_reply(*args):
            entered.set()
            release.wait(4)
            return 'interpretation'
        with patch.object(api, 'generate_reply', slow_reply), concurrent.futures.ThreadPoolExecutor() as pool:
            slow = pool.submit(self.get, query='slow', use_llm='true')
            try:
                self.assertTrue(entered.wait(2))
                self.assertEqual(self.get('/health')[0], 200)
                status, body = self.get(query='fast')
                self.assertEqual(status, 200)
                self.assertIn('fast', body['result'])
                self.assertFalse(slow.done())
            finally:
                release.set()
            self.assertEqual(slow.result()[1]['philosophical_reply'], 'interpretation')

    def test_ai_failure_retains_base_result(self):
        with patch.object(api, 'generate_reply', side_effect=RuntimeError('upstream unavailable')):
            status, body = self.get(query='test', use_llm='true')
        self.assertEqual(status, 200)
        self.assertTrue(body['result'])
        self.assertIn('philosophical_reply_error', body)

    def test_parallel_results_never_mix_questions(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            results = list(pool.map(lambda i: self.get(type='Tarot', query=f'question-{i}'), range(12)))
        for i, (status, body) in enumerate(results):
            self.assertEqual(status, 200)
            self.assertIn(f'question-{i}', body['result'])

    def test_all_4096_yao_combinations_resolve_available_data(self):
        info = algorithms.load_info('64gua.json')
        mapping = dict(zip('天地泽山火水风雷', '乾坤兑艮离坎巽震'))
        for yaos in itertools.product(['老阴', '阳', '阴', '老阳'], repeat=6):
            name, line = algorithms.getGuaYaoCiFromYaoListGot(yaos)
            entry = info[mapping[name[0]] + '上' + mapping[name[1]] + '下']
            if line not in entry:
                self.assertIn(line, ('用九', '用六'))
                line = '卦辞'
            self.assertTrue(entry[line]['解释'])
        for value, line in [('老阴', '用九'), ('老阳', '用六')]:
            with patch.object(algorithms, 'random_get_liu_yao', return_value=[value] * 6):
                result = api.build_result('boundary test', 'LiuYaoQiGua')
                self.assertIn(f'资料未收录{line}', result)
                self.assertIn('以下展示卦辞', result)


if __name__ == '__main__':
    unittest.main()
