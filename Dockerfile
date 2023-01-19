FROM python:3.9-slim

COPY ./app /app

COPY ./entrypoint.sh /app/entrypoint.sh

COPY ./requirements.txt /app/requirements.txt

# just for linux
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install pip install -r /requirements.txt \
    && apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]