import json
import requests
import os
import logging

logger = logging.getLogger(__name__)


def provider_failure_reason(response):
    """Classify upstream failures without exposing response text or credentials."""
    try:
        payload = response.json()
    except ValueError:
        return 'non_json_response'
    error = payload.get('error', {}) if isinstance(payload, dict) else {}
    # Only inspect error metadata, never choices or the echoed request.
    details = ' '.join(str(error.get(key, '')) for key in ('code', 'type', 'message')) if isinstance(error, dict) else str(error)
    details = details.lower()
    categories = (
        ('free_key_expired', ('老版本免费 apikey 已失效', '旧版免费密钥已失效')),
        ('insufficient_quota', ('insufficient_quota', 'insufficient_balance', 'insufficient balance', '余额不足', 'quota exceeded', 'quota_exceeded', '额度不足', '配额不足', '积分不足', 'exceeded your current quota', 'credit balance is too low')),
        ('account_disabled', ('account_deactivated', 'account disabled', 'account banned', '封禁', '已禁用')),
        ('invalid_api_key', ('invalid_api_key', 'invalid api key', 'incorrect api key', '无效的令牌', '无效的密钥')),
        ('model_unavailable', ('model_not_found', 'model not found', 'model_not_supported', '不支持此模型', '模型不存在')),
        ('rate_limited', ('rate_limit', 'rate limit', '请求次数', '请求频率')),
        ('access_denied', ('permission_denied', 'access denied', 'ip not allowed', '地区限制', '无权访问')),
    )
    for reason, markers in categories:
        if any(marker in details for marker in markers):
            return reason
    return 'unclassified_provider_error'


class LLMIntegration:
    def __init__(self):
        # 默认配置，可通过环境变量覆盖
        self.api_base = os.environ.get(
            "LLM_API_BASE", "https://api.chatanywhere.tech/v1"
        )
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.model = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")

        # 可以根据需要切换到其他免费API服务，如以下配置：
        # self.api_base = 'https://api.openai-proxy.com/v1'
        # self.api_key = 'your_api_key_here'

        # 如果使用本地部署的模型，可以配置为：
        # self.api_base = 'http://localhost:8080/v1'
        # self.api_key = 'not_used_for_local_models'

    def generate_philosophical_reply(self, query, divine_result, divination_type):
        """
        将占卜结果与查询结合，生成富有哲理的回复

        参数:
        query: 用户的查询内容
        divine_result: 占卜结果文本
        divination_type: 占卜类型（JiuGongLiuRen, LiuYaoQiGua, Tarot）

        返回:
        生成的富有哲理的回复文本
        """

        # 构建提示词
        prompt = self._build_prompt(query, divine_result, divination_type)

        if not self.api_key:
            logger.warning('AI interpretation unavailable: missing_api_key')
            raise RuntimeError('LLM is not configured')
        return self._call_llm_api(prompt)

    def _build_prompt(self, query, divine_result, divination_type):
        """构建发送给LLM的提示词"""

        # 根据不同的占卜类型，构建不同的系统提示
        type_map = {
            "JiuGongLiuRen": "九宫六壬",
            "LiuYaoQiGua": "六爻起卦",
            "Tarot": "塔罗牌",
        }

        divination_name = type_map.get(divination_type, "占卜")

        # 系统提示词
        system_prompt = f"你是一位精通{divination_name}的智者，能够将占卜结果与人生哲理相结合，给出富有启发性的解读。"

        # 用户提示词
        user_prompt = f"用户的问题是：{query}\n"
        user_prompt += f"{divination_name}的占卜结果是：{divine_result}\n"
        user_prompt += "请结合上述信息，用富有哲理的语言给出回答，帮助用户理解其中的深意和启示。回答要简洁明了，富有智慧，但不要脱离占卜结果的本意。"

        return {"system": system_prompt, "user": user_prompt}

    def _call_llm_api(self, prompt):
        """调用LLM API生成回复"""

        try:
            # 准备请求数据
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]},
                ],
                "temperature": 0.7,
            }

            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }

            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=(3, 12),  # Separate connect/read deadlines; optional work stays bounded.
            )

            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                reason = provider_failure_reason(response)
                logger.warning('AI provider rejected request: HTTP %s reason=%s', response.status_code, reason)
                raise RuntimeError(f'AI provider HTTP {response.status_code}: {reason}')
        except requests.exceptions.RequestException as e:
            # Log only the exception class; messages can contain secrets or input.
            logger.warning('AI provider network failure: %s', type(e).__name__)
            raise Exception(f"网络请求错误: {str(e)}")
        except Exception as e:
            # 其他错误处理
            raise Exception(f"LLM API调用出错: {str(e)}")


# 创建全局实例，方便其他模块导入使用
llm_integrator = LLMIntegration()
