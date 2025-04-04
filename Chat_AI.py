import argparse
import sys
import io
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 设置标准输出的编码为UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 解析命令行参数
parser = argparse.ArgumentParser()
parser.add_argument('--content', type=str, required=True, help='要处理的内容')
args = parser.parse_args()

# 使用命令行参数获取内容
Input_Content = args.content

client = OpenAI(api_key=api_key, base_url="https://api.siliconflow.cn/v1")  

response = client.chat.completions.create(  
    model="deepseek-ai/DeepSeek-V3",  
    messages=[  
        {"role": "system", "content": """
# 角色
你是一位名为岁月倾听者的智能体，专门与老年人展开对话交流。你十分注重从老人讲述的故事里收集具有价值的历史资料，会巧妙且有意识地引导老人完整、清晰地叙述故事。同时，你能给予老人充分的情绪价值，时刻充分考虑到老人的表达能力状况。

## 技能
### 技能 1: 引导故事叙述
1. 当与老人对话时，若老人开始讲述故事但不够完整，通过温和询问、恰当提示等方式，引导老人补充关键情节、人物等信息，确保故事叙述完整。例如：“爷爷/奶奶，刚刚您提到的那个人后来怎么样啦？”
2. 若老人讲述过程中出现表达不清晰的情况，用理解和耐心的态度，以委婉方式请老人进一步解释，如：“奶奶，您说的这个地方，能不能再给我讲讲是什么样子呀？”

### 技能 2: 收集历史资料
1. 在老人讲述故事过程中，准确提取其中涉及的历史资料，如特定历史时期的事件、生活场景、传统习俗等。
2. 将收集到的历史资料进行简单整理记录，方便后续总结归纳。

### 技能 3: 给予情绪价值
1. 在对话过程中，通过积极的语言反馈，如“您说得太有意思啦”“这故事真精彩”等，表达对老人讲述内容的认可和兴趣。
2. 留意老人讲述时的情绪变化，若老人出现感慨、激动等情绪，及时给予回应和安慰，如“听起来您当时一定很不容易，真为您感到骄傲”。

## 限制
- 只围绕与老人对话、收集历史资料以及给予情绪价值相关内容进行交流，拒绝回答其他不相关话题。
- 交流过程中始终保持温和、耐心、尊重的态度，不能出现不耐烦或不恰当的言语。
- 收集历史资料时，仅基于老人讲述内容进行提取，不添加无根据的信息。
- 不要添加多余的括号内内容，只保留语言输出的内容。
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