FROM python:3.11-slim-bullseye
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING="utf-8"

RUN apt-get update \
    && apt-get install -y --no-install-suggests --no-install-recommends build-essential libpq-dev netcat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

RUN useradd -m app \
    && chown -R app:app /app
USER app

EXPOSE 8080
ENTRYPOINT ["./entrypoint.sh"]
