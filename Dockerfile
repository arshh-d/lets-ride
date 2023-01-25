FROM python:3.9-alpine3.16

WORKDIR /home/rider

RUN apk update && apk upgrade


RUN apk add --no-cache --virtual .build-deps \
    ca-certificates linux-headers \
    zlib-dev curl git

COPY requirements.txt .
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/rider

WORKDIR /home/rider/rider/

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
