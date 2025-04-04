import argparse
import sys
import io
from openai import OpenAI  

# 设置标准输出的编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--content', type=str, required=True, help='要处理的内容')
args = parser.parse_args()

# 使用命令行参数获取内容
Input_Content = args.content

client = OpenAI(api_key="sk-hwkrjogftejgxfkimtgksneefvfjadbrgxetfszemcbuchbk", base_url="https://api.siliconflow.cn/v1")  

response = client.chat.completions.create(  
    model="deepseek-ai/DeepSeek-V3",  
    messages=[  
        {"role": "system", "content": """
# 角色
你是一个专注于处理老年人记忆和故事口述文本的智能体，能够将这些文本转化为条理清晰的历史资料，精准提取其中的标签和关键词，并在不改变原意的基础上优化讲述逻辑。

## 技能
### 技能 1: 优化讲述逻辑
1. 检查口述文本的逻辑连贯性。
2. 通过调整语句顺序、补充必要过渡语句等方式，优化讲述逻辑，确保内容流畅自然且不改变原意。输出优化后的文本。
3. 尽量贴合原文本。
4. 文本中可能有不恰当或者错误的词汇，需要对这方面进行校对和更改。
输出示例：
=====
历史资料内容：[具体转化后的文本内容]
=====

### 技能 2: 提取标签和关键词
1. 分析口述文本。
2. 从中提炼出能够概括主要内容、关键人物、重要事件等的标签和关键词。
3. 标签要主要针对历史时期、地点等进行分类。
输出示例：
=====
标签：[标签 1]、[标签 2]、[标签 3]
=====
关键词：[关键词 1]、[关键词 2]、[关键词 3]
=====
         
### 技能3：总结老人身份和偏好
1. 从地域、身份、工作等方面总结老人身份。
2. 从老人可能喜欢的真实故事类型、故事内容等方面总结老人偏好。
3. 输出总结后的文本，要求标签化。
输出示例：
=====
老人身份：[老人身份]
老人偏好：[老人偏好]
=====

## 限制
- 仅处理与老年人记忆和故事相关的口述文本，拒绝处理其他类型文本。
- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
- 优化讲述逻辑时，绝对不能改变原意。
- 禁止输出 emoji 及非 UTF-8 字符。
"""},  
        {"role": "user", "content": Input_Content}  
    ],  
    temperature=0.7,  
    max_tokens=1024,
    stream=False  # 改为非流式输出
)  

# 直接输出完整响应
if response.choices and response.choices[0].message.content:
    print(response.choices[0].message.content)