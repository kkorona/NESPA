import execute

s1 = "test"
s2 = "test "
Q1 = execute.tokenize(s1.strip())
Q2 = execute.tokenize(s2.strip())
print(Q1)
print(Q2)
print((Q1 == Q2))