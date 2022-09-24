import subprocess
import glob
import re
import os
import time

from . import configs

### 
#
#  ** execution routine functions **
#  : functions about execution process
#  - generate queries for execution on target language and each test cases
#  - .que file contains those queries
#    * overwrite problem occurs with .que files in compile.py : needs to be resolved.
#  - execute queries with subprocess module
#  - .cerr file will be generated when compile fails
#  - .cerr file contains log compile error
#    * overwrite problem occurs with .cerr files in compile.py : needs to be resolved.
#  - .cres file will be generated after successful execution
#  - .cres file contains result of execution on each test cases
#  - .wal file will be generated if warning message occurs
#  - .wal file contains warning messages
#
###

def tokenize(str):
    return re.split("[ \t]+",str)

def executes(target_path, eval_path, header_path, subs_path, submission_id, ext, timeout):
    inplist = glob.glob(os.path.join(eval_path,"*.inp"))
    
    filenames = [ "".join(x.split('.')[:-1]) for x in inplist]

    results = []
    
    queries = ""
    resf = ""
    raw_res = ""
    
    query_head = ""
    if ext == "cpp":
        query_head = execute_cpp(target_path, submission_id, header_path)
    elif ext == "c":
        query_head = execute_c(target_path, submission_id, header_path)
    elif ext == "py":
        query_head = execute_py(target_path, submission_id, header_path)
    elif ext == "java":
        query_head = execute_java(target_path, submission_id, header_path)
        filelist = os.listdir(target_path)
        for item in filelist:
            if item.endswith(".class"):
                os.remove(os.path.join(target_path, item))

    target_title = os.path.join(target_path, submission_id)
    err_log = ""
    for filename in filenames:
        eval_input_file_path = os.path.join(eval_path, filename + ".inp")
        eval_output_file_path = os.path.join(eval_path, filename + ".out")
        query = configs.get_timeout_query(timeout, query_head, eval_input_file_path)
        fname = os.path.basename(eval_input_file_path).split('.')[0]
        queries += query + "\n"
        res = ""
        try:
            timeSt = time.time()
            res = subprocess.check_output(query, cwd=target_path, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            timeDelta = time.time() - timeSt
            res = res.strip()
            l2 = re.split('[\n]+',res)
            with open(eval_output_file_path,"r") as f:
                l1 = f.readlines()
                identical = True
                if len(l1) != len(l2):
                    identical = False
                for line1,line2 in zip(l1,l2):
                    t1 = tokenize(line1.strip())
                    t2 = tokenize(line2.strip())
                    if not t1 == t2:
                        identical = False
                if identical:
                    results.append({'filename': fname,'caseRes': "CORRECT ANSWER",'exectime': str(timeDelta)})
                else:
                    results.append({'filename': fname,'caseRes': "WRONG ANSWER",'exectime': str(timeDelta)})
                    raw_res += fname+"\n"+res+"\n"
        except subprocess.CalledProcessError as e:
            if e.returncode == 124:
                results.append({'filename': fname,'caseRes': "TIME LIMIT EXCEEDED",'exectime': timeout})
            else:
                results.append({'filename': fname,'caseRes': "RUNTIME ERROR - " + res,'exectime': '0'})
                err_log += str(e.output)

        except subprocess.TimeoutExpired as e:
            results.append({'filename': fname,'caseRes': "TIME LIMIT EXCEEDED",'exectime': timeout})
        except Exception as e:
            results.append({'filename': fname,'caseRes': str(e), 'exectime' : '0'})

    for result in results:
        resf += result['filename'] + " : " + result['caseRes'] + " : " + result['exectime'] + "\n"

    if err_log:
        with open(target_title + ".cerr", "w") as f:
            f.write(err_log)

    with open(target_title + ".que", "w") as f:
        f.write(queries)
    with open(target_title + ".cres", "w") as f:
        f.write(resf)
    if raw_res != "":
        with open(target_title + ".wal", "w") as f:
            f.write(raw_res)
    return results
       
def execute_c(target_path, filename, header_path):
    file_path = os.path.join(target_path,filename)
    query = configs.get_c_execution_query(file_path)
    return query
    
def execute_cpp(target_path, filename, header_path):
    file_path = os.path.join(target_path,filename)
    query = configs.get_cpp_execution_query(file_path)
    return query

def execute_py(target_path, filename, header_path):
    file_path = os.path.join(target_path,filename) + ".py"
    query = configs.get_python_execution_query(file_path)
    return query

def execute_java(target_path, filename, header_path):
    file_path = os.path.join(target_path, filename) + ".java"
    query = configs.get_java_execution_query(file_path)
    return query


