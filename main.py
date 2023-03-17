import requests, json
import io
import wave
import time
import pyaudio
import pickle
import datetime
import os
import openai

from modules.req_chat import request_chat
from modules.speak import Voicevox
from modules.input_voice import save_voice, voice_to_text, print_device

VOICE_ID = 8 
# 47

def main():

    times: str = ""

    # 音声入力からテキストへ
    input_time = time.perf_counter()
    save_voice()
    input_text: str = voice_to_text()
    times += "input voice time: {0} \n".format(time.perf_counter() - input_time)

    # テキストをChatGPTに投げる
    request_time = time.perf_counter()
    response: str = request_chat(input_text)
    times += "request time: {0} \n".format(time.perf_counter() - request_time)

    # VoiceVoxにテキストを投げて話させる
    vv = Voicevox()
    output_time = time.perf_counter()
    vv.speak(text=response,speaker=VOICE_ID)
    times += "output time: {0} \n".format(time.perf_counter() - output_time)

    # 時間の出力
    print(times)

if __name__ == "__main__":
    main()
    #print_device()