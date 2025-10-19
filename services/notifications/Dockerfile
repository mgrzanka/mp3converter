FROM python:3.11-slim-bullseye
WORKDIR /app

RUN apt-get update \
    && apt-get -y --no-install-recommends --no-install-suggests install build-essential libpq-dev netcat \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY entrypoint.sh ./
RUN chmod 755 ./entrypoint.sh

RUN useradd -m app \
    && chown -R app:app /app
USER app

ENTRYPOINT [ "./entrypoint.sh" ]
