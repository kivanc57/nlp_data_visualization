FROM alpine:3.22.1

WORKDIR /app

COPY . .

# Install Python, pip, bash
RUN apk update && apk upgrade && \
    apk add --no-cache python3 py3-pip && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /opt/venv/bin/python -m spacy download en_core_web_sm

# Add venv to PATH
ENV PATH="/opt/venv/bin:$PATH"

# Default command
CMD ["python3"]

