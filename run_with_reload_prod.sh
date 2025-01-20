#!/bin/bash

uvicorn remanga_site.asgi:application --ssl-keyfile /etc/letsencrypt/live/meshchenko.ru/privkey.pem --ssl-certfile /etc/letsencrypt/live/meshchenko.ru/fullchain.pem

