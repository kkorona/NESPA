import subprocess
import glob
import re
import os
import time
def tokenize(str):
    return re.split("[ \t]+",str)

def executes(target_path, eval_path, submission_id, ext):
    inplist = glob.glob(os.path.join(eval_path,"*.inp"))
    
    filenames = [ "".join(x.split('.')[:-1]) for x in inplist]

    results = []
    
    queries = ""
    resf = ""
    
    query_head = ""
    if ext == "cpp":
        query_head = execute_cpp(target_path, submission_id)
    elif ext == "c":
        query_head = execute_c(target_path, submission_id)
    elif ext == "py":
        query_head = execute_py(target_path, submission_id)
    elif ext == "java":
        query_head = execute_c(target_path, submission_id)

    for filename in filenames:
        eval_input_file = os.path.join(eval_path, filename + ".inp")
        eval_output_file = os.path.join(eval_path, filename + ".out")
        query = '"/usr/bin/timeout" 1 ' + query_head + " < " + eval_input_file
        fname = os.path.basename(eval_input_file).split('.')[0]
        queries += query + "\n"
        res = ""
        try:
            timeSt = time.time()
            res = subprocess.check_output(query, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            timeDelta = time.time() - timeSt
            exit_status = subprocess.check_output("/usr/bin/echo $?")
            if exit_status == "124":
                results.append({'filename': fname,'caseRes': "TIME LIMIT EXCEEDED",'exectime': '1'})
                continue
            with open(eval_output_file,"r") as f:
                identical = True
                for line1,line2 in zip(f.readlines(),re.split('[\n]+',res)):
                    t1 = tokenize(line1.lstrip().rstrip())
                    t2 = tokenize(line2.lstrip().rstrip())
                    if not t1 == t2:
                        identical = False
                if identical:
                    results.append({'filename': fname,'caseRes': "CORRECT ANSWER",'exectime': str(timeDelta)})
                else:
                    results.append({'filename': fname,'caseRes': "WRONG ANSWER",'exectime': str(timeDelta)})
        except subprocess.CalledProcessError as e:
            results.append({'filename': fname,'caseRes': "RUNTIME ERROR - " + res,'exectime': '0'})
        except subprocess.TimeoutExpired as e:
            results.append({'filename': fname,'caseRes': "TIME LIMIT EXCEEDED",'exectime': '1'})
        except Exception as e:
            results.append({'filename': fname,'caseRes': str(e), 'exectime' : '0'})
    
    for result in results:
        resf += result['filename'] + " : " + result['caseRes'] + " : " + result['exectime'] + "\n"
    
    target_title = os.path.join(target_path,submission_id)
    with open(target_title + ".que", "w") as f:
        f.write(queries)
    with open(target_title + ".cres", "w") as f:
        f.write(resf)
    return results
       
    
def execute_cpp(target_path, filename):
    query = os.path.join(target_path,filename)
    return query

def execute_c(target_path, filename):
    query = os.path.join(target_path,filename)
    return query

def execute_py(target_path, filename):
    query = "python3 " + os.path.join(target_path,filename) + ".py"
    return query

def execute_java(target_path, filename):
    pass
