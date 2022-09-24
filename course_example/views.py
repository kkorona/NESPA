# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import Post, Comment, Attach, vespaUser
from .models import SubmissionModel, ProblemModel, GradeModel
from .forms import CommentForm

import os, shutil, glob, urllib.parse, re

from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

from django.core.files import File as DjangoFile

from . import validation
from . import compile
from . import execute
from . import configs

from collections import OrderedDict
import pandas as pd
import numpy as np
import shutil
import os
import time
import zipfile

from pygments.lexers.c_cpp import CppLexer
from pygments.lexers.python import PythonLexer

# -----------------------------accounts-----------------------

def signup(request):
    if request.method == "GET":
        return render(request, configs.COURSE_NAME + '/signup.html')
        
    if request.method == "POST":
        username = request.POST.get('user_name',None)
        studentNumber = request.POST.get('student_number',None)
        user_id = request.POST.get('user_id',None)
        password1 = request.POST.get('password1',None)
        password2 = request.POST.get('password2',None)
        grade = request.POST.get('grade',None)
        major = request.POST.get('major',None)
        email = request.POST.get('email',None)
        phone = request.POST.get('phone',None)
        usertype = 'unapproved'
        res_data = {}
        
        # validation zone
        
        # user ID
        
        p = re.compile('[a-zA-Z0-9]+')
        
        if p.match(user_id) == None:
            return HttpResponse('잘못된 아이디입니다: '+user_id + '<br>Wrong user id: '+ user_id)
        
        if len(user_id) < 4 or len(user_id) > 10:
            return HttpResponse('아이디가 너무 길거나 짧습니다.<br>ID is too long or too short.')
            
        if len(password1) < 8:
            return HttpResponse('비밀번호가 너무 짧습니다.<br> Password is too short.')

        if password1 == user_id:
            return HttpResponse('비밀번호가 아이디와 같습니다.<br> Password is same with ID.')
        
        # student number
        if not len(studentNumber) == 9:
            return HttpResponse('학번이 잘못되었습니다.<br>Wrong Student Number.')
        
        # email match
        
        p = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if p.match(email) == None:
            return HttpResponse('이메일이 잘못되었습니다.<br>Wrong Email.')
        
        # all-fill validation
        if not (username and studentNumber and user_id and password1 and password2 and grade and major and email and phone):
            return HttpResponse('모든 칸을 빠짐없이 채워주세요.<br> Please fill all the blanks in registeration form.')
            
        # validate passwords
        elif password1 != password2:
            return HttpResponse('비밀번호 확인이 잘못되었습니다.<br>Wrong password confirmation.')
        else:
            user = vespaUser(username=username, studentNumber=studentNumber, password=make_password(password1), user_id=user_id, grade=grade, major=major, email=email, phone=phone, usertype=usertype)
            try:
                c_user = vespaUser.objects.get(user_id=user_id)
                return HttpResponse('이미 등록된 사용자입니다.<br>Already registerd user.')
            except vespaUser.DoesNotExist:
                user.save()
                return redirect(configs.COURSE_NAME+':login')
        return render(request, configs.COURSE_NAME+'/signup.html')

def login(request):
    response_data = {}
    if request.method == "GET":
        return render(request, configs.COURSE_NAME+'/login.html')
        
    elif request.method == "POST":
        login_userid = request.POST["user_id"]
        login_password = request.POST["password"]
        
        if not (login_userid and login_password):
            return HttpResponse('ID나 비밀번호는 비울 수 없습니다.<br>ID or password cannot be empty.')
        else:
            try:
                myuser = vespaUser.objects.get(user_id=login_userid)
                if check_password(login_password, myuser.password):
                    request.session['userid'] = myuser.user_id
                    request.session['username'] = myuser.username
                    request.session['usertype'] = myuser.usertype
                    request.session['logged_in'] = 'YES'
                    return redirect(configs.COURSE_NAME + ':index')
                else:
                    return HttpResponse('ID 또는 비밀번호가 잘못되었습니다.<br>ID or password is invalid.')
            except vespaUser.DoesNotExist:
                return HttpResponse('등록되지 않은 사용자입니다.')
    return render(request,configs.COURSE_NAME+'/login.html')

def logout(request):
    request.session.pop('userid')
    request.session.pop('username')
    request.session.pop('usertype')
    request.session.pop('logged_in')
    return redirect(configs.COURSE_NAME + ':index')


# -----------------------------assignments-----------------------

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

TOKENDICT = {
'Name':'Names',
'Keyword':'Reserved words',
'Operator':'Operators',
'Punctuation':'Punctuations',
'Literal':'Literals',
}

def submission(request):
    if request.method == "GET":
        full_prob_list = ProblemModel.objects.all()
        now = timezone.now()
        cur_prob_list = []
        for prob in full_prob_list:
            if prob.starts_at <= now and prob.ends_at >= now:
                cur_prob_list.append(prob)
        return render(request, configs.COURSE_NAME+'/submission.html', {'full_prob_list' : full_prob_list, 'cur_prob_list':cur_prob_list})
        
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
            return render(request, configs.COURSE_NAME+"/submission_check.html")
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
        
        ext = submission.lang.lower()

        destination_path = os.path.join(settings.BASE_DIR, 'data', configs.COURSE_NAME ,'submission', studentNumber, prob_ID)
        subfile_path = os.path.join(settings.BASE_DIR, 'data', configs.COURSE_NAME, 'assignment', prob_ID, 'subs')
        header_path = os.path.join(settings.BASE_DIR, 'data', configs.COURSE_NAME, 'assignment', prob_ID, 'header')

        target_name = submission.filename()
        target_path = os.path.join(destination_path, target_name)
        target_title = os.path.join(destination_path, str(submission.id)) 
        eval_path = os.path.join(settings.BASE_DIR,'data', configs.COURSE_NAME, 'assignment',prob_ID,'eval')
        
        if os.path.exists(subfile_path):
            subfiles = os.listdir(subfile_path)
            for subfile in subfiles:
                shutil.copyfile(os.path.join(subfile_path,subfile),os.path.join(destination_path,subfile))
        
        code_size = submission.sub_file.size

        compile_result = compile.compiles(target_title, header_path, ext)
        
        if compile_result == 1:
            submission.delete()
            return render(request, configs.COURSE_NAME+"/compile_error.html", {'error_msg' : '컴파일 에러가 발생하였습니다. 소스코드를 확인해주시고, 해결이 안될 경우 조교에게 문의하세요.'})

        src = ""
        with open(target_path,"r") as f:
            src = f.read()
        
        lexer = None
        if ext == 'cpp':
            lexer = CppLexer()
        elif ext == 'c':
            lexer = CppLexer()
        elif ext == 'py':
            lexer = PythonLexer()
        else:
            submission.delete()
            return render(request, configs.COURSE_NAME+"/compile_error.html", {'error_msg' : 'Lexer 구문 분석이 지원되지 않는 언어입니다.'})

        tokens = lexer.get_tokens(src)
        
        token_identified_info = {}
        token_classified_info = {}
        
        prev_key = ""
        for w in tokens :
            token_class = str(w[0])[6:]
            token_key = token_class+"___"+str(w[1])
            if prev_key == token_class:
                continue
            prev_key = token_class
            if token_key in token_identified_info:
                token_identified_info[token_key] += 1
            else:
                token_identified_info[token_key] = 1
                
            if token_class in token_classified_info:
                token_classified_info[token_class] += 1
            else:
                token_classified_info[token_class] = 1
                
        sum_value = 0
        
        for token_key in token_classified_info:
            for valid_token_class in TOKENDICT:
                if valid_token_class in token_key:
                    sum_value += token_classified_info[token_key]

        if sum_value > prob.token_limit:
            submission.delete()
            return render(request, configs.COURSE_NAME+"/compile_error.html", {'error_msg' : 'Token 크기가 초과되었습니다.'})


        execute_result = execute.executes(destination_path, eval_path, header_path, subfile_path, str(submission.id), ext, str(prob.time_limit))
        
        total_tc = len(execute_result)
        if total_tc <=0:
            total_tc = 1
        scored_tc = 0
        total_time = 0.0
        res_out = []
        
        filename_list = []
        caseRes_list = []
        exectime_list = []

        execute_result = sorted(execute_result, key = lambda i : i['filename'])

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
        submission.token_size = sum_value
        
        submission.save()
            
        return render(request, configs.COURSE_NAME+"/result.html", {'prob_id' : prob_ID, 'result_out_table' : res_out, 'score' : str(score), 'total_time' : str(total_time)})
        
        
    return render(request, configs.COURSE_NAME+"/submission_check.html")
    
def assignment_list(request):
    prob_list = ProblemModel.objects.all().order_by('-id')
    return render(request, configs.COURSE_NAME+'/assignment_list.html', {'prob_list':prob_list})
        
def submission_list(request):
    prob_list = ProblemModel.objects.all().order_by('-id')
    return render(request, configs.COURSE_NAME+"/submission_list.html", {'prob_list':prob_list})

def watch_code(request):
    submission_ID = request.GET.get('submission_id', None)
    if submission_ID == "None": submission_ID = -1
    submission = get_object_or_404(SubmissionModel, id=submission_ID)
    code_path = submission.sub_file.path
    code_frame = code_path[:code_path.rfind('.')]
    cerr_file_path = code_frame + ".cerr"
    wal_file_path = code_frame + ".wal"
    code_content = "No code finded."
    cerr_log = "This code was successfully compiled and executed."
    wal_log = "This code had no different output results compared with correct answers."
    if os.path.isfile(code_path) :
        try:
            with open(code_path, 'r', encoding="utf-8") as f:
                code_content = f.read()
        except UnicodeDecodeError:
            with open(code_path, 'r', encoding="ISO-8859-1") as f:
                code_content = f.read()
        code_content = code_content.replace('\\n', '\\\n')
        code_content = code_content.replace('\\t', '\\\t')
        code_content = code_content.replace('\r\n', '\\n')
        code_content = code_content.replace('\r', '\\n')
        code_content = code_content.replace('\n', '\\n')
        code_content = code_content.replace('\r\t', '\\t').replace('\r', '\\t').replace('\t', '\\t')
        code_content = code_content.replace('\"', '\\\"')
    if os.path.isfile(cerr_file_path) :
        with open(cerr_file_path, 'r', encoding = "utf-8") as f:
            cerr_log = f.read()
    if os.path.isfile(wal_file_path) :
        with open(wal_file_path, 'r', encoding = "utf-8") as f:
            wal_log = f.read()

    return render(request, configs.COURSE_NAME+"/watch_code.html", {'code_content' : code_content, 'lang': submission.lang, 'path':code_path, 'cerr': cerr_log, 'wal':wal_log})
    
def sub_to_show(sub, name, count):
    show = {}
    show['client_ID'] = sub.client_ID
    show['username'] = name
    show['client_number'] = sub.client_number
    show['prob_ID'] = sub.prob_ID
    if sub.created_at != "-":
        show['created_at'] = sub.created_at.strftime('%m/%d %H:%M')
    show['score'] = sub.score
    show['exec_time'] = sub.exec_time
    show['code_size'] = sub.code_size
    show['token_size'] = sub.token_size
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
                    recent_submission = SubmissionModel(client_ID = user.user_id, client_number = user.studentNumber, prob_ID = prob_ID, created_at = "-", score = 0, exec_time = 0.0, code_size = 0, token_size = 0, lang = '-')

                if not recent_submission.score in scores:
                    scores[recent_submission.score] = 0
                scores[recent_submission.score] += 1
            scores = OrderedDict(sorted(scores.items()))
            key_list = []
            score_list = []
            for key,score in scores.items():
                key_list.append(key)
                score_list.append(score)

            return render(request, configs.COURSE_NAME+"/submission_detail.html", {'submission_table' : submission_table, 'key_list':key_list, 'score_list':score_list, "prob":prob})

        elif request.session['usertype'] == 'admin':
            if prob_ID == 'full':
                submission_table = SubmissionModel.objects.all()
                return render(request, configs.COURSE_NAME+"/submission_detail.html", {'submission_table' : submission_table})
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
                        recent_submission = SubmissionModel(client_ID = user.user_id, client_number = user.studentNumber, prob_ID = prob_ID, created_at = "-" , score = 0, exec_time = 0.0, code_size = 0, token_size = 0, lang = '-')
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
                score_table_path = '/media/'+configs.COURSE_NAME+'/assignment/sheets/'+prob_ID+'.xlsx'
                full_table_path = '/opt/vespa' + score_table_path
                if not os.path.isdir('/opt/vespa/media/'+configs.COURSE_NAME+'/assignment/sheets/'):
                    os.makedirs('/opt/vespa/media/'+configs.COURSE_NAME+'/assignment/sheets/')
                if os.path.isfile(full_table_path):
                    os.remove(full_table_path)
                df.to_excel(full_table_path)
                return render(request, configs.COURSE_NAME+"/submission_detail.html", {'submission_table' : submission_table, 'key_list':key_list, 'score_list':score_list, "prob":prob, "sheet_path" : score_table_path})



'''
    여기서부터 관리자 항목 함수
'''

def dos2unix_converting(prob_id):
    path = os.path.join("/opt","vespa","data",configs.COURSE_NAME,"assignment",str(prob_id),"eval")
    filelist = [os.path.join(path, x) for x in os.listdir(path)]
    for filename in filelist:
        os.system("dos2unix " + filename)
    
    
def assignment_registry(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')

    if request.method == "POST":
        prob_id = request.POST["prob_id"]
        prob_name = request.POST["prob_name"]
        try_limit = int(request.POST["try_limit"])
        time_limit = float(request.POST["time_limit"])
        size_limit = int(request.POST["size_limit"])
        token_limit = int(request.POST["token_limit"])
        start_date = request.POST["start_date"]
        start_time = request.POST["start_time"]
        end_date = request.POST["end_date"]
        end_time = request.POST["end_time"]
        eval_std = request.POST["eval"]
        files = request.FILES
        
        new_problem = ProblemModel(prob_id=prob_id, prob_name=prob_name, try_limit=try_limit, time_limit=time_limit, size_limit=size_limit, token_limit=token_limit, eval=eval_std)
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
            dos2unix_converting(prob_id)
        return render(request, configs.COURSE_NAME+"/assignment_registry.html");

    return render(request, configs.COURSE_NAME+"/assignment_registry.html");


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
            token_limit = int(request.POST["token_limit"])
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
            problem.token_limit = token_limit
            problem.time_limit = time_limit
            problem.eval = eval_std
            
            configs.log("Changing files of Problem #"+prob_id)
            for filename in files:
                if filename == "document":
                    configs.log("document file changed")
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'media',configs.COURSE_NAME, problem.document.name)):
                        doc_path = os.path.join(settings.BASE_DIR,'media',configs.COURSE_NAME, problem.document.name)
                        os.remove(docpath)
                        configs.log("remove : "+doc_path)
                    problem.document = files['document']
                elif filename == "sample_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'media', configs.COURSE_NAME, problem.sample_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'media',configs.COURSE_NAME, problem.sample_data.name))
                    problem.sample_data = files['sample_data']
                elif filename == "sub_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME, 'assignment', problem.sub_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'data', configs.COURSE_NAME, 'assignment', problem.sub_data.name))
                    problem.sub_data = files['sub_data']
                elif filename == "header_data":
                    if os.path.isfile(os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME, 'assignment', problem.header_data.name)):
                        os.remove(os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME, 'assignment', problem.header_data.name))
                    problem.header_data = files['header_data']
                else:
                    for gradeModel in GradeModel.objects.filter(problem=problem):
                        curr_input_filename = gradeModel.grade_input.name.split('/')[-1]
                        curr_output_filename = gradeModel.grade_output.name.split('/')[-1]
                        configs.log("filename: {}, cur_input : {}, cur_output : {}".format(filename, curr_input_filename, curr_output_filename))
                        if filename == curr_input_filename:
                            if os.path.isfile(os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME,'assignment',gradeModel.grade_input.name)):
                                inp_file_path = os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME,'assignment',gradeModel.grade_input.name)
                                configs.log("remove : {}, changed : {}".format(inp_file_path,files[filename]))
                                os.remove(inp_file_path)
                            gradeModel.grade_input = files[filename]
                            gradeModel.save()
                        if filename == curr_output_filename:
                            if os.path.isfile(os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME,'assignment',gradeModel.grade_output.name)):
                                out_file_path = os.path.join(settings.BASE_DIR,'data',configs.COURSE_NAME,'assignment',gradeModel.grade_output.name)
                                configs.log("remove : {}, changed : {}".format(out_file_path,files[filename]))
                                os.remove(out_file_path)
                            gradeModel.grade_output = files[filename]
                            gradeModel.save()
            problem.save()
            configs.log("Finished")
            return redirect(configs.COURSE_NAME+':assignment_manage')

        prob_id = int(request.POST["prob_id"])
        problem = ProblemModel.objects.get(id=prob_id)
        start_date = problem.starts_at.strftime('%Y-%m-%d')
        start_time = problem.starts_at.strftime('%H:%M')
        end_date = problem.ends_at.strftime('%Y-%m-%d')
        end_time = problem.ends_at.strftime('%H:%M')
        grade_model_list = GradeModel.objects.filter(problem = problem)
        return render(request, configs.COURSE_NAME+"/assignment_registry.html", {'problem':problem,
                                                            'start_date':start_date,
                                                            'start_time':start_time,
                                                            'end_date':end_date,
                                                            'end_time':end_time,
                                                            'grade_model_list':grade_model_list});
    prob_list = ProblemModel.objects.all().order_by("-id")
    return render(request, configs.COURSE_NAME+"/assignment_manage.html",  {'prob_list':prob_list});

def user_approval(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        user_id = int(request.POST["approve_user"])
        approve_user = vespaUser.objects.get(id=user_id)
        approve_user.usertype = "normal"
        approve_user.save()
    newuser = vespaUser.objects.filter(usertype="unapproved")
    return render(request, configs.COURSE_NAME+"/user_approval.html",{'newusers' : newuser})

def user_manage(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        if "delete_user" in request.POST:
            user_id = int(request.POST["delete_user"])
            delete_user = vespaUser.objects.get(id=user_id)
            delete_user.delete()
    users = vespaUser.objects.filter(usertype="normal")
    return render(request, configs.COURSE_NAME+"/user_manage.html", {'users':users});

def web_setting(request):
    if request.session['usertype'] != 'admin':
            return HttpResponse('허용되지 않은 기능입니다.')
    if request.method == "POST":
        if 'banner' in request.FILES:
            banner_file = open(os.path.join(settings.BASE_DIR,'static', 'miscs', 'banner_'+configs.COURSE_NAME+'.png'), 'wb')
            banner_file.write(request.FILES.get('banner').read())
            banner_file.close()
    return render(request, configs.COURSE_NAME+"/settings.html");
    
# -----------------------------board-----------------------


board_names = {
"notice":"공지사항 / Notices",
"forum":"자유게시판 / Forum",
"qna":"질문게시판 / QnA",
"reports":"평가게시판 / Reports",
"error_reports":"오류보고게시판 / Error Reports",
"course":"강의자료실 / Course Materials",
}

class PostLV(ListView):
    model = Post
    context_object_name = 'posts'
    paginate_by = 15
    template_name= configs.COURSE_NAME + "/post_list.html"
    def get_queryset(self, **kwargs):
        cur_board_info = self.kwargs['board_info']
        article_context = Post.objects.filter(board_info = cur_board_info)
        return article_context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_board_info = self.kwargs['board_info']
        context['board_title'] = board_names[cur_board_info]
        context['board_info'] = cur_board_info
        return context

class PostDV(FormMixin, DetailView):
    model = Post
    form_class = CommentForm
    template_name= configs.COURSE_NAME + "/post_detail.html"

    def get_success_url(self, **kwargs):
        return reverse(configs.COURSE_NAME + ':post_detail', kwargs = {'pk': self.object.pk })
        
    def get_context_data(self, **kwargs):
        context = super(PostDV, self).get_context_data(**kwargs)
        
        post_id = self.kwargs['pk']
        if f'username/board/{post_id}' not in self.request.session:
            current_post = Post.objects.get(pk=post_id)
            current_post.update_counter
            self.request.session[f'username/board/{post_id}'] = True

        context['form'] = CommentForm(initial={
            'text' : '댓글을 입력해주세요.',
        })
        if 'logged_in' in self.request.session:
            context['user'] = self.request.session['userid']
        else:
            context['user'] = 'anonymous'
        context['comments'] = sorted(list(self.object.comment_set.all()), key=lambda x: x.pub_date, reverse=False)
        context['attachments'] = self.object.attach_set.all()
        cur_board_info = self.object.board_info
        context['board_title'] = board_names[cur_board_info]
        context['board_info'] = cur_board_info
        
        # Markdown Replacement
        content = self.object.content
        content = content.replace('\\n', '\\\n')
        content = content.replace('\\t', '\\\t')
        content = content.replace('\r\n', '\\n')
        content = content.replace('\r', '\\n')
        content = content.replace('\n', '\\n')
        content = content.replace('\r\t', '\\t').replace('\r', '\\t').replace('\t', '\\t')
        content = content.replace('\"', '\\\"')
        
        context['content'] = content
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
        comment_id = int(self.request.POST.get('comment_id'))
        retweet_id = int(self.request.POST.get('retweet_id'))
        if retweet_id != -1 and comment_id == -1:
            comment = form.save(commit=False)
            comment.parent = get_object_or_404(Post, pk=self.object.pk)
            comment.author = self.request.session['userid']
            comment.retweet = get_object_or_404(Comment, pk=retweet_id)
            comment.save()
            return super(PostDV, self).form_valid(form)

        if comment_id == -1:
            comment = form.save(commit=False)
            comment.parent = get_object_or_404(Post, pk=self.object.pk)
            comment.author = self.request.session['userid']
            comment.save()
        else:
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.text = self.request.POST.get('text')
            comment.save()
        return super(PostDV, self).form_valid(form)

def edit(request, article_id):
    username = request.session['username']
    usertype = request.session['usertype']
    userid = request.session['userid']
    article = Post.objects.get(id=article_id)
    
    if usertype == "unapproved":
        return HttpResponse('접근할 수 없는 기능입니다.')
    
    if usertype == "normal":
        if article.author != userid:
            return HttpResponse('수정 권한이 없습니다.')
    
    if request.method == "POST":
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)
        if title == "" or content == "":
            return HttpResponse('제목 또는 내용이 비어있습니다.')
        article.title = title
        article.content = content
        article.save()

        files = request.FILES.getlist('attach_files')
        existing_files = request.POST.getlist('existing_files')
        print(existing_files)
        for attach in article.attach_set.all():
            if str(attach.id) not in existing_files:
                attach.delete()
        
        fs = FileSystemStorage()
        for file in files:
            fname = urllib.parse.unquote(file.name)
            filename = fs.save(fname,file)
            uploaded_file_url = fs.url(filename)
            departure_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, uploaded_file_url[1:]))
            destination_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, 'media','attached',configs.COURSE_NAME, article.board_info, str(article.id)))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            destination_path = os.path.join(destination_path, fname)
            shutil.move(departure_path,destination_path)
            ext = filename.split(".")[-1]
            attach = Attach(parent=article, path = destination_path,name=fname, ext = ext)
            attach.save()
        return redirect(configs.COURSE_NAME + ':post_detail', pk=int(article_id))
        
    if request.method == "GET":
        content = article.content
        content = content.replace('\\n', '\\\n')
        content = content.replace('\\t', '\\\t')
        content = content.replace('\r\n', '\\n').replace('\r', '\\n').replace('\n', '\\n')
        content = content.replace('\r\t', '\\t').replace('\r', '\\t')
        content = content.replace("\"", "\\\"").replace('\'', '\\\'')
        i_board_info = article.board_info
        return render(request, configs.COURSE_NAME + '/edit.html',{'article_content' : content, 'article_title' : article.title, 'attachments' : article.attach_set.all(), 'board_info': i_board_info, 'board_title' : board_names[i_board_info]})


def write(request, i_board_info):
    if request.method == "GET":
        return render(request, configs.COURSE_NAME + '/write.html', {'board_info': i_board_info, 'board_title' : board_names[i_board_info]})
    if request.method == "POST":
        username = request.session['username']
        usertype = request.session['usertype']
        userid = request.session['userid']
        if usertype == "unapproved":
            return HttpResponse('접근할 수 없는 기능입니다.')
            
        title = request.POST.get('post_title',None)
        content = request.POST.get('post_contents',None)

        if title == "" or content == "":
            return HttpResponse('제목 또는 내용이 비어있습니다.')
        if i_board_info == "notices":
            author = username
        else:
            author = userid
        article = Post(title = title, author = author, content=content, board_info = i_board_info, post_hit = 0)
        article.save()

        files = request.FILES.getlist('attach_files')
        fs = FileSystemStorage()
        for file in files:
            fname = urllib.parse.unquote(file.name)
            filename = fs.save(fname,file)
            uploaded_file_url = fs.url(filename)
            departure_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, uploaded_file_url[1:]))
            destination_path = urllib.parse.unquote(os.path.join(settings.BASE_DIR, 'media','attached',configs.COURSE_NAME,i_board_info,str(article.id)))
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)
            destination_path = os.path.join(destination_path, fname)
            shutil.move(departure_path,destination_path)
            ext = filename.split(".")[-1]
            attach = Attach(parent=article, path = destination_path,name=fname, ext = ext)
            attach.save()
            
        return redirect(configs.COURSE_NAME+':post_list', board_info = i_board_info)

def deleteComment(request, article_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.deleted = True
    comment.save()
    return redirect(configs.COURSE_NAME +':post_detail', pk=int(article_id))
    
def index(request):
    return render(request, configs.COURSE_NAME + '/index.html')
    
def nespa_dev(request):
    return render(request, configs.COURSE_NAME + '/nespa_dev.html')

def page_not_found(request, exception):
    return render(request, configs.COURSE_NAME + '/404.html', {})
    
def lexer(request):
    if request.method == "GET":
        return render(request, configs.COURSE_NAME + '/lexer.html',{})
    if request.method == "POST":
        language = request.POST.get('language',None)
        
        src = request.POST.get('codeblocks',None)

        lexer = None
        if language == '01': 
            lexer = CppLexer()
        elif language == '02': 
            lexer = CppLexer()
        elif language == '03':
            lexer = PythonLexer()


        if lexer == None:
            return HttpResponse('Token이 지원되지 않는 언어입니다.')

        tokens = lexer.get_tokens(src)
        
        token_identified_info = {}
        token_classified_info = {}
        
        prev_key = ""
        for w in tokens :
            token_class = str(w[0])[6:]
            token_key = token_class+"___"+str(w[1])
            if prev_key == token_class:
                continue
            prev_key = token_class
            if token_key in token_identified_info:
                token_identified_info[token_key] += 1
            else:
                token_identified_info[token_key] = 1
                
            if token_class in token_classified_info:
                token_classified_info[token_class] += 1
            else:
                token_classified_info[token_class] = 1
                
        ret = {}
        sum_value = 0
        
        for valid_token_class in TOKENDICT:
            ret[TOKENDICT[valid_token_class]] = 0
        
        for token_key in token_classified_info:
            for valid_token_class in TOKENDICT:
                if valid_token_class in token_key:
                    ret[TOKENDICT[valid_token_class]] +=  token_classified_info[token_key]
                    sum_value += token_classified_info[token_key]
                    
        for k in list(ret.keys()):
            if ret[k] == 0:
                del ret[k]
            else:
                ret[k] = str(ret[k])
        ret['Sum of Tokens'] = str(sum_value)
        
        return render(request, configs.COURSE_NAME + '/lexer.html',{"src":src, "ret":ret})
        
