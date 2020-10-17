import sys
#2839
n = int(input())

result = 0

if n in [1,2,4,7]:
    result = -1
else:
    while n>0:
        if n>12:
            result += 1
            n -= 5
        else:
            if n%5==0:
                result += n//5
                n -= 5*(n//5)
            elif n%3==0:
                result += n//3
                n -= 3*(n//3)
            else:
                result += 1
                n -= 5

print(result)