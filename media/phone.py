import matplotlib.pyplot as plt 
import numpy as np

def main():
    N = int(input())# Number of items( evaluation, price )
    phone = []    
    for i in range(N):
        phone.append(list(map(int,(input().split()))))
    original=phone[:]# copy phone list to find index of original list
    phone.sort(reverse=True , key=lambda x:x[1])
    for i in (phone):
        print(i[0], i[1])
    result = []
    flag = False
    for i in range(len(phone)):
        flag = False
        for j in range(i+1, len(phone)):             
            if phone[i][0] <= phone[j][0]:      
                flag = True           
                break
        if flag == False:
            result.append(phone[i])
    t_idx=0   
    t_idx_list=[]
    for i in range(len(result)):
        t_idx = original.index(result[i])
        t_idx_list.append(t_idx)        
    t_idx_list.sort()
    for i in t_idx_list:
        print(i+1)#because the starting point of list is '0' , so add '1'
if __name__ == "__main__":
    main()