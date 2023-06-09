import pickle
import datetime
import os
import re
import openai

"""
    APIを使ってChatGPTと対話する
"""

# 参考
# https://snuow.com/blog/ChatGPT%E3%81%AEAPI%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E4%BD%BF%E3%81%A3%E3%81%A6%E3%81%BF%E3%81%9F%E3%80%82/
# https://nikkie-ftnext.hatenablog.com/entry/my-first-shion-python-speech-recognition-part3
# https://github.com/Uberi/speech_recognition


# 環境設定
#openai.organization = "org-w9OLF18WAxKDo46FLWIOjoV"    # organization id
openai.api_key = os.environ["OpenAI API Key"]           # APIKey

# 会話の保存
def save_chat(messages,response):
    file_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    path = os.getcwd() + "\\outputs\\" + file_name + ".pickle"
    messages.append(response)

    with open(path, "wb") as f:
        pickle.dump(messages,f)


# ChatGPTに投げる
def request_chat(input_to_chatgpt:str, role:str, max_tokens:int=100) -> str:

    # 実際のメッセージとロール
    messages = [
            {"role": "system", "content": role},
            {"role": "user", "content": input_to_chatgpt}
        ]

    # OpenAIに投げるパケット
    res = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100
    )

    #print(input_to_chatgpt)                                # 入力文の表示
    print(res['choices'][0]['message']['content'])          # 出力されたメッセージの表示
    save_chat(messages=messages,response={'response':res})  # やりとりの保存
    print(res)

    text = res['choices'][0]['message']['content']

    return text


# テキストを句読点で分割
def separate_text(text: str):
    pattern = re.compile(r"(?<=、)|(?<=。)|(?<=！)|(?<=？)")
    sentences = re.split(pattern,text)
    if (1 < len(sentences)): 
        if (sentences[-1] == ""): sentences = sentences[:-1]
    #print(sentences)
    return sentences


# テスト
def test():
    user_input = input('ChatGPTに聞きたいことを入力:')
    request_chat(input_to_chatgpt=user_input)


if __name__ == "__main__":
    test()
