import re

def validate(FILE_PATH, TYPE):
    code = ""
    with open(FILE_PATH, 'r') as f:
        code += "".join(f.readlines())
    if TYPE == "01" :
        return validate_CPP(code, "WHITELIST")
    elif TYPE == "02" :
        return validate_C(code, "WHITELIST")
    elif TYPE == "03" :
        return validate_py(code, "BLACKLIST")
    elif TYPE == "04" :
        return validate_JAVA(code, "WHITELIST")
    else :
        return (-1, "Wrong language type.")

def validate_CPP(CODE, POLICY):
    whitelist = set()
    with open('restrictions/whitelist_cpp.txt', 'r') as f:
        for x in f.readlines():
            whitelist.add(x.rstrip()) 
    
    blacklist = set()
    
    with open('restrictions/blacklist_cpp.txt', 'r') as f:
        for x in f.readlines():
            blacklist.add(x.rstrip())
    
    lib_pattern = r'#include[ ]*<(?P<content>[a-zA-Z. ]+)>'
    query = re.compile(lib_pattern)
    libs = query.findall(CODE)
    libs = set([x.lstrip().rstrip() for x in libs])
    
    if POLICY == "WHITELIST":
        remove_queue = set()
        for x in whitelist:
            for y in libs:
                if x in y:
                    remove_queue.add(y)
        for y in remove_queue:
            libs.remove(y)
        if len(libs) == 0:
            return (1,"Validation success")
        return (0, "Whitelist violation : " + ''.join(libs))

    else:
        for x in blacklist:
            for y in libs:
                if x in y:
                    return (0, "Blacklist violation")
        return True
    
    

def validate_C(CODE, POLICY):
    whitelist = set()
    with open('restrictions/whitelist_c.txt','r') as f:
        for x in f.readlines():
            whitelist.add(x.rstrip()) 
    
    blacklist = set()
    
    with open('restrictions/blacklist_c.txt','r') as f:
        for x in f.readlines():
            blacklist.add(x.rstrip())
    
    lib_pattern = r'#include[ ]*<(?P<content>[a-zA-Z. ]+)>'
    query = re.compile(lib_pattern)
    libs = query.findall(CODE)
    libs = set([x.lstrip().rstrip() for x in libs])
    
    if POLICY == "WHITELIST":
        remove_queue = set()
        for x in whitelist:
            for y in libs:
                if x in y:
                    remove_queue.add(y)
        if len(libs) == len(remove_queue):
            return True
        return False

    else:
        for x in blacklist:
            for y in libs:
                if x in y:
                    return False
        return True

def validate_py(CODE, POLICY):
    whitelist = set()
    with open('restrictions/whitelist_py.txt','r') as f:
        for x in f.readlines():
            whitelist.add(x.rstrip()) 
    
    blacklist = set()
    
    # https://docs.python.org/ko/3/library/index.html
    
    with open('restrictions/blacklist_py.txt','r') as f:
        for x in f.readlines():
            blacklist.add(x.rstrip())
    
    lib_pattern = r'import (?P<content>.*)'
    query = re.compile(lib_pattern)
    libs = query.findall(CODE)
    libs = [x.rstrip() for x in libs]
    
    if POLICY == "WHITELIST":
        remove_queue = set()
        for x in whitelist:
            for y in libs:
                if x in y:
                    remove_queue.add(y)
        if len(libs) == len(remove_queue):
            return True
        return False

    else:
        for x in blacklist:
            for y in libs:
                if x in y:
                    return False
        return True

def validate_JAVA(CODE, POLICY):
    return True
    
    
if __name__ == "__main__" :
    # print(validate('test.py','03'))
    pass