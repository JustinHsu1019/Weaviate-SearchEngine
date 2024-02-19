import json
from utils.gpt_integration import GPT_Template

# openai_api_key_for_openai = "YOUR_OPENAI_API_KEY"
# deployment_name_for_openai = "gpt-4-1106-preview"

def call_aied(wait, quest):
    prompt = f"""
請從下列三個選項中選擇出最適合回答 "我的問題" 的答案

"我的問題": {quest}

"選項一": {wait[0]}
"選項二": {wait[1]}
"選項三": {wait[2]}

輸出: 請將選中的那個選項內的完整文字輸出出來

json 格式:
{{
    "輸出": ""
}}
"""
    try:
        res = GPT_Template(prompt)
        res = json.loads(res)["輸出"]
    except:
        res = "GPT 當掉囉! 請重新發問 >_<"

    return res

if __name__ == "__main__":
    quest = "你喜歡吃什麼?"
    wait = ["我喜歡吃蛋餅", "我喜歡打藍球", "我是個人類"]

    print(call_aied(wait, quest))
