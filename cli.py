from AI.agent.api import ModelApi
from AI.agent.tools import RunTools
from AI.agent.config import prompt, tools

import os

# 从环境变量中获取OpenAI API密钥
API_KEY = os.getenv('API_KEY')
# 从环境变量中获取OpenAI API URL
API_URL = os.getenv('API_URL')

def run():
    messages = [{"role": "system", "content": prompt}]
    api = ModelApi(API_KEY, API_URL)

    while True:
        user_input = input("👤: ")
        messages.append({"role": "user", "content": user_input})
        while True:
            response = api.oneapi(messages, model="gpt-4o", tools=tools, choices="auto", response_format=None)
            if response['type'] == 'message':
                response_message = response['message']
                print("🤖:", response_message)
                messages.append({"role": "assistant", "content": response_message})
                break  
            elif response['type'] == 'tools':
                # print("工具响应调试:", response)
                messages.append(response['message'])
                tool_calls = response['tools']
                tool_messages = RunTools(tool_calls)
                messages.extend(tool_messages)

if __name__ == "__main__":
    run()