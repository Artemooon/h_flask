FROM python:3.8

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

COPY . /usr/src/app

RUN pip install -r requirements.txt

EXPOSE 5000

ENV TZ Europe/Kiev

CMD ["python3","main.py"]