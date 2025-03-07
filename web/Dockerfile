FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /app
COPY flag.txt /flag.txt

EXPOSE 5000

CMD ["waitress-serve", "--port=5000", "app:app"]
