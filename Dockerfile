FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import whisper;whisper.load_model('large')"
RUN python -c "from df.enhance import init_df;init_df()"
RUN apt update
RUN apt install ffmpeg -y
COPY *.py .
CMD [ "python", "-u", "./index.py" ]
