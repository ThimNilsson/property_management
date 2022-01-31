# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
#RUN apt update && apt install -y python3-psycopg2
COPY . .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
