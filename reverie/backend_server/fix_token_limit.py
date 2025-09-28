#!/usr/bin/env python3
"""
修复脚本：将项目中的 text-davinci-003 模型替换为 gpt-3.5-turbo 并更新相关函数调用
"""

import os
import re

def fix_gpt_structure():
    """修复 gpt_structure.py 中的模型配置"""
    file_path = "/Users/gongyunbo/Documents/Github/generative_agents/reverie/backend_server/persona/prompt_template/gpt_structure.py"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 添加一个新的安全生成响应函数，使用 ChatGPT
    if 'def safe_generate_response_chatgpt(' not in content:
        new_function = '''
def safe_generate_response_chatgpt(prompt, 
                                   max_tokens=50,
                                   temperature=0.5,
                                   repeat=5,
                                   fail_safe_response="error",
                                   func_validate=None,
                                   func_clean_up=None,
                                   verbose=False): 
  """
  使用 ChatGPT 的安全响应生成函数
  这个函数将旧的 GPT-3 参数转换为 ChatGPT 调用
  """
  if verbose: 
    print("ChatGPT PROMPT:")
    print(prompt)

  for i in range(repeat): 
    try:
      # 使用 ChatGPT API
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=temperature
      )
      curr_gpt_response = completion["choices"][0]["message"]["content"].strip()
      
      if func_validate and func_validate(curr_gpt_response, prompt=prompt): 
        return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
      elif not func_validate:
        return func_clean_up(curr_gpt_response, prompt=prompt) if func_clean_up else curr_gpt_response
        
      if verbose: 
        print(f"---- repeat count: {i}")
        print(curr_gpt_response)
        print("~~~~")

    except Exception as e:
      if verbose:
        print(f"Error in attempt {i}: {str(e)}")
      pass
  
  print("FAIL SAFE TRIGGERED") 
  return fail_safe_response

'''
        # 在文件末尾添加新函数
        content += new_function
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ 已更新 gpt_structure.py")

def fix_run_gpt_prompt():
    """修复 run_gpt_prompt.py 中的所有 GPT 调用"""
    file_path = "/Users/gongyunbo/Documents/Github/generative_agents/reverie/backend_server/persona/prompt_template/run_gpt_prompt.py"
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. 首先添加导入
    if 'from gpt_structure import safe_generate_response_chatgpt' not in content:
        import_line = 'from gpt_structure import *'
        if import_line in content:
            content = content.replace(import_line, import_line + '\\nfrom gpt_structure import safe_generate_response_chatgpt')
        else:
            # 在文件开头添加导入
            lines = content.split('\\n')
            for i, line in enumerate(lines):
                if line.startswith('from ') or line.startswith('import '):
                    lines.insert(i + 1, 'from gpt_structure import safe_generate_response_chatgpt')
                    break
            content = '\\n'.join(lines)
    
    # 2. 替换所有的 safe_generate_response 调用为新的函数
    # 查找模式：safe_generate_response(prompt, gpt_param, 5, fail_safe, __func_validate, __func_clean_up)
    pattern = r'safe_generate_response\s*\(\s*prompt\s*,\s*gpt_param\s*,\s*(\d+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)'
    
    def replace_function(match):
        repeat = match.group(1)
        fail_safe = match.group(2)
        func_validate = match.group(3)
        func_clean_up = match.group(4)
        
        return f'safe_generate_response_chatgpt(prompt, max_tokens=gpt_param.get("max_tokens", 50), temperature=gpt_param.get("temperature", 0.5), repeat={repeat}, fail_safe_response={fail_safe}, func_validate={func_validate}, func_clean_up={func_clean_up})'
    
    content = re.sub(pattern, replace_function, content)
    
    # 3. 处理其他模式的 safe_generate_response 调用
    pattern2 = r'safe_generate_response\s*\(\s*prompt\s*,\s*gpt_param\s*,\s*(\d+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\s*\)'
    content = re.sub(pattern2, replace_function, content)
    
    # 4. 注释掉或删除旧的 gpt_param 定义（可选）
    # 保留它们以防需要参考参数值
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print("✅ 已更新 run_gpt_prompt.py")

def main():
    print("🔧 开始修复 TOKEN LIMIT EXCEEDED 问题...")
    print("=" * 60)
    
    try:
        # 1. 修复 gpt_structure.py
        fix_gpt_structure()
        
        # 2. 修复 run_gpt_prompt.py  
        fix_run_gpt_prompt()
        
        print("=" * 60)
        print("🎉 修复完成！")
        print("✅ 已将所有 text-davinci-003 调用替换为 gpt-3.5-turbo")
        print("✅ 现在可以重新运行仿真了")
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    main()