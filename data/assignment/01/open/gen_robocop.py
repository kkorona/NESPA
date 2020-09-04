#-------------------------------------------------------------------------------
# Purpose:     2020 Prof. Zoh's Work
# Author:      Cho
# Created:     2020-09-01
#-------------------------------------------------------------------------------
import random
import PIL

N= 14             # 꼭지점의 갯수
Mleng = 2000

random.seed( 1734 )

# 8번, 24개 546161
# 7번, 10개, 661

bx = sx = 5000
by = sy = 5000
k = 1

xylist = []
print(N)
while ( k < N ) :
    print( f'{sx} {sy}')
    xylist.extend( [sx, sy] )

    jump = random.randrange(1000, Mleng)
    if random.random( ) < 0.5 :
        jump = - jump

    if ( k%2 == 1 ) : # odd
        sy += jump
    else : # ever
        sx += jump
    k += 1


print( f'{sx} {by}')
xylist.extend( [sx, by] )
xylist.append( xylist[0] )
xylist.append( xylist[1] )

#print("xylist= ", xylist )


xymax = max( xylist)
xymin = min( xylist)

#print("xymax, xymin = ",  xymax, xymin )

from tkinter import *


root = Tk()     # 창을 하나 만듭니다.
root.title(' 자료구조 roboCop 평가데이터 만들기: ')

xyspan = xymax - xymin

N = 800
S = 600
normalxy= [ int( S*(w-xymin)/xyspan)+20 for w in xylist ]
#print( "normalxy = ", normalxy )

mypaper = Canvas(root, width= N, height= N, background="light green")
mypaper.create_line( normalxy, width=2, fill='black' )  # 점찍기
mypaper.create_text(50,50, font=("맑은 고딕",14), fill="blue", text="FILE:" )

mypaper.pack()   # 그려진 것을 꽉 차게 보여준다.
mypaper.postscript(file="file_name.ps", colormode='color')

root.mainloop()

