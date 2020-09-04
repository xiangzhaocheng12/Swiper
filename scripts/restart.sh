#!/usr/bin/env bash
echo '正在重启服务器'
sleep 3
echo '重启完毕'


# 11295 master

# 旧的进程
#15259 worker <- 2736
#15260 worker <- 3725
#15261 worker <- 7362
#15262 worker <- 7251

# 当master 收到 kill -HUP 的信号后, 先产生子进程, 然后等旧的子进程处理完毕后,再将其关闭
#18412 new worker <- 12
#18413 new worker <- 21
#18414 new worker <- 42
#18415 new worker <- 12

