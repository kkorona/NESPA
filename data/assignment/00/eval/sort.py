q = input()
N = int(q)
q = input()
numbers = [int(x) for x in q.split(' ')]

numbers = sorted(numbers)
res = ""
for x in numbers:
    res += "%d " % (x)
print(res)