from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from django.core.files import File as DjangoFile
# Create your views here.

from . import validation
from . import compile
from . import execute
from assignment.models import SubmissionModel, ProblemModel, GradeModel
from accounts.models import vespaUser
from collections import OrderedDict
import pandas as pd
import numpy as np
import shutil
import os
import time
import zipfile

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
            language = request.POST.get('language')
            source_code = request.FILES['source_code']

            user = vespaUser.objects.get(user_id=request.session['userid'])
            try:
                prob = ProblemModel.objects.get(prob_id = request.POST.get('problem_id'))
            except:
                return HttpResponse('문제가 선택되지 않았습니다.')            
            
            if request.session['usertype'] == 'normal':

                my_submissions = SubmissionModel.objects.filter(problem=prob, user=user).count()
                if my_submissions >= prob.try_limit:
                    return HttpResponse('제출 횟수가 초과되었습니다. ')
                
                now = timezone.now()
                
                if prob.starts_at >= now or prob.ends_at <= now:
                    return HttpResponse('제출 기간이 아닙니다.')

                if len(request.FILES['source_code'].read()) > prob.size_limit:
                    return HttpResponse('코드 크기가 초과되었습니다.')
            
            request.session['problem_id'] = prob.prob_id
            request.session['language'] = LANGDICT[language]

            now = time.localtime()
            request.session['updated_time'] = "%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

            submission = SubmissionModel(client_ID=user.user_id, client_number=user.studentNumber, prob_ID=prob.prob_id, score=0,exec_time=999.0, code_size=0, lang=EXTDICT[language], prob_name=prob.prob_name)
            submission.user = user
            submission.problem = prob
            submission.save()
            submission.sub_file = request.FILES['source_code']
            submission.code_size = submission.sub_file.size
            submission.save()

            request.session['code_size'] = submission.code_size
            request.session['submission_id'] = submission.id
            return render(request, "submission_check.html")
        else:
            return HttpResponse('소스 코드가 첨부되지 않았습니다.')
            
        # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html

def submission_check(request):
    if request.method == "POST":    

        submission = SubmissionModel.objects.get(id = int(request.session['submission_id']))

        prob = submission.problem
        prob_ID = prob.prob_id

        client = vespaUser.objects.get(user_id = request.session['userid'])
        studentNumber = client.studentNumber
        
        ext = submission.lang

        destination_path = os.path.join(settings.BASE_DIR, 'data', 'submission', studentNumber, prob_ID)
        subfile_path = os.path.join(settings.BASE_DIR, 'data', 'assignment', prob_ID, 'subs')
        header_path = os.path.join(settings.BASE_DIR, 'data', 'assignment', prob_ID, 'header')

        target_name = submission.filename()
        target_path = os.path.join(destination_path, target_name)
        target_title = os.path.join(destination_path, str(submission.id)) 
        eval_path = os.path.join(settings.BASE_DIR,'data','assignment',prob_ID,'eval')
        
        if os.path.exists(subfile_path):
            subfiles = os.listdir(subfile_path)
            for subfile in subfiles:
                shutil.copyfile(os.path.join(subfile_path,subfile),os.path.join(destination_path,subfile))
        
        code_size = submission.sub_file.size

        compile_result = compile.compiles(target_title, ext)
        
        if compile_result == 1:
            return render(request, "compile_error.html", {'error_msg' : '컴파일 에러가 발생하였습니다. 소스코드를 확인해주시고, 해결이 안될 경우 조교에게 문의하세요.'})
        
        execute_result = execute.executes(destination_path, eval_path, str(submission.id), ext, str(prob.time_limit))
        
        total_tc = len(execute_result)
        if total_tc <=0:
            total_tc = 1
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
    prob_list = ProblemModel.objects.all()
    return render(request, 'assignment_list.html', {'prob_list':prob_list})
        
def submission_list(request):
    prob_list = ProblemModel.objects.all()
    return render(request, "submission_list.html", {'prob_list':prob_list})

    
    
def watch_code(request):
    submission_ID = request.GET.get('submission_id', None)
    if submission_ID == "None": submission_ID = -1
    submission = get_object_or_404(SubmissionModel, id=submission_ID)
    code_path = submission.sub_file.path
    if os.path.isfile(code_path) :
        try:
            with open(code_path, 'r', encoding="utf-8") as f:
                code_content = f.read()
        except UnicodeDecodeError:
            with open(code_path, 'r', encoding="ISO-8859-1") as f:
                code_content = f.read()
    return render(request, "watch_code.html", {'code_content' : code_content, 'lang': submission.lang, 'path':code_path})
    
def sub_to_show(sub, name, count):
    show = {}
    show['client_ID'] = sub.client_ID
    show['username'] = name
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
    if not "logged_in" in request.session:
        return HttpResponse("로그인이 필요한 기능입니다.")
    if request.method == "GET":
        submission_table = None
        prob_ID = request.GET.get('prob_id', None)
        if request.session['usertype'] == 'normal':
            prob = ProblemModel.objects.get(prob_id = prob_ID)
            submission_table = SubmissionModel.objects.filter(client_ID = request.session['userid'], prob_ID = prob_ID)

            users = vespaUser.objects.filter(usertype="normal")
            scores = {}
            for user in users:
                recent_submission = SubmissionModel.objects.filter(prob_ID = prob_ID, client_ID = user.user_id).order_by('-created_at')
                sub_count = recent_submission.count()
                if recent_submission:
                    recent_submission = recent_submission[0]
                else:
                    recent_submission = SubmissionModel(client_ID = user.user_id, client_number = user.studentNumber, prob_ID = prob_ID, created_at = "-", score = 0, exec_time = 0.0, code_size = 0, lang = '-')

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
                    submission_table.append(sub_to_show(recent_submission, user.username, sub_count))
                    if not recent_submission.score in scores:
                        scores[recent_submission.score] = 0
                    scores[recent_submission.score] += 1
                scores = OrderedDict(sorted(scores.items()))
                key_list = []
                score_list = []
                for key,score in scores.items():
                    key_list.append(key)
                    score_list.append(score)
                    
                df = pd.DataFrame(submission_table)
                score_table_path = '/media/assignment/sheets/'+prob_ID+'.xlsx'
                full_table_path = '/opt/vespa' + score_table_path
                if not os.path.isdir('/opt/vespa/media/assignment/sheets/'):
                    os.mkdir('/opt/vespa/media/assignment/sheets/')
                if os.path.isfile(full_table_path):
                    os.remove(full_table_path)
                df.to_excel(full_table_path)
                return render(request, "submission_detail.html", {'submission_table' : submission_table, 'key_list':key_list, 'score_list':score_list, "prob":prob, "sheet_path" : score_table_path})



'''
    여기서부터 관리자 항목 함수
'''
def assignment_registry(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')

    if request.method == "POST":
        prob_id = request.POST["prob_id"]
        prob_name = request.POST["prob_name"]
        try_limit = int(request.POST["try_limit"])
        time_limit = float(request.POST["time_limit"])
        size_limit = int(request.POST["size_limit"])
        start_date = request.POST["start_date"]
        start_time = request.POST["start_time"]
        end_date = request.POST["end_date"]
        end_time = request.POST["end_time"]
        eval_std = request.POST["eval"]
        files = request.FILES
        
        new_problem = ProblemModel(prob_id=prob_id, prob_name=prob_name, try_limit=try_limit, time_limit=time_limit, size_limit=size_limit, eval=eval_std)
        new_problem.starts_at = start_date + ' ' + start_time
        new_problem.ends_at = end_date + ' ' + end_time
        for filename in files:
            if filename == "document": new_problem.document = files['document']
            if filename == "sample_data": new_problem.sample_data = files['sample_data']
            if filename == "sub_data": new_problem.sub_data = files['sub_data']
            if filename == "header_data": new_problem.header_data = files['header_data']
        new_problem.save()

        if "grade_data" in files:
            grade_data = files['grade_data']
            zf = zipfile.ZipFile(grade_data)
            file_list = zf.namelist()
            for i in range(0, len(file_list) // 2):
                gradeModel = GradeModel(problem=new_problem)
                if f"0{i+1}.inp" in file_list:
                    gradeModel.grade_input = DjangoFile(zf.open(file_list[file_list.index(f"0{i+1}.inp")]), name=f"0{i+1}.inp")
                    gradeModel.grade_output = DjangoFile(zf.open(file_list[file_list.index(f"0{i+1}.out")]), name=f"0{i+1}.out")
                else:
                    gradeModel.grade_input = DjangoFile(zf.open(file_list[file_list.index(f"{i+1}.inp")]), name=f"{i+1}.inp")
                    gradeModel.grade_output = DjangoFile(zf.open(file_list[file_list.index(f"{i+1}.out")]), name=f"{i+1}.out")

                gradeModel.save()
        return render(request, "assignment_registry.html");

    return render(request, "assignment_registry.html");


def assignment_manage(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    
    if request.method == "POST":
        if "prob_name" in request.POST:
            prob_id = request.POST["prob_id"]
            prob_name = request.POST["prob_name"]
            try_limit = int(request.POST["try_limit"])
            time_limit = float(request.POST["time_limit"])
            size_limit = int(request.POST["size_limit"])
            start_date = request.POST["start_date"]
            start_time = request.POST["start_time"]
            end_date = request.POST["end_date"]
            end_time = request.POST["end_time"]
            eval_std = request.POST["eval"]
            files = request.FILES

            problem = ProblemModel.objects.get(prob_id=prob_id, prob_name=prob_name)
            problem.starts_at = start_date + ' ' + start_time
            problem.ends_at = end_date + ' ' + end_time
            problem.prob_name = prob_name
            problem.try_limit = try_limit
            problem.size_limit = size_limit
            problem.time_limit = time_limit
            problem.eval = eval_std
            
            for filename in files:
                if filename == "document":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'media',problem.document.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'media',problem.document.name))
                    problem.document = files['document']
                elif filename == "sample_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'media', problem.sample_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'media',problem.sample_data.name))
                    problem.sample_data = files['sample_data']
                elif filename == "sub_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'data', 'assignment', problem.sub_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'data', 'assignment', problem.sub_data.name))
                    problem.sub_data = files['sub_data']
                elif filename == "header_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'data', 'assignment', problem.header_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'data', 'assignment', problem.header_data.name))
                    problem.header_data = files['header_data']
                else:
                    for gradeModel in GradeModel.objects.filter(problem=problem):
                        curr_input_filename = gradeModel.grade_input.name.split('/')[-1]
                        curr_output_filename = gradeModel.grade_output.name.split('/')[-1]
                        if filename == curr_input_filename:
                            if os.path.isfile(os.path.join(settings.BASE_DIR,'data','assignment',gradeModel.grade_input.name)):
                                os.remove(os.path.join(settings.BASE_DIR,'data','assignment',gradeModel.grade_input.name))
                            gradeModel.grade_input = files[filename]
                            gradeModel.save()
                        if filename == curr_output_filename:
                            if os.path.isfile(os.path.join(settings.BASE_DIR,'data','assignment',gradeModel.grade_output.name)):
                                os.remove(os.path.join(settings.BASE_DIR,'data','assignment',gradeModel.grade_output.name))
                            gradeModel.grade_output = files[filename]
                            gradeModel.save()
            problem.save()
            return redirect('assignment_manage')

        prob_id = int(request.POST["prob_id"])
        problem = ProblemModel.objects.get(id=prob_id)
        start_date = problem.starts_at.strftime('%Y-%m-%d')
        start_time = problem.starts_at.strftime('%H:%M')
        end_date = problem.ends_at.strftime('%Y-%m-%d')
        end_time = problem.ends_at.strftime('%H:%M')
        grade_model_list = GradeModel.objects.filter(problem = problem)
        return render(request, "assignment_registry.html", {'problem':problem,
                                                            'start_date':start_date,
                                                            'start_time':start_time,
                                                            'end_date':end_date,
                                                            'end_time':end_time,
                                                            'grade_model_list':grade_model_list});
    prob_list = ProblemModel.objects.all()
    return render(request, "assignment_manage.html",  {'prob_list':prob_list});

def user_approval(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        user_id = int(request.POST["approve_user"])
        approve_user = vespaUser.objects.get(id=user_id)
        approve_user.usertype = "normal"
        approve_user.save()
    newuser = vespaUser.objects.filter(usertype="unapproved")
    return render(request, "user_approval.html",{'newusers' : newuser})

def user_manage(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        if "delete_user" in request.POST:
            user_id = int(request.POST["delete_user"])
            delete_user = vespaUser.objects.get(id=user_id)
            delete_user.delete()
    users = vespaUser.objects.filter(usertype="normal")
    return render(request, "user_manage.html", {'users':users});

def web_setting(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        if 'banner' in request.FILES:
            banner_file = open(os.path.join(settings.BASE_DIR,'static', 'miscs', 'banner.png'), 'wb')
            banner_file.write(request.FILES.get('banner').read())
            banner_file.close()
    return render(request, "settings.html");
