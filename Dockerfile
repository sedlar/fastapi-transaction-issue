FROM python:3.8-alpine3.13

WORKDIR /app

COPY *requirements.txt /app/

RUN apk add --no-cache --virtual=.run-deps curl pcre libpq libffi libxslt libxml2 && \
    apk add --no-cache --virtual=.build-deps build-base libffi-dev libxml2-dev libxslt-dev postgresql-dev linux-headers openssh-client make

RUN pip install -r requirements.txt

COPY . /app

CMD uvicorn app:app --reload
