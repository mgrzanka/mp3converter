FROM python:3.11-slim-bullseye
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING="utf-8"

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests build-essential libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# App code + migrations
COPY src ./src
COPY migrations ./migrations
COPY entrypoint.sh ./entrypoint.sh
RUN chmod 755 ./entrypoint.sh

# Create app user
RUN useradd -m app && chown -R app:app /app
USER app

EXPOSE 5000
ENTRYPOINT ["./entrypoint.sh"]
