FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

COPY . /usr/src/app

RUN pip install -r requirements.txt


ENV TZ Europe/Kiev

ENV FLASK_ENV=development


#CMD ["gunicorn","app:app","-b","0.0.0.0:8000"]