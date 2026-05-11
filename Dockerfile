FROM python:3.12
WORKDIR /usr/src/app
RUN apt update && apt install -y rustc cargo ffmpeg libsndfile1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import whisper;whisper.load_model('turbo')"
RUN python -c "from df.enhance import init_df;init_df()"
COPY *.py .
CMD [ "python", "-u", "./index.py" ]
