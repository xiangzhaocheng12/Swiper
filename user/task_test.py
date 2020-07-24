import time
from celery import Celery

broker = 'redis//127.0.0.1:6379/0'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('worker',broker,backend=backend)

@app.task
def foo():
    print('start')
    time.sleep(10)
    print('end')
    return 123


# celery worker -A task_test --loglevel=INFO  启动celery 的命令
# 