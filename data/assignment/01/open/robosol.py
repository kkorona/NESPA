#-------------------------------------------------------------------------------
# Purpose:     2020 Prof. Zoh's Work
# Author:      Cho
# Created:     2020-09-03
#-------------------------------------------------------------------------------

#fname = input("Input file name: ")

seglist=[]   # segment 길이  list
xylist =[]   # 좌표  list
Sflag = []   # 시작 방향


fname = "openin01.txt"
fin   = open( fname, "r")

def getpos( T ) : # 위치좌표 구하기
    grow = 0
    L = len( seglist )
    for (i,w) in enumerate(seglist) :
        if grow + abs(w) >= T :
            gap = T - grow
            break
        else : grow += abs(w)
    print( " Stop=", i, "gap=", gap)

    if Sflag[i] == 0 : # 세로축 방향
        px = xylist[i][0]
        if w < 0 :  py = xylist[i][1] - gap
        else :      py = xylist[i][1] + gap
    else :  # 가로축 방향
        py = xylist[i][1]
        if w < 0 :  px = xylist[i][0] - gap
        else :      px = xylist[i][0] + gap

    return (px, py)


def verify( plist ) :
    L = len(plist)
    if( L%2 == 1 ) :
        print("error: line segment odd error")
        exit
    if ( plist[0][0] == plist[1][0] )  :
          flag = 0
    elif ( plist[0][1] == plist[1][1] ) : flag = 1
    else :
        print("error: xylist format error")
        return(1)
    for idx in range( L ) :
        if ( plist[idx][ flag] != plist[(idx+1)%L][ flag] )  :
            print("Error", idx )
            return(1)
        flag = (flag+1)%2
    return(0)
# ---------- end of verify -----------

def perimeter( plist ) :
    tperi = 0
    L = len(plist)
    if ( plist[0][0] == plist[1][0] )  :
          flag = 0
    elif ( plist[0][1] == plist[1][1] ) : flag = 1 ;
    else :
        print("error: xylist format error")
        return(1)
    for idx in range( L ) :
        lenseg = ( plist[(idx+1)%L][ (flag+1)%2] -  plist[idx][ (flag+1)%2] )
        seglist.append( lenseg )
        Sflag.append( flag )
        tperi += abs(lenseg)
        #print( f' lenseg = { lenseg}, tperi={tperi} ')
        flag = (flag+1)%2

    if ( sum( [abs(w) for w in seglist ] )  != tperi ) :
        print("Error: 둘레 측정 오류")

    return( seglist, tperi )
# --------------- perimeter( ) ----------



N = int( fin.readline() )
print(N, N*100)


for w in range(N) :
    xylist.append( list(map(int, fin.readline().split())) )

print( xylist )
if ( verify( xylist) == 1 ) :
        print("error: LIne segment error")
        exit
else :
    print(">> line segment 입력오류 없음")

tlist = list(map(int, fin.readline().split()))
if( len(tlist) != 5 ) :
    print("Time point Error")
    exit
else : print( ">> 시간 오류없음 ", tlist )

seglist, allperi = perimeter( xylist )
print(f' Total perimeter = {allperi}')

Final=[]
for tw in tlist :
    realt = tw%allperi
    x,y = getpos( realt )
    print( f' real={realt} pos={x,y} \n')
    Final.append([x,y])

print("\n  Result  \n" )
for w in Final :
    print(f' {w[0]}  {w[1]}')


fin.close()