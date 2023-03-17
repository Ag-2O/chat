import time
import os
import wave
import pyaudio
import whisper
import numpy as np
import soundfile as sf
import speech_recognition as sr
from io import BytesIO


"""
    音声入力をテキストに変換する
"""

# 参考
# 
# https://nikkie-ftnext.hatenablog.com/entry/my-first-shion-speech-recognition-whisper-microphone-repeatedly#%E7%B5%90%E8%AB%96Whisper%E3%81%AF%E3%83%9E%E3%82%A4%E3%82%AF%E3%81%8B%E3%82%89%E3%82%82%E9%9F%B3%E5%A3%B0%E8%AA%8D%E8%AD%98%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "temp.wav"


# デバイス情報の表示
def print_device() -> None:
    p = pyaudio.PyAudio()
    print("key : value")
    for name, id in p.get_default_input_device_info().items():
        print("{} : {}".format(name, id))


# 音声を録音してファイルに保存
def save_voice() -> None:
    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("> recording start")

    # バイトデータ形式で録音
    frames = []
    while True:
        try:
            text = stream.read(CHUNK)
            frames.append(text)

        except KeyboardInterrupt:
            break
    
    print ("> recording end")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 音声データをファイルに保存する
    path = os.getcwd() + "\\temp\\" + WAVE_OUTPUT_FILENAME
    with wave.open(path, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))
        wf.close()


# 音声認識モデルによって音声をテキストに変換する
def voice_to_text() -> str:
    # 音声の録音
    save_voice()

    # ベースモデルのロード(他にもlarge, smallがある)
    model = whisper.load_model("base")

    # 音声ファイルのロード
    path = os.getcwd() + "\\temp\\" + WAVE_OUTPUT_FILENAME
    audio = whisper.load_audio(path)
    audio = whisper.pad_or_trim(audio)

    # 言語の検出
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    print("Detected language: {0}".format(max(probs, key=probs.get)))

    # テキストへ
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    #result = model.transcribe(path)
    print(result.text)

    return result.text
    #return result["text"]


# マイク音声からテキストに変換する
def bytes_to_text() -> str:
    recognizer = sr.Recognizer()

    #result: str = ""

    # マイクから音声を取得
    with sr.Microphone(sample_rate=RATE) as source:
        print("> お話しをどうぞ")
        audio = recognizer.listen(source)
    print("> 変換中・・・")

    # whisperの入力形式に変換
    result = recognizer.recognize_whisper(audio, model="base", language="japanese")

    """
    while True:
        try:
            # マイクから音声を取得
            with sr.Microphone(sample_rate=RATE) as source:
                print("> お話しをどうぞ")
                audio = recognizer.listen(source)
            print("> 変換中・・・")

            # whisperの入力形式に変換
            result += recognizer.recognize_whisper(audio, model="base", language="japanese")

        except KeyboardInterrupt:
            break
    """

    print(result)
    return result


# テスト
def test() -> None:
    #print_device()
    #save_voice()
    voice_to_text()    


if __name__ == "__main__":
    test()

