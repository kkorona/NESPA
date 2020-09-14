coord = []
face = True
class Robot:
    def __init__(self, x, y, direct:str):
        self.direct = direct
        self.now_coord = [x, y]
        for i, c in enumerate(coord):
            if c == self.now_coord:
                self.now_index = i
        
    def move(self): # 1씩 움직인다고 가정
        if self.direct == '+':
            try:
                self.now_coord = coord[self.now_index+1]
                self.now_index += 1
            except:
                self.now_coord = coord[0]
                self.now_index = 0
        else:
            try:
                self.now_coord = coord[self.now_index-1]
                self.now_index -= 1
            except:
                self.now_coord = coord[len(coord)-1]
                self.now_index = len(coord)-1
    
    def change_direction(self):
        if self.direct == '+':
            self.direct = '-'
        else:
            self.direct = '+'
    
    def __repr__(self):
        return " ".join(map(str, self.now_coord))

def near(A:Robot, B:Robot):
    global face
    if (abs(A.now_index - B.now_index) == 1 or\
         abs(A.now_index - B.now_index) == len(coord)-1) and A.direct != B.direct and face:
        return True
    else:
        return False

def robot_interaction(c1:Robot, c2:Robot, t):
    global face
    for _ in range(t):    
        if c1.now_coord == c2.now_coord:
            c1.change_direction()
            c1.move()
            c2.change_direction()
            c2.move()
            face = False
        elif near(c1, c2):
            c1.change_direction()
            c2.change_direction()
            face = False
        else:
            c1.move()
            c2.move()
            face = True
    print(c1)
    print(c2)

import copy
def coord_list(apex:list):
    global coord
    temp = copy.deepcopy(apex)
    temp.append(temp[0])
    all_coord = []

    for i in range(len(apex)):
        all_coord.append(temp[i])
        if temp[i][0] == temp[i+1][0]:
            for j in range(1, abs(temp[i+1][1] - temp[i][1])):
                if temp[i+1][1] > temp[i][1]:
                    all_coord.append([temp[i][0], temp[i][1] + j])
                else:
                    all_coord.append([temp[i][0], temp[i][1] - j])

        elif temp[i][1] == temp[i+1][1]:
            for j in range(1, abs(temp[i+1][0] - temp[i][0])):
                if temp[i+1][0] > temp[i][0]:
                    all_coord.append([temp[i][0]+j, temp[i][1]])
                else:
                    all_coord.append([temp[i][0]-j, temp[i][1]])    
    
    coord = all_coord

K = int(input())        # K <= 50
apex = []
for i in range(K):
    apex.append(list(map(int, input().split())))
coord_list(apex)

c1 = Robot(coord[0][0], coord[0][1], '+')
c2 = Robot(apex[int(K/2-1)][0], apex[int(K/2-1)][1], '-')
t = int(input())

robot_interaction(c1, c2, t)
