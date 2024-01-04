FROM python:3.11

WORKDIR /

COPY "requirements.txt" "requirements.txt"

RUN ["pip3", "install", "-r","requirements.txt"]

RUN ["pip3", "install", "gunicorn", "boto3"]

WORKDIR /space-odyssey

COPY . .

CMD gunicorn --bind 0.0.0.0:80 --workers 20 wsgi:app

EXPOSE 80