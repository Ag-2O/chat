import requests, json
import io
import sys
import wave
import time
import pyaudio
import threading
import queue

"""
    VoiceVoxを使って音声出力を行う
"""

# 参考
# VoiceVox: https://voicevox.hiroshiba.jp/
# https://snuow.com/blog/%E3%80%90python%E3%80%91voicevox%E3%82%92python%E3%81%8B%E3%82%89%E4%BD%BF%E7%94%A8%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95/

class Voicevox:
    def __init__(self, host="127.0.0.1", port=50021):
        self.host = host
        self.port = port
        self.is_complete = False    # 完了フラグ


    # テキストの読み上げ
    def read_text(self, text_list: list, speaker=47, is_parallel: bool=True):
        try:
            if (1 < len(text_list) and is_parallel):
                q = queue.Queue()

                thread = threading.Thread(target=self.texts_to_wavs, args=(text_list,q,speaker))
                thread.start()

                while True:
                    if q.empty() and self.is_complete: break

                    if not q.empty():
                        self.play_wav(q.get())
                    else:
                        time.sleep(0.5)

            else:
                for text in text_list:
                    audio = self.text_to_wav(text,speaker)
                    self.play_wav(audio)
        
        except Exception as e:
            import traceback
            etype, value, tb = sys.exc_info()
            print(traceback.format_exception(etype, value, tb))
            audio = self.text_to_wav("予期せぬエラーが発生したため、もう一度お願いします。",speaker)
            self.play_wav(audio)


    # テキストリストを順次音声へ
    def texts_to_wavs(self, text_list:list, q, speaker=47):
        for text in text_list:
            q.put(self.text_to_wav(text,speaker))
        self.is_complete = True

    # テキストから音声へ
    def text_to_wav(self,text=None,speaker=47):
        params = (
            ("text", text),
            ("speaker", speaker)  # 音声の種類をInt型で指定
        )

        init_q = requests.post(
            f"http://{self.host}:{self.port}/audio_query",
            params=params
        )

        res = requests.post(
            f"http://{self.host}:{self.port}/synthesis",
            headers={"Content-Type": "application/json"},
            params=params,
            data=json.dumps(init_q.json())
        )

        return io.BytesIO(res.content)


    # 音声の再生
    def play_wav(self,audio):
        with wave.open(audio,'rb') as f:
            # 以下再生用処理
            p = pyaudio.PyAudio()

            def _callback(in_data, frame_count, time_info, status):
                data = f.readframes(frame_count)
                return (data, pyaudio.paContinue)

            stream = p.open(format=p.get_format_from_width(width=f.getsampwidth()),
                            channels=f.getnchannels(),
                            rate=f.getframerate(),
                            output=True,
                            stream_callback=_callback)

            # Voice再生
            stream.start_stream()
            while stream.is_active():
                time.sleep(0.1)

            stream.stop_stream()
            stream.close()
            p.terminate()

# テスト
def test():
    vv = Voicevox()
    vv.read_text(text="こんにちは")    


if __name__ == "__main__":
    test()
