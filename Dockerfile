FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import whisper;whisper.load_model('large')"
COPY *.py .
CMD [ "python", "./index.py" ]
