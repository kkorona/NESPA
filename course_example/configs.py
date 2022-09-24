import os

### 
#
#  ** Essential configurations **
#  : configurations about essential course informations
#  - course name
#
###

COURSE_NAME = "course_example"

### 
#
#  ** logging configurations **
#  : configurations about logging options and path
#  - log file path for problem configuration change
#
###

LOGGING_PATH = "/opt/vespa/logs/"+COURSE_NAME+".log"

def log(log_content):
    edit_mode = "a"
    if not os.path.isfile(LOGGING_PATH):
        edit_mode = "w"
    with open(LOGGING_PATH,edit_mode) as f:
        f.write(log_content+"\n")


### 
#
#  ** compile configurations **
#  : configurations about compile process while judging
#  - options for compile on each language
#
###

C_PATH_HEAD = "gcc"
C_COMPILE_OPTION = " -O2 -Wall -lm -static -std=c11"
C_COMPILE_QUERY = C_PATH_HEAD + " {}.c -o {}"+ C_COMPILE_OPTION

CPP_PATH_HEAD = "g++"
CPP_COMPILE_OPTION = " -O2 -Wall -lm -static -std=gnu++14"
CPP_COMPILE_QUERY = CPP_PATH_HEAD + " {}.cpp -o {}"+ CPP_COMPILE_OPTION

PYTHON_COMPILE_QUERY = "python3 -c \"import py_compile; py_compile.compile(r' {}.py')\""

JAVA_COMPILE_QUERY = "javac -J-Xms1024m -J-Xmx1920m -J-Xss512m -encoding UTF-8 {}.java"

def get_c_compile_query(input_path, header_path):
    query = C_COMPILE_OPTION.format(input_path, input_path)
    if os.path.exists(header_path):
        query += " -I"+header_path
    return query

def get_cpp_compile_query(input_path, header_path):
    query = CPP_COMPILE_OPTION.format(input_path, input_path)
    if os.path.exists(header_path):
        query += " -I"+header_path
    return query

def get_python_compile_query(input_path):
    return PYTHON_COMPILE_QUERY.format(input_path)

def get_java_compile_query(input_path):
    return JAVA_COMPILE_QUERY.format(input_path)

### 
#
#  ** execution configurations **
#  : configurations about execution process while judging
#  - options for execution on python3 and java
#  - system timeout command
#
###

C_EXECUTION_HEAD = ""
CPP_EXECUTION_HEAD = ""
PYTHON_EXECUTION_HEAD = "python3 "
JAVA_EXECUTION_HEAD = "java -Xms1024m -Xmx1920m -Xss512m -Dfile.encoding=UTF-8 "

def get_c_execution_query(input_path):
    return C_EXECUTION_HEAD + input_path

def get_cpp_execution_query(input_path):
    return CPP_EXECUTION_HEAD + input_path

def get_python_execution_query(input_path):
    return PYTHON_EXECUTION_HEAD + input_path

def get_java_execution_query(input_path):
    return JAVA_EXECUTION_HEAD + input_path
    
def get_timeout_query(timeout, execution_query_head, eval_input_file_path):
    return '"/usr/bin/timeout" '+ timeout + 's ' + execution_query_head + " < " + eval_input_file_path