FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN uv venv
RUN uv pip install -r requirements.txt

COPY server.py .
COPY client.py .

EXPOSE 8050

CMD ["uv", "run", "server.py"]