broker_url = 'redis://127.0.0.1:6379/1'
broker_pool_limit = 10 # Borker 连接池, 默认是10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']

task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/1'
result_serializer = 'pickle'    # 接口的序列化器
result_expires = 3600 # 任务结果过期时间
result_cache_max = 10000 # 任务结果最⼤缓存数量

worker_redirect_stdouts_level = 'INFO'
