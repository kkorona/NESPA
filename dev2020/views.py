from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'dev2020/index.html')
    
def nespa_dev(request):
    return render(request, 'dev2020/nespa_dev.html')

def page_not_found(request, exception):
    return render(request, 'dev2020/404.html', {})