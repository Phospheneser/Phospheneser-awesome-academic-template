import os
import json
import requests

class LLMIntegration:
    def __init__(self):
        # 默认使用ChatAnywhere提供的免费API，也可以通过环境变量配置
        self.api_base = os.environ.get('LLM_API_BASE', 'https://api.chatanywhere.tech/v1')
        self.api_key = os.environ.get('LLM_API_KEY', 'free')  # ChatAnywhere的免费API可以使用'free'作为key
        self.model = os.environ.get('LLM_MODEL', 'gpt-3.5-turbo')
        
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
        
        try:
            # 调用LLM API
            response = self._call_llm_api(prompt)
            return response
        except Exception as e:
            # 出错时返回原始占卜结果，确保服务不中断
            print(f"LLM API调用失败: {str(e)}")
            return divine_result
    
    def _build_prompt(self, query, divine_result, divination_type):
        """构建发送给LLM的提示词"""
        
        # 根据不同的占卜类型，构建不同的系统提示
        type_map = {
            'JiuGongLiuRen': '九宫六壬',
            'LiuYaoQiGua': '六爻起卦',
            'Tarot': '塔罗牌'
        }
        
        divination_name = type_map.get(divination_type, '占卜')
        
        # 系统提示词
        system_prompt = f"你是一位精通{divination_name}的智者，能够将占卜结果与人生哲理相结合，给出富有启发性的解读。"
        
        # 用户提示词
        user_prompt = f"用户的问题是：{query}\n"
        user_prompt += f"{divination_name}的占卜结果是：{divine_result}\n"
        user_prompt += "请结合上述信息，用富有哲理的语言给出回答，帮助用户理解其中的深意和启示。回答要简洁明了，富有智慧，但不要脱离占卜结果的本意。"
        
        return {
            "system": system_prompt,
            "user": user_prompt
        }
    
    def _call_llm_api(self, prompt):
        """调用LLM API生成回复"""
        
        try:
            # 准备请求数据
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                "temperature": 0.7
            }
            
            # 发送请求
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=30  # 设置30秒超时
            )
            
            # 检查响应状态
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    error_msg = error_data.get("error", {}).get("message", f"API调用失败，状态码: {response.status_code}")
                except:
                    error_msg = f"API调用失败，状态码: {response.status_code}"
                
                raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            # 网络错误处理
            raise Exception(f"网络请求错误: {str(e)}")
        except Exception as e:
            # 其他错误处理
            raise Exception(f"LLM API调用出错: {str(e)}")

# 创建全局实例，方便其他模块导入使用
llm_integrator = LLMIntegration()