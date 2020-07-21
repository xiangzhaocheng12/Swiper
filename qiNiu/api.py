from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def token(request):
    data = {
        'token':'上传凭证',
        'key':'文件名',
    }
    return JsonResponse(data=data)