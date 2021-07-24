def cut(target, st, ed):
    return target[0:st] + target[ed:]

def front(target, st, ed):
    return target[st:ed] + target[0:st] + target[ed:]
    
def back(target, st, ed):
    return target[0:st] + target[ed:] + target[st:ed]
    
def double(target, st, ed):
    return target[0:st] + target[st:ed] + target[st:ed] + target[ed:]

def flip(target, st, ed):
    revstr = ''.join(reversed(target[st:ed]))
    return target[0:st] + revstr + target[ed:]

DNA_FILE_NAME = "sapiens.txt"
lines = None
with open(DNA_FILE_NAME, "r") as f:
    lines = f.readlines();

dna_line = ""
for line in lines:
    dna_line += line.rstrip()
   
N = int(input())
for i in range(N):
    command = input().split(" ")
    order = command[0]
    st = int(command[1])-1
    ed = int(command[2])
    if order == "front":
        dna_line = front(dna_line, st,ed)
    if order == "back":
        dna_line = back(dna_line, st,ed)
    if order == "cut":
        dna_line = cut(dna_line, st,ed)
    if order == "double":
        dna_line = double(dna_line, st,ed)
    if order == "flip":
        dna_line = flip(dna_line, st,ed)
    if order == "report":
        print(dna_line[st:ed])