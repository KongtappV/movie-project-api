FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev

RUN pip3 install --no-cache-dir -r requirements.txt

RUN apk del build-deps

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["app.py"]
