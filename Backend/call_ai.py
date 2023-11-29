from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

openai_api_key_for_openai = "YOUR_OPENAI_API_KEY"
deployment_name_for_openai = "gpt-4-1106-preview"

def do_openai(messages):
    openAI = ChatOpenAI(
        model_name=deployment_name_for_openai,
        openai_api_key=openai_api_key_for_openai,
        temperature=0,
        max_tokens=4096
    )
    try:
        res = openAI(messages)
        return res.content
    except Exception as e:
        print(f"哭哭，出現錯誤，錯誤內容: {e}")
        return do_openai(messages)

def call_aied(wait, quest):

    prompt = f"""
請從下列三個選項中選擇出最適合回答 "我的問題" 的答案

"我的問題": {quest}

"選項一": {wait[0]}
"選項二": {wait[1]}
"選項三": {wait[2]}

輸出: 請將選中的那個選項內的完整文字輸出出來
"""
    try:
        res = do_openai([HumanMessage(content=prompt)])
    except:
        res = "GPT 當掉囉! 請重新發問 >_<"

    return res
