from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

from . import validation

def submission(request):
    if request.method == "GET":
        return render(request, 'submission.html')
        
    if request.method == "POST":
        if not request.FILES['source_code']:
            return HttpResponse('소스코드가 첨부되지 않았습니다.')
            
        prob_ID = request.POST.get('problem_id')
        language = request.POST.get('language')
        source_code = request.FILES['source_code']
        
        
        
        # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
        
def assignment_list(request):
    if request.method == "GET":
        return render(request, 'assignment_list.html')