FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /remanga

COPY requirements.txt /remanga
COPY remanga_site /remanga

# replacing database host to serivce name

RUN sed -i 's/"HOST": .*/"HOST": "db",/' ./remanga_site/settings.py

RUN pip install -r requirements.txt

