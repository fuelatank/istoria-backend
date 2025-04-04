import sys
import io
from openai import OpenAI  

# 设置标准输出的编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 从preferences.txt读取老人偏好
try:
    with open('preferences.txt', 'r', encoding='utf-8') as f:
        preferences = f.read()
except Exception as e:
    print(f"读取preferences.txt时出错：{str(e)}")
    sys.exit(1)

client = OpenAI(api_key="sk-hwkrjogftejgxfkimtgksneefvfjadbrgxetfszemcbuchbk", base_url="https://api.siliconflow.cn/v1")  

response = client.chat.completions.create(  
    model="deepseek-ai/DeepSeek-V3",  
    messages=[  
        {"role": "system", "content": """
你是一位专业的说书人，擅长根据老人的偏好和兴趣讲述故事。你的任务是：

1. 根据老人的偏好和兴趣，创作一个适合老人听的故事
2. 使用说书的形式讲述故事，包括：
   - 适当的停顿和语气变化
   - 生动的描述和细节
   - 符合老人接受习惯的表达方式
3. 故事要：
   - 情节简单易懂
   - 语言通俗易懂
   - 包含老人熟悉的生活元素
4. 输出格式：
=====
故事标题：[故事标题]

[故事内容，使用说书的形式，包含适当的停顿和语气变化]
=====
"""},  
        {"role": "user", "content": f"根据以下老人偏好，创作一个适合的故事：\n{preferences}"}  
    ],  
    temperature=0.7,  
    max_tokens=1024,
    stream=False  # 改为非流式输出
)  

# 直接输出完整响应
if response.choices and response.choices[0].message.content:
    print(response.choices[0].message.content) 