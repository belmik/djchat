#!/bin/sh
chown -R app:app /home/app
echo "execute \"$@\""
exec su-exec app $@
