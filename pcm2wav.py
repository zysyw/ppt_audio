import wave

def pcm2wav(pcm_file, wav_file, channels=1, bit_depth=16, sample_rate=16000):
    # 以二进制读取模式打开PCM文件
    with open(pcm_file, "rb") as pcmf:
        pcm_data = pcmf.read()

    # 使用wave模块创建一个新的WAV文件
    with wave.open(wav_file, "wb") as wavf:
        # 设置WAV文件的通道数、采样宽度（字节单位）和采样率
        wavf.setnchannels(channels)
        wavf.setsampwidth(bit_depth // 8)  # 位深转换为字节
        wavf.setframerate(sample_rate)
        # 写入PCM数据
        wavf.writeframes(pcm_data)
    
if __name__ == "__main__":
    pcm2wav("1.pcm", "1.wav")