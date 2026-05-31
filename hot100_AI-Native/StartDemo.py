import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()


# Chatting use DeepSeek
chat_client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages=[
    {"role": "system", "content": "你现在是一个算法老师"},
     {"role": "user", "content": "leetcode的hot100的两数之和：给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。你可以按任意顺序返回答案。"}
]

resp = chat_client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
print(resp.choices[0].message.content)