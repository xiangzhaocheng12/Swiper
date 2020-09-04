#!/bin/bash

# shellcheck disable=SC2034
BASE_DIR="/opt/swiper"

# shellcheck disable=SC2164
cd $BASE_DIR
source .venv/bin/activate
gunicorn -c swiper/gconfig.py swiper.wsgi
deactivate
# shellcheck disable=SC2164
cd -
