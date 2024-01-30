import textwrap
from openai import AzureOpenAI

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.config_log as config_log
config, logger, CONFIG_PATH = config_log.setup_config_and_logging()
config.read(CONFIG_PATH)

def GPT_Template(prompt, output_way="json"):
    """GPT4 使用模板"""
    Azure_Open_AI_VERSION = 'Azure_Open_AI_GPT4_1106'
    client = AzureOpenAI(
        azure_endpoint = config.get(Azure_Open_AI_VERSION, 'azure_endpoint'),
        api_key = config.get(Azure_Open_AI_VERSION, 'api_key'),
        api_version = config.get(Azure_Open_AI_VERSION, 'api_version'),
        azure_deployment = config.get(Azure_Open_AI_VERSION, 'azure_deployment')
    )

    userPrompt = textwrap.dedent(f"""
        {prompt}
    """)

    response = client.chat.completions.create(
        model=config.get(Azure_Open_AI_VERSION, 'azure_deployment'),
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": f"使用繁體中文回答, 並使用 {output_way} 格式回傳"},
            {"role": "user", "content": userPrompt},
        ]
    )
    return(response.choices[0].message.content)

def GPT35_Template(prompt, output_way="json"):
    """GPT-35 使用模板"""
    Azure_Open_AI_VERSION = 'Azure_Open_AI_GPT4_1106'
    client = AzureOpenAI(
        azure_endpoint = config.get(Azure_Open_AI_VERSION, 'azure_endpoint'),
        api_key = config.get(Azure_Open_AI_VERSION, 'api_key'),
        api_version = config.get(Azure_Open_AI_VERSION, 'api_version'),
        azure_deployment = config.get(Azure_Open_AI_VERSION, 'azure_deployment')
    )

    userPrompt = textwrap.dedent(f"""
        {prompt}
    """)

    response = client.chat.completions.create(
        model=config.get(Azure_Open_AI_VERSION, 'azure_deployment'),
        messages=[
            {"role": "system", "content": f"使用繁體中文回答, 並使用 {output_way} 格式回傳"},
            {"role": "user", "content": userPrompt},
        ]
    )
    return(response.choices[0].message.content)

def main():
    """ 範例: GPT 模板使用 """
    # import utils.gpt_integration as gpt_call
    # gpt_call.GPT_Template()
    print(GPT_Template('問題: 太陽系有哪些行星？請用 json 格式回傳，{"回傳內容": "_回答_"}'))

if __name__ == "__main__":
    main()
