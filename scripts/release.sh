#!/bin/bash

LOCAL_DIR="./"
# shellcheck disable=SC2034
REMOTE_DIR="/opt/swiper/"
USER="ubuntu"
# shellcheck disable=SC2034
HOST="121.36.230.33"

# 获取指定代码版本
if [[ "$#" == "1" ]]; then
  echo '请输入正确的参数'
  exit 1 # 这里的 1 表示退出程序的时候的状态码
fi

# 检查版本切换是否成功
if git checkout $1; then
  rsync -crvP --exclude={.git,.venv,.vscode,logs,__pycache__} $LOCAL_DIR USER@HOST:REMOTE_DIR

  # 重启远程服务器
    # 提示是否需要重启服务器, read 是一个命令, user_input 是一个变量名
  read -p '您是否需要重启服务器 (y/n)' user_input
  if [[ "user_input" == "y" ]]; then
    ssh $USER@HOST 'bash /opt/swiper/scripts/restart.sh'
  fi


  # 切回之前操作的分支
  git checkout -
fi

# 还需要给sh文件添加可执行权限: chmod 755 *.sh
