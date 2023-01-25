FROM python:3.9-alpine3.16

WORKDIR /home/rider

RUN apk update && apk upgrade


RUN apk add --no-cache --virtual .build-deps \
    ca-certificates g++ postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev curl jq libxml2-dev libxslt-dev git

COPY requirements.txt .
RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/integration-proxy

ARG CLIENT
ARG VERSION
RUN echo ${CLIENT}
RUN if [ ! -z "${CLIENT}" ] ; then find iproxy -type d -maxdepth 1 ! -name ${CLIENT} ! -name __* ! -name .mypy* ! -name iproxy -exec rm -rf {} + ; fi

WORKDIR /home/integration-proxy/iproxy

EXPOSE 8007

ENV REDIS_REMOTE_PORT=6379 \
    REDIS_REMOTE_HOST=host.docker.internal \
    POSTGRES_REMOTE_PORT=5432 \
    POSTGRES_REMOTE_HOST=host.docker.internal \
    RELEASE_VERSION=${VERSION}

ENV PYTHONUNBUFFERED=1

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8007"]
