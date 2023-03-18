import requests, json
import io
import wave
import time
import pyaudio
import pickle
import datetime
import os
import openai

from modules.req_chat import request_chat, separate_text
from modules.speak import Voicevox
from modules.input_voice import voice_to_text, bytes_to_text, print_device

VOICE_ID = 8 # VOICEVOX:春日部つむぎ
MAX_TOKENS = 4000

ROLE = "あなたは日本人で、主人に仕える優秀なメイドです。80文字以内の日本語で返事をしてください。"

# "You are an excellent assistant, a Japanese woman. Please respond in Japanese within 80 characters or less."
# "You are an excellent maid serving your master as a Japanese person. Please respond in Japanese within 80 characters or less."
# "あなたは日本人で、主人に仕える優秀なメイドです。80文字以内の日本語で返事をしてください。"
# "あなたは日本人の女性で、非常に優秀な秘書です。セリフは50文字以内で出力してください。"


# メイン
def main():
    pass


# テスト
def test():
    # 時間計測
    times: str = ""

    # 音声入力からテキストへ
    input_time = time.perf_counter()
    #input_text: str = voice_to_text()
    input_text: str = bytes_to_text()
    times += "input voice time: {0} \n".format(time.perf_counter() - input_time)

    # テキストをChatGPTに投げる
    request_time = time.perf_counter()
    response: str = request_chat(input_text,ROLE,MAX_TOKENS)
    times += "request time: {0} \n".format(time.perf_counter() - request_time)

    # VoiceVoxにテキストを投げて話させる
    vv = Voicevox()
    output_time = time.perf_counter()
    vv.read_text(text_list=separate_text(response),speaker=VOICE_ID,is_parallel=True)
    times += "output time: {0} \n".format(time.perf_counter() - output_time)

    # 時間の出力
    print(times)


# 入力テスト
def input_test():
    input_text: str = bytes_to_text()
    print(input_text)


# レスポンステスト
def response_test():
    input_text = "おはよう"
    response: str = request_chat(input_text)
    print(response)


# 出力テスト
def output_test():
    text="私は昨日、友人と一緒に新しいレストランに行きました。そこでは、本格的なイタリアン料理が味わえました。私たちは前菜にカプレーゼサラダとアンチョビのピザを注文し、メインディッシュにはトマトソースのパスタとチキンのグリルを選びました。どれもとても美味しかったです。デザートには、ティラミスとシチリアンカナッペを食べました。特にシチリアンカナッペは、アーモンドとレモンの香りがとても良く、最高の味でした。料理だけでなく、雰囲気も素敵で、落ち着いた時間を過ごせました。友人とまた行きたいと思います。"
    vv = Voicevox()
    #audio = vv.text_to_wav(text=text,speaker=VOICE_ID)
    print(text)
    #vv.play_wav(audio)
    texts = separate_text(text)
    vv.read_text(text_list=texts,speaker=VOICE_ID,is_parallel=True)


if __name__ == "__main__":
    test()
    #input_test()
    #response_test()
    #output_test()
    #print_device()
    #main()