import subprocess

def compiles(target_path, ext):
    query = ""
    if ext == "cpp":
        query = compile_cpp(target_path)
    elif ext == "c":
        query = compile_c(target_path)
    elif ext == "py":
        query = compile_py(target_path)
    elif ext == "java":
        query = compile_c(target_path)
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
    
def compile_cpp(target_path):
    # Use this when your OS is Ubuntu.
    # cpp_path_head = "g++"
    # use this when your OS is CentOS 7
    cpp_path_head = "/opt/rh/devtoolset-8/root/usr/bin/g++"
    query = cpp_path_head + " " + target_path + ".cpp -o " + target_path + " -O2 -Wall -lm -static -std=gnu++14"
    return query

def compile_c(target_path):
    query = "gcc " + target_path + ".c -o " + target_path + " -O2 -Wall -lm -static -std=c11"
    return query

def compile_py(target_path):
    query = "python3 -c \"import py_compile; py_compile.compile(r'" + target_path + ".py')\""
    return query

def compile_java(target_path):
    pass
