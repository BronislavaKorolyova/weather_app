FROM python:3.11-slim-buster

COPY requirements.txt .

RUN python -m venv /app/venv \
    && /app/venv/bin/pip install --upgrade pip \
    && /app/venv/bin/pip install -r requirements.txt

COPY . .

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

CMD ["/app/venv/bin/python", "main.py"]

