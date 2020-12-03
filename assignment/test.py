import execute
import re

v1 = ["OOXOX\n","OXOOX\n"]
s2 = "OOXOX \nOXOOX \n"
s2 = s2.strip()
v2 = re.split('[\n]+',s2)

# print(v1)
for k in v1:
    print(k.strip())
# print(v2)
for k in v2:
    print(k.strip())
