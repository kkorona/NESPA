from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
# Create your views here.

from . import validation
from . import compile
from . import execute
from .models import SubmissionModel, ProblemModel
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
        full_prob_list = ProblemModel.objects.all()
        now = timezone.now()
        cur_prob_list = []
        for prob in full_prob_list:
            if prob.starts_at <= now and prob.ends_at >= now:
                cur_prob_list.append(prob)
            with open("test.txt","a") as f:
                f.write(str(prob.starts_at)+"\n")
                f.write(str(prob.ends_at)+"\n")
                f.write(str(now)+"\n\n")
        return render(request, 'submission.html', {'full_prob_list' : full_prob_list, 'cur_prob_list':cur_prob_list})
        
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
            if int(request.session['code_size']) > 3000:
                os.remove(departure_path)
                return HttpResponse('코드 크기가 초과되었습니다.')
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
        
        submission = SubmissionModel(client_ID = request.session['userid'], client_number = studentNumber, prob_ID = prob_ID, score=0, exec_time=999.0, code_size=0)
        submission.save()
        request.session['submission_id'] = str(submission.id)
        submission_id = str(submission.id)
        
        target_name = submission_id + '.' + ext
        target_path = os.path.join(destination_path,target_name)
        target_title = os.path.join(destination_path, submission_id) 
        eval_path = os.path.join(settings.BASE_DIR,'data','assignment',prob_ID,'eval')
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        shutil.move(departure_path,target_path)
        
        code_size = os.path.getsize(target_path)        
        
        submission.code_size = code_size
        
        compile_result = compile.compiles(target_title, ext)
        
        if compile_result == 1:
            return render(request, "compile_error.html", {'error_msg' : '컴파일 에러가 발생하였습니다. 소스코드를 확인해주시고, 해결이 안될 경우 조교에게 문의하세요.'})
        
        execute_result = execute.executes(destination_path, eval_path, submission_id, ext)
        
        total_tc = len(execute_result)
        scored_tc = 0
        total_time = 0.0
        res_out = []
        
        filename_list = []
        caseRes_list = []
        exectime_list = []
        
        for tc in execute_result:
            if tc['caseRes'] == "CORRECT ANSWER":
                scored_tc += 1
            total_time += float(tc['exectime'])
            filename_list.append(tc['filename'])
            caseRes_list.append(tc['caseRes'])
            exectime_list.append(tc['exectime'])
        
        score = 100 * scored_tc // total_tc
        
        res_out = zip(filename_list, caseRes_list, exectime_list)
        
        submission.exec_time = total_time
        submission.score = score
        
        submission.save()
            
        return render(request, "result.html", {'prob_id' : prob_ID, 'result_out_table' : res_out, 'score' : str(score), 'total_time' : str(total_time)})
        
        
    return render(request, "submission_check.html")
    
def assignment_list(request):
    if request.method == "GET":
        return render(request, 'assignment_list.html')
        
def submission_list(request):
    return render(request, "submission_list.html")
    
def submission_detail(request):
    if request.method == "GET":
        submission_table = None
        prob_ID = request.GET.get('prob_id', None)
        if request.session['usertype'] == 'normal':
            submission_table = SubmissionModel.objects.filter(client_ID = request.session['userid'], prob_ID = prob_ID)
        elif request.session['usertype'] == 'admin':
            if prob_ID == 'full':
                submission_table = SubmissionModel.objects.all()
            else:
                full_submission_table = SubmissionModel.objects.filter(prob_ID = prob_ID).order_by('-score','exec_time','code_size','client_number','-created_at')
                submission_table = []
                last = None
                for submission in full_submission_table:
                    if len(submission_table) > 0:
                        if last.client_number == submission.client_number:
                            continue
                    
                    submission_table.append(submission)
                    last = submission
        return render(request, "submission_detail.html", {'submission_table' : submission_table})