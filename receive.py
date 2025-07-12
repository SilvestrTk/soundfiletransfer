import ggwave
import pyaudio
import re
import time
import os



def decode_and_save(content_string, output_dir="."):
    pattern = r"<<FILENAME_START>>(.*?)<<FILENAME_END>>\n(.*)"
    match = re.match(pattern, content_string, re.DOTALL)

    if not match:
        raise ValueError("Invalid format: Could not find embedded filename.")

    filename = match.group(1)
    content = match.group(2)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_filename = f"received_{timestamp}_{filename}"
    output_path = os.path.join(output_dir, safe_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Saved to: {output_path}")
    return output_path

def receiveAudio():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=48000, input=True, frames_per_buffer=1024)

    print('Listening ... Press Ctrl+C to stop')
    instance = ggwave.init()

    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            res = ggwave.decode(instance, data)
            if (not res is None):
                try:
                    print('Received text: ' + res.decode("utf-8"))
                    decode_and_save(res.decode("utf-8"))
                except:
                    pass
    except KeyboardInterrupt:
        pass

    ggwave.free(instance)

    stream.stop_stream()
    stream.close()

    p.terminate()

if __name__ == "__main__":
    receiveAudio()