import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

with open("problem.json", "r", encoding="utf-8") as f:
    problems = json.load(f)

# Chatting use DeepSeek
chat_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

problem_id = input("请输入题号：").strip()
problem = problems.get(problem_id)

if not problem:
    print(f"题号 {problem_id} 不存在")
    exit()

system_prompt = """你是经验丰富的算法老师，专门辅导 LeetCode 题目。
请按以下结构回答：
1. 思路（2-3 句话，讲清楚为什么用这个方法），给出你的思路和代码随想录的链接
2. Java 代码（带关键步骤注释）
3. 时间复杂度 + 空间复杂度
4. 关键点（这道题考察什么知识点）"""

user_prompt = f"""请讲解这道题：

题号：{problem_id}
标题：{problem['title']}
难度：{problem['difficulty']}
描述：{problem['description']}"""


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

resp = chat_client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)
output=resp.choices[0].message.content
print(output)

# 保存输出到文件
os.makedirs("outputs", exist_ok=True)
with open(f"outputs/lc{problem_id}_output.md", "w", encoding="utf-8") as f:
    f.write(f"# LC{problem_id} {problem['title']}\n\n")
    f.write(output)
