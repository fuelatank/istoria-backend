import subprocess
import json
import sys
import io
import re

# 设置标准输出的编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 存储所有用户对话内容
user_conversation = ""

while True:
    # 获取用户输入
    print("\n请输入您的内容（输入'退出'结束对话）：")
    Content = input()
    
    # 检查是否退出
    if Content.lower() == '退出':
        break
    
    # 将当前用户对话添加到总对话中
    user_conversation += Content + "\n"
    
    # 调用Chat_AI.py并获取AI回复
    # 使用json.dumps确保内容正确传递
    process = subprocess.Popen(['python', 'Chat_AI.py', '--content', json.dumps(Content)], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True,
                             encoding='utf-8')
    stdout, stderr = process.communicate()
    
    # 打印AI回复
    if stdout:
        print("\nAI回复：")
        print(stdout)
    if stderr:
        print("错误：", stderr)

# 保存用户对话到文件
with open('user_conversation.txt', 'w', encoding='utf-8') as f:
    f.write(user_conversation)
print("\n用户对话已保存到 user_conversation.txt")

# 调用Summary_AI.py处理保存的对话内容
print("\n正在对对话内容进行总结...")
try:
    process = subprocess.Popen(['python', 'Summary_AI.py', '--content', json.dumps(user_conversation)], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE, 
                             text=True,
                             encoding='utf-8')
    stdout, stderr = process.communicate()
    
    # 打印总结结果
    if stdout:
        print("\n总结结果：")
        print(stdout)
        
        # 提取并保存不同部分的内容
        # 历史资料内容
        history_match = re.search(r'=====\n历史资料内容：(.*?)\n=====', stdout, re.DOTALL)
        if history_match:
            with open('history_content.txt', 'w', encoding='utf-8') as f:
                f.write(history_match.group(1).strip())
        
        # 标签
        tags_match = re.search(r'=====\n标签：(.*?)\n=====', stdout, re.DOTALL)
        if tags_match:
            with open('tags.txt', 'w', encoding='utf-8') as f:
                f.write(tags_match.group(1).strip())
        
        # 关键词
        keywords_match = re.search(r'=====\n关键词：(.*?)\n=====', stdout, re.DOTALL)
        if keywords_match:
            with open('keywords.txt', 'w', encoding='utf-8') as f:
                f.write(keywords_match.group(1).strip())
        
        # 老人身份
        identity_match = re.search(r'=====\n老人身份：(.*?)\n=====', stdout, re.DOTALL)
        if identity_match:
            with open('identity.txt', 'w', encoding='utf-8') as f:
                f.write(identity_match.group(1).strip())
        
        # 老人偏好
        preferences_match = re.search(r'=====\n老人偏好：(.*?)\n=====', stdout, re.DOTALL)
        if preferences_match:
            with open('preferences.txt', 'w', encoding='utf-8') as f:
                f.write(preferences_match.group(1).strip())
        
        print("\n总结内容已分别保存到以下文件：")
        print("- history_content.txt：历史资料内容")
        print("- tags.txt：标签")
        print("- keywords.txt：关键词")
        print("- identity.txt：老人身份")
        print("- preferences.txt：老人偏好")
    
    if stderr:
        print("错误：", stderr)
except Exception as e:
    print(f"总结过程中出现错误：{str(e)}")