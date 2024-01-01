FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /remanga_django

COPY requirements.txt .
COPY manage.py .
COPY remanga /remanga_django/remanga
COPY remanga_site /remanga_django/remanga_site
COPY docker .

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /remanga_django/entrypoint.sh

ENTRYPOINT ["/remanga_django/entrypoint.sh"]
