from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings

from django.core.files.storage import FileSystemStorage
# Create your views here.

from . import validation
from . import compile
# from . import execute
from .models import SubmissionModel
from accounts.models import vespaUser
import shutil
import os
import time

LANGDICT = {
'01':'C++14',
'02':'C11',
'03':'Python3',
'04':'JAVA'
}

EXTDICT = {
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
            departure_path = os.path.join(settings.BASE_DIR,uploaded_file_url[1:])            
            request.session['code_size'] = os.path.getsize(departure_path)
            
            request.session['problem_id'] = prob_ID
            request.session['language'] = LANGDICT[language]
            request.session['langext'] = EXTDICT[language]
            request.session['uploaded_file_url'] = uploaded_file_url
            now = time.localtime()
            request.session['updated_time'] = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
            
            return redirect('submission_check')
            
        else:
            return HttpResponse('소스코드가 첨부되지 않았습니다.')
        # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def submission_check(request):
    if request.method == "POST":    
        uploaded_file_url = request.session['uploaded_file_url']
        prob_ID = request.session['problem_id']
        client = vespaUser.objects.get(user_id = request.session['userid'])
        studentNumber = client.studentNumber
        ext = request.session['langext']
        
        departure_path = os.path.join(settings.BASE_DIR,uploaded_file_url[1:])
        destination_path = os.path.join(settings.BASE_DIR,'data','submission',studentNumber,prob_ID)
        
        submission = SubmissionModel(client_ID = request.session['userid'], client_number = studentNumber, prob_ID = prob_ID, score=0, exec_time=999.0, code_size=0, result = 'TBD')
        submission.save()
        request.session['submission_id'] = str(submission.id)
        submission_id = str(submission.id)
        
        target_name = submission_id + '.' + ext
        target_path = os.path.join(destination_path,target_name)
        target_title = os.path.join(destination_path, submission_id)      
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        shutil.move(departure_path,target_path)
        
        code_size = os.path.getsize(target_path)        
        
        submission.code_size = code_size
        
        compile_result = compile.compiles(target_title, ext)
        
        if compile_result[0] == 1:
            return render(request, "compile_error.html", {'error_msg' : compile_result[1]})
        
        return HttpResponse("compile finished.")
        
        # execute_result = execute.execute(target_path, prob_ID, ext)
        
        # return HttpResponse("execution finished.")
        
        
    return render(request, "submission_check.html")
    
def assignment_list(request):
    if request.method == "GET":
        return render(request, 'assignment_list.html')