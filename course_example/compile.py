import subprocess
import os

from . import configs

### 
#
#  ** compile routine functions **
#  : functions about compile process
#  - generate queries for compile on target language
#  - .que file contains those queries
#    * overwrite problem occurs with .que files in execute.py : needs to be resolved.
#  - execute compile queries with subprocess module
#  - .cerr file will be generated when compile fails
#  - .cerr file contains log compile error
#    * overwrite problem occurs with .cerr files in execute.py : needs to be resolved.
#
###

def compiles(target_path, header_path, ext):
    query = ""
    if ext == "cpp":
        query = compile_cpp(target_path, header_path)
    elif ext == "c":
        query = compile_c(target_path, header_path)
    elif ext == "py":
        query = compile_py(target_path, header_path)
    elif ext == "java":
        query = compile_java(target_path, header_path)
    with open(target_path + ".que", "w") as f:
        f.write(query)
        
    res = ""
    try:
        res = subprocess.check_output(query, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        with open(target_path + ".cerr", "w") as f:
            f.write(str(e.output))
        return 1
    return 0
    
def compile_cpp(input_path, header_path):
    query = configs.get_cpp_compile_query(input_path, header_path)
    return query

def compile_c(input_path, header_path):
    query = configs.get_c_compile_query(input_path, header_path)
    return query

def compile_py(input_path, header_path):
    query = configs.get_python_compile_query(input_path)
    return query

def compile_java(input_path, header_path):
    query = configs.get_java_compile_query(input_path)
    return query


