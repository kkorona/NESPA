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
        return (1,str(e.output))
    return (0,res)
    
def compile_cpp(target_path):
    query = "g++ " + target_path + ".cpp -o " + target_path + " -O2 -Wall -lm -static -std=gnu++14"
    return query

def compile_c(target_path):
    query = "gcc " + target_path + ".cpp -o " + target_path + " -O2 -Wall -lm -static -std=gnu++14"
    return query

def compile_py(target_path):
    pass

def compile_java(target_path):
    pass