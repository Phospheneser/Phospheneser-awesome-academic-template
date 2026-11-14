"""Provider diagnostics must explain failures without retaining private text."""
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'static/python/diviner'))
import llm_integration as llm


class ProviderFailureTests(unittest.TestCase):
    def test_classifies_quota_and_other_provider_failures(self):
        for message, expected in (
            ('余额不足，请充值', 'insufficient_quota'),
            ('You exceeded your current quota', 'insufficient_quota'),
            ('invalid_api_key', 'invalid_api_key'),
            ('model_not_found', 'model_unavailable'),
            ('account_deactivated', 'account_disabled'),
            ('rate_limit_exceeded', 'rate_limited'),
            ('An unknown error', 'unclassified_provider_error'),
        ):
            response = Mock()
            response.json.return_value = {'error': {'message': message}}
            self.assertEqual(llm.provider_failure_reason(response), expected)

    def test_non_json_and_unexpected_json_are_safe(self):
        response = Mock()
        response.json.side_effect = ValueError('private response')
        self.assertEqual(llm.provider_failure_reason(response), 'non_json_response')
        response.json.side_effect = None
        for payload in ([], None, {'choices': [{'text': '余额不足'}]}):
            response.json.return_value = payload
            self.assertEqual(llm.provider_failure_reason(response), 'unclassified_provider_error')

    def test_unknown_explanation_redacts_keys_questions_and_email(self):
        response = Mock(status_code=403)
        response.json.return_value = {'error': {'message': 'Policy error: private-secret sk-another-key test@example.com private-question'}}
        client = llm.LLMIntegration()
        client.api_key = 'private-secret'
        with patch.object(llm.requests, 'post', return_value=response), self.assertLogs(llm.logger, level='WARNING') as logs:
            with self.assertRaises(Exception):
                client._call_llm_api({'system': 'system', 'user': '用户的问题是：private-question\n占卜结果'})
        output = str(logs.output)
        self.assertIn('Policy error:', output)
        for private in ('private-secret', 'sk-another-key', 'test@example.com', 'private-question'):
            self.assertNotIn(private, output)

    def test_logs_and_exceptions_never_include_provider_message_or_prompt(self):
        response = Mock(status_code=403)
        response.json.return_value = {'error': {'message': '余额不足 key=private-secret query=private-question'}}
        client = llm.LLMIntegration()
        client.api_key = 'private-secret'
        with patch.object(llm.requests, 'post', return_value=response), self.assertLogs(llm.logger, level='WARNING') as logs:
            with self.assertRaises(Exception) as caught:
                client._call_llm_api({'system': 'test', 'user': 'private-question'})
        output = str(logs.output) + str(caught.exception)
        self.assertIn('HTTP 403 reason=insufficient_quota', output)
        self.assertNotIn('private-secret', output)
        self.assertNotIn('private-question', output)


if __name__ == '__main__':
    unittest.main()
