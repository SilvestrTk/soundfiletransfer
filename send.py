import ggwave
import pyaudio
import os
import sys

def prepareFile(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return
    filename = os.path.basename(file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    result = f"<<FILENAME_START>>{filename}<<FILENAME_END>>\n{content}"
    print(result)
    return result


def sendAudio(content):
    p = pyaudio.PyAudio()

    # generate audio waveform for string "hello python"
    waveform = ggwave.encode(content, protocolId = 1, volume = 100)

    print("Transmitting text content")
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, output=True, frames_per_buffer=4096)
    stream.write(waveform, len(waveform)//4)
    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 send.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    sendAudio(prepareFile(file_path))