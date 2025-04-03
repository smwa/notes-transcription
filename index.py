from pathlib import Path
from os import environ
from time import sleep

import whisper

search_path = Path(environ.get('SEARCH_PATH', '/files'))
wait_time = int(environ.get('INTERVAL', '1800'))
file_extensions = environ.get('FILE_EXTENSIONS', 'mp3')

file_extensions = [".{}".format(f) for f in file_extensions.split(',')]
model = whisper.load_model('large')

def transcribe(audio_file_path, target_file_path):
    result = model.transcribe(audio_file_path)

    with open(target_file_path, 'w') as f:
        f.write(result["text"])

while True:
    for extension in file_extensions:
        files = search_path.glob('**/*{}'.format(extension))
        for file in files:
            if not file.is_file():
                print("not file")
                continue
            file.resolve()
            source_file_path = str(file)
            target_file_path = source_file_path + '.txt'
            if Path(target_file_path).exists():
                continue
            print("Transcribing {}".format(source_file_path))
            transcribe(source_file_path, target_file_path)

    sleep(wait_time)
