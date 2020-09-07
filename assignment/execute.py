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
        query = query_head + " < " + eval_input_file
        queries += query + "\n"
        try:
            timeSt = time.time()
            res = subprocess.check_output(query, stderr=subprocess.STDOUT, timeout = 1, shell=True, universal_newlines=True)
            timeDelta = time.time() - timeSt
            with open(eval_output_file,"r") as f:
                identical = True
                for line1,line2 in zip(f.readlines(),re.split('[\n]+',res)):
                    t1 = tokenize(line1.lstrip().rstrip())
                    t2 = tokenize(line2.lstrip().rstrip())
                    if not t1 == t2:
                        identical = False
                if identical:
                    results.append((filename,"CORRECT ANSWER", str(timeDelta)))
                else:
                    results.append((filename,"WRONG ANSWER", str(timeDelta)))
        except subprocess.CalledProcessError as e:
            results.append((filename,"RUNTIME ERROR", "0.0"))
    
    for result in results:
        resf += result[0] + " : " + result[1] + " : " + result[2] + "\n"
    
    target_title = os.path.join(target_path,submission_id)
    with open(target_title + ".que", "w") as f:
        f.write(queries)
    with open(target_title + ".cres", "w") as f:
        f.write(resf)
    return results
       
    
def execute_cpp(target_path, filename):
    query = os.path.join(target_path,filename)
    return query

def execute_c(target_path):
    pass

def execute_py(target_path):
    pass

def execute_java(target_path):
    pass