FROM alpine:3.22.1

WORKDIR /app

COPY . .

RUN apk update && apk upgrade && \
    apk add --no-cache python3 py3-pip && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /opt/venv/bin/python -m spacy download en_core_web_sm

ENV PATH="/opt/venv/bin:$PATH"

CMD ["python3"]

