
def main():
    n = input().split()
    res = input().split()
    res = list(map(int,res))

    r = int(n[1])#사전식순서에서 해의 개수
    n = int(n[0])#상품권개수   
    
    c = res[n]
    del res[n]
     
    #sol = [ 0 for i in range(n)]
    sol = []
    temp = [ 1 for i in range(n)] # 1 1 1 1 1 1 0
    
    idx = n-1
    cnt = 0
    
    flag = False
    while True:      
        
        tempc = 0
        for i in range(n):
            tempc += ( res[i] * temp[i] )     
        if tempc == c :
            sol.append(list(temp))    
            cnt += 1              
        if temp[idx] == c:
            for i in range(n-1, -1, -1):  
                if temp[i] == c :
                    if i == 0 :
                        flag = True
                        break
                    
                    temp[i] = 1
                    temp[idx] = 0

                else :
                    temp[i] += 1
                    break 
            
        if flag == True:
            break

        temp[idx]+=1
        
         
    sol.sort()

   

    if r-1 < len(sol):
        for i in range(n):
            print(sol[r-1][i], end=" ")
    else:
        print("NONE")    
if __name__ == "__main__":
    main()
