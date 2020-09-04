#!/usr/bin/env bash
BASE_DIR="opt/swiper"
# ``表示将命令的结果赋值到新的变量里面去
# shellcheck disable=SC2034
GUNICORN_PID=`cat $BASE_DIR/logs/gunicorn.pid`
