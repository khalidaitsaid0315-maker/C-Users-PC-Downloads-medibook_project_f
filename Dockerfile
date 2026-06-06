FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8161

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY medibook_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY medibook_project/medibook /app/medibook
COPY medibook_project/docker-entrypoint.sh /app/

RUN sed -i 's/\r$//' /app/docker-entrypoint.sh && chmod +x /app/docker-entrypoint.sh

WORKDIR /app/medibook

EXPOSE 8161

ENTRYPOINT ["/app/docker-entrypoint.sh"]
