import json
import nls
from getAudio import SingleSentenceTTS

def main():
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    input_text_file = config["text_file_path"] + config["text_file_name"] # 输入文本文件的路径
    print(input_text_file)
    output_pcm_file_path = config["pcm_file_path"]
    line_count = 0

    with open(input_text_file, "r", encoding='utf-16') as file:
        for line in file:
            line = line.strip()  # 移除行尾的换行符
            if line:  # 检查行是否为空
                line_count += 1
                tts = SingleSentenceTTS(line_count)
                pcm_file_name = f"{output_pcm_file_path}{line_count}.pcm"
                print(pcm_file_name)
                tts.start(line, pcm_file_name)
                #print(f"Progress: {line_count} PCM files generated.")

if __name__ == "__main__":
    nls.enableTrace(False)
    main()

    