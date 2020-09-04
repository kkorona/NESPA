from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from django.core.files.storage import FileSystemStorage
# Create your views here.

from . import validation
from .models import SubmissionModel
from accounts.models import vespaUser
import shutil
import os

LANGDICT = {
'01':'cpp',
'02':'c',
'03':'py',
'04':'java'
}

def submission(request):
    if request.method == "GET":
        return render(request, 'submission.html')
        
    if request.method == "POST":
        if 'source_code' in request.FILES:
            prob_ID = request.POST.get('problem_id')
            language = request.POST.get('language')
            source_code = request.FILES['source_code']
            fs = FileSystemStorage()
            filename = fs.save(source_code.name,source_code)
            uploaded_file_url = fs.url(filename)
            
            request.session['problem_id'] = prob_ID
            request.session['language'] = language
            request.session['langext'] = LANGDICT[language]
            request.session['uploaded_file_url'] = uploaded_file_url
            
            submission = SubmissionModel(client = request.session['userid'], prob_ID = prob_ID, result = 'Failed')
            
            submission.save()
            request.session['submission_id'] = str(submission.id)
            
            return redirect('submission_check')
        else:
            return HttpResponse('소스코드가 첨부되지 않았습니다.')
        # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def submission_check(request):
    if not request.session['submission_id']:
        return HttpResponse('잘못된 접근입니다.')
    if request.method == "POST":    
        uploaded_file_url = request.session['uploaded_file_url']
        prob_ID = request.session['problem_id']
        client = vespaUser.objects.get(user_id = request.session['userid'])
        studentNumber = client.studentNumber
        departure_path = os.path.join(settings.BASE_DIR,uploaded_file_url[1:])
        destination_path = os.path.join(settings.BASE_DIR,'data','submission',studentNumber,prob_ID)
        target_name = request.session['submission_id']+'.'+request.session['langext']
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        shutil.move(departure_path,os.path.join(destination_path,target_name))
        return HttpResponse('Succesfully saved code')
        #https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
    return render(request, "submission_check.html")
    
def assignment_list(request):
    if request.method == "GET":
        return render(request, 'assignment_list.html')