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

VOICE_ID = 8 
# 47

# テスト
def test():

    times: str = ""

    # 音声入力からテキストへ
    input_time = time.perf_counter()
    #input_text: str = voice_to_text()
    input_text: str = bytes_to_text()
    times += "input voice time: {0} \n".format(time.perf_counter() - input_time)

    # テキストをChatGPTに投げる
    request_time = time.perf_counter()
    response: str = request_chat(input_text)
    times += "request time: {0} \n".format(time.perf_counter() - request_time)

    # VoiceVoxにテキストを投げて話させる
    vv = Voicevox()
    output_time = time.perf_counter()
    vv.read_text(text_list=separate_text(response),speaker=VOICE_ID,is_parallel=False)
    times += "output time: {0} \n".format(time.perf_counter() - output_time)

    # 時間の出力
    print(times)


# 反復して実行
def output_test():
    text="最近、私は新しい趣味を見つけました。それはガーデニングです。私は自宅の庭に新しい花を植えることがとても楽しいです。特に、色とりどりのチューリップやバラが大好きです。最初は、どのように植えるかわからず、いくつかの失敗もありましたが、少しずつ学びながら進めています。これまでの成果を見ると、本当にやりがいを感じます。また、庭に出ることで日常のストレスも解消されるので、とてもリフレッシュできます。今後も、さらにたくさんの花を植えて、素敵な庭を作っていきたいと思っています。"
    vv = Voicevox()
    audio = vv.text_to_wav(text=text,speaker=VOICE_ID)
    print(text)
    vv.play_wav(audio)
    #texts = separate_text(text)
    #vv.read_text(text_list=texts,speaker=VOICE_ID,is_parallel=False)


if __name__ == "__main__":
    #test()
    output_test()
    #print_device()