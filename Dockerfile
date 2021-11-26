FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY init.sh /init.sh

RUN set -ex \
    && chmod +x /init.sh \
    && apk add su-exec libpq \
    && apk add --virtual .temp-dependencies \
    gcc g++ libffi-dev make musl-dev postgresql-dev python3-dev openssl-dev cargo rustup\
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .temp-dependencies \
    && rm -rf /root/.cargo \
    && adduser -s /bin/sh -D -u 1111 app

WORKDIR /home/app

COPY --chown=app:app djchat/djchat djchat
COPY --chown=app:app djchat/chat chat
COPY --chown=app:app djchat/manage.py manage.py

ENTRYPOINT [ "/init.sh" ]
CMD [ "python" ]