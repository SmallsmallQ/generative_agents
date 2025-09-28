#!/usr/bin/env python3
"""
测试修复后的 GPT 功能是否正常工作
"""

import sys
import os

# 添加路径
sys.path.append('/Users/gongyunbo/Documents/Github/generative_agents/reverie/backend_server')
sys.path.append('/Users/gongyunbo/Documents/Github/generative_agents/reverie/backend_server/persona/prompt_template')

try:
    from gpt_structure import safe_generate_response_chatgpt
    from utils import openai_api_key, openai_api_base
    import openai
    
    # 配置 API
    openai.api_key = openai_api_key
    openai.api_base = openai_api_base
    
    print("🧪 测试新的 safe_generate_response_chatgpt 函数...")
    
    def test_validate(response, prompt=""):
        """简单的验证函数"""
        return len(response.strip()) > 0
    
    def test_cleanup(response, prompt=""):
        """简单的清理函数"""
        return response.strip()
    
    # 测试简单的提示
    test_prompt = "Generate a simple daily activity for someone waking up at 6am. Just one sentence."
    
    result = safe_generate_response_chatgpt(
        prompt=test_prompt,
        max_tokens=50,
        temperature=0.5,
        repeat=3,
        fail_safe_response="wake up and brush teeth",
        func_validate=test_validate,
        func_clean_up=test_cleanup,
        verbose=True
    )
    
    print(f"\n✅ 测试成功!")
    print(f"结果: {result}")
    
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()