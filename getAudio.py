import os
import wave
import nls
from getToken import get_token
from pydub import AudioSegment

URL="wss://nls-gateway-cn-shanghai.aliyuncs.com/ws/v1"
TOKEN, _ = get_token()  #参考https://help.aliyun.com/document_detail/450255.html获取token
APPKEY = os.environ['ALIYUN_AK_APPKEY']       #获取Appkey请前往控制台：https://nls-portal.console.aliyun.com/applist

class SingleSentenceTTS:
    def __init__(self, tid):
        self.__id = tid
   
    def start(self, text, pcm_file):
        self.__text = text
        self.__pcm_file = pcm_file
        self.__f = open(self.__pcm_file, "wb")
        self.__test_run()
    
    def _on_metainfo(self, message, *args):
        print("on_metainfo message=>{}".format(message))  

    def _on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def _on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
            self.pcm2wav()
            self.pcm2mp3()
        except Exception as e:
            print("close file failed since:", e)

    def _on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def _on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))


    def __test_run(self):
        print("thread:{} start..".format(self.__id))
        tts = nls.NlsSpeechSynthesizer(url=URL,
                                       token=TOKEN,
                                       appkey=APPKEY,
                                       on_metainfo=self._on_metainfo,
                                       on_data=self._on_data,
                                       on_completed=self._on_completed,
                                       on_error=self._on_error,
                                       on_close=self._on_close,
                                       callback_args=[self.__id])
        print("{}: session start".format(self.__id))
        r = tts.start(self.__text, voice="zhida")
        print("{}: tts done with result:{}".format(self.__id, r))
        
    def pcm2wav(self, channels=1, bit_depth=16, sample_rate=16000):
        # 以二进制读取模式打开PCM文件
        with open(self.__pcm_file, "rb") as pcmf:
            pcm_data = pcmf.read()
        base_name = self.__pcm_file.rpartition('.')[0]
        wav_file = base_name + ".wav"
        # 使用wave模块创建一个新的WAV文件
        with wave.open(wav_file, "wb") as wavf:
            # 设置WAV文件的通道数、采样宽度（字节单位）和采样率
            wavf.setnchannels(channels)
            wavf.setsampwidth(bit_depth // 8)  # 位深转换为字节
            wavf.setframerate(sample_rate)
            # 写入PCM数据
            wavf.writeframes(pcm_data)
            
    def pcm2mp3(self, channels=1, bit_depth=16, sample_rate=16000):
        # 以二进制读取模式打开PCM文件
        with open(self.__pcm_file, "rb") as pcmf:
            pcm_data = pcmf.read()
        base_name = self.__pcm_file.rpartition('.')[0]
        mp3_file = base_name + ".mp3"
        audio = AudioSegment.from_raw(self.__pcm_file, sample_width=bit_depth//8, frame_rate=sample_rate, channels=channels)
        audio.export(mp3_file, format="mp3", parameters=["-codec:a", "libmp3lame", "-qscale:a", "2"])