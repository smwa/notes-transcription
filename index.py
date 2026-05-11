from pathlib import Path
from os import environ
from time import sleep
from tempfile import NamedTemporaryFile
import subprocess

import whisper

print("Starting v4")

search_path = Path(environ.get('SEARCH_PATH', '/files'))
wait_time = int(environ.get('INTERVAL', '1800'))
file_extensions = environ.get('FILE_EXTENSIONS', 'mp3')
target_file_extension = environ.get('TARGET_FILE_EXTENSION', 'md')
enable_denoise = True
denoised_suffix = environ.get('DENOISED_SUFFIX', 'denoised.wav')

file_extensions = [".{}".format(f) for f in file_extensions.split(',')]
model = whisper.load_model('large')

if enable_denoise:
    from df.enhance import enhance, init_df, load_audio, save_audio
    df_model, df_state, _ = init_df()

def denoise(audio_file_path, denoised_file_path):
    with NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        tmp_path = tmp.name
    try:
        subprocess.run(
            ['ffmpeg', '-i', audio_file_path, '-ar', str(df_state.sr()), '-ac', '1', '-y', tmp_path],
            check=True, capture_output=True
        )
        audio, _ = load_audio(tmp_path, sr=df_state.sr())
        enhanced = enhance(df_model, df_state, audio)
        save_audio(denoised_file_path, enhanced, df_state.sr())
    finally:
        Path(tmp_path).unlink(missing_ok=True)

def transcribe(audio_file_path, target_file_path):
    result = model.transcribe(audio_file_path, language="en")

    with open(target_file_path, 'w') as f:
        for segment in result["segments"]:
            f.write(segment["text"])
            f.write("\n")

while True:
    for extension in file_extensions:
        files = search_path.glob('**/*{}'.format(extension))
        for file in files:
            if not file.is_file():
                print("not file")
                continue
            file.resolve()
            source_file_path = str(file)
            if denoised_suffix in file.name:
                continue

            if enable_denoise:
                denoised_file_path = '{}.{}'.format(source_file_path, denoised_suffix)
                if not Path(denoised_file_path).exists():
                    print("Denoising {}".format(source_file_path))
                    denoise(source_file_path, denoised_file_path)

            target_file_path = '{}.{}'.format(source_file_path, target_file_extension)
            if Path(target_file_path).exists():
                continue
            print("Transcribing {}".format(source_file_path))
            transcribe(source_file_path, target_file_path)

    sleep(wait_time)
