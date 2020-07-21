import json

from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
def sub_phnum(request):
    phonenum = request.GET.get('phonenum')
    print('-----')
    print(phonenum)
    data = {
        'code': 200,
        'data': None,
    }

    return JsonResponse(data)
