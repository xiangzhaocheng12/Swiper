import time
from celery import Celery

# 连接redis的地址
broker = 'redis://127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('worker', broker=broker, backend=backend)


@app.task
def foo():
    print('start')
    time.sleep(10)
    print('end')
    return 123


@app.task
def func1():
    print('func1:start')
    time.sleep(20)
    print('func1:stop')

# celery worker -A task_test --loglevel=INFO  启动celery 的命令
