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
from collections import OrderedDict
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
        return render(request, 'submission.html', {'full_prob_list' : full_prob_list, 'cur_prob_list':cur_prob_list})
        
    if request.method == "POST":
        if 'source_code' in request.FILES:
            prob_ID = request.POST.get('problem_id')
            language = request.POST.get('language')
            source_code = request.FILES['source_code']
            user_id = request.session['userid']
            fs = FileSystemStorage()
            filename = fs.save(source_code.name,source_code)
            uploaded_file_url = fs.url(filename)      
            departure_path = os.path.join(settings.BASE_DIR,uploaded_file_url[1:])
            
            prob = ProblemModel.objects.get(prob_id = prob_ID)
            
            if request.session['usertype'] == 'normal':

                my_submissions = SubmissionModel.objects.filter(prob_ID = prob_ID, client_ID = user_id).count()
                if my_submissions >= prob.try_limit:
                    return HttpResponse('제출 횟수가 초과되었습니다. ')
                
                now = timezone.now()
                
                if prob.starts_at >= now or prob.ends_at <= now:
                    return HttpResponse('제출 기간이 아닙니다.')
                
                request.session['code_size'] = os.path.getsize(departure_path)
                if int(request.session['code_size']) > prob.size_limit:
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
        prob = ProblemModel.objects.get(prob_id = prob_ID)  

        client = vespaUser.objects.get(user_id = request.session['userid'])
        studentNumber = client.studentNumber
        ext = request.session['langext']
        
        departure_path = os.path.join(settings.BASE_DIR,uploaded_file_url[1:])
        destination_path = os.path.join(settings.BASE_DIR,'data','submission',studentNumber,prob_ID)
        
        submission = SubmissionModel(client_ID = request.session['userid'], client_number = studentNumber, prob_ID = prob_ID, score=0, exec_time=999.0, code_size=0, lang=ext, prob_name = prob.prob_name)
        submission.save()
        request.session['submission_id'] = str(submission.id)
        submission_id = str(submission.id)
        
        target_name = submission_id + '.' + ext
        target_path = os.path.join(destination_path,target_name)
        target_title = os.path.join(destination_path, submission_id) 
        eval_path = os.path.join(settings.BASE_DIR,'data','exam',prob_ID,'eval')
        
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        
        shutil.move(departure_path,target_path)
        
        code_size = os.path.getsize(target_path)        
        
        submission.code_size = code_size
        
        compile_result = compile.compiles(target_title, ext)
        
        if compile_result == 1:
            return render(request, "compile_error.html", {'error_msg' : '컴파일 에러가 발생하였습니다. 소스코드를 확인해주시고, 해결이 안될 경우 조교에게 문의하세요.'})
        
        execute_result = execute.executes(destination_path, eval_path, submission_id, ext, str(prob.time_limit))
        
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
        
def submission_list(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')        
    prob_list = ProblemModel.objects.all()
    return render(request, "submission_list.html", {'prob_list':prob_list})
    
def watch_code(request):
    if request.session['usertype'] != 'admin':
        return HttpResponse('허용되지 않은 기능입니다.')        
    prob_ID = request.GET.get('prob_id', None)
    student_number = request.GET.get('student_number', None)
    submission_ID = request.GET.get('submission_id', None)
    ext = request.GET.get('ext', None)
    if not prob_ID:
        return HttpResponse("Wrong prob_id")
    if not student_number:
        return HttpResponse("Wrong student_number")
    if not submission_ID:
        return HttpResponse("Wrong submission_id")
    if not ext:
        return HttpResponse("Wrong ext")
    code_path = os.path.join("/opt/vespa/data/exam_submission",student_number,prob_ID,submission_ID+'.'+ext)
    code_content = ""
    if os.path.isfile(code_path) :
        try:
            with open(code_path, 'r', encoding="utf-8") as f:
                code_content = f.read()
        except UnicodeDecodeError:
            with open(code_path, 'r', encoding="ISO-8859-1") as f:
                code_content = f.read()
    
    return render(request, "watch_code.html", {'code_content' : code_content, 'path':code_path})
    
def sub_to_show(sub, count):
    show = {}
    show['client_ID'] = sub.client_ID
    show['client_number'] = sub.client_number
    show['prob_ID'] = sub.prob_ID
    show['created_at'] = sub.created_at
    show['score'] = sub.score
    show['exec_time'] = sub.exec_time
    show['code_size'] = sub.code_size
    show['lang'] = sub.lang
    show['count'] = count
    show['id'] = sub.id
    return show

def submission_detail(request):
    if request.session['usertype'] != 'admin':
        return HttpResponse('허용되지 않은 기능입니다.')        
    if not "logged_in" in request.session:
        return HttpResponse("로그인이 필요한 기능입니다.")
    if request.method == "GET":
        submission_table = None
        prob_ID = request.GET.get('prob_id', None)
        if request.session['usertype'] == 'normal':
            prob = ProblemModel.objects.get(prob_id = prob_ID)
            submission_table = SubmissionModel.objects.filter(client_ID = request.session['userid'], prob_ID = prob_ID)
            return render(request, "submission_detail.html", {'submission_table' : submission_table, "prob":prob})
        elif request.session['usertype'] == 'admin':
            if prob_ID == 'full':
                submission_table = SubmissionModel.objects.all()
                return render(request, "submission_detail.html", {'submission_table' : submission_table})
            else:
                prob = ProblemModel.objects.get(prob_id = prob_ID)
                users = vespaUser.objects.filter(usertype="normal")
                submission_table = []
                scores = {}
                for user in users:
                    recent_submission = SubmissionModel.objects.filter(prob_ID = prob_ID, client_ID = user.user_id).order_by('-created_at')
                    sub_count = recent_submission.count()
                    if recent_submission:
                        recent_submission = recent_submission[0]
                    else:
                        recent_submission = SubmissionModel(client_ID = user.user_id, client_number = user.studentNumber, prob_ID = prob_ID, created_at = "-", score = 0, exec_time = 0.0, code_size = 0, lang = '-')
                    recent_submission.client_ID = user.username
                    submission_table.append(sub_to_show(recent_submission, sub_count))
                    if not recent_submission.score in scores:
                        scores[recent_submission.score] = 0
                    scores[recent_submission.score] += 1
                scores = OrderedDict(sorted(scores.items()))
                key_list = []
                score_list = []
                for key,score in scores.items():
                    key_list.append(key)
                    score_list.append(score)
                return render(request, "submission_detail.html", {'submission_table' : submission_table, 'key_list':key_list, 'score_list':score_list, "prob":prob})
