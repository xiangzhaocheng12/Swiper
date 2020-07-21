from django.shortcuts import render

# 用作调试的时候使用
def home(request):
    # 加载 HTML
    return render(request,'index.html')

