#include <stdio.h>     // fopen, fscanf, fclose 함수가 선언된 헤더 파일
#include <stdlib.h>
int ini,num1;
int time,xis[100],yis[100];
int count,xcount,ycount;




int *cop1_out,*cop2_out;
int cop1[2],cop2[2];
int ans1,ans2;

void read_data() {
    count = xcount = ycount  = 0;
    int lines;
    scanf("%d",&lines);
    ini = lines;
    while(scanf("%d",&num1)!=EOF) {
        if (count <= lines*2) {
            if (count%2) {
                yis[xcount] = num1;
                xcount = xcount + 1;
            } else {
                xis[ycount] = num1;
                ycount = ycount + 1;
            }
            count = count + 1;
        } // end of if to determine x,y axis
        if (count > lines*2)    time = num1;
    }  //end of while()

} //end of read_data()

int t_dis = 0;
int xy_mid = 0;
int x_mid;
void ft() {
    for(int p = 0; p < ini-1; p++) {
        int x1,x2,y1,y2;
        x1 = xis[p]; x2 = xis[p+1];y1 = yis[p];y2 = yis[p+1];
        if (x1 != x2) t_dis = t_dis + abs(x1-x2);
        if (y1 != y2) t_dis = t_dis + abs(y1-y2);

    }
    t_dis = t_dis + abs(xis[0] -xis[ini-1])+ abs(yis[0] -yis[ini-1]);
    for(int p = 0; p < (ini/2)-1; p++) {
        int x1,x2,y1,y2;
        x1 = xis[p]; x2 = xis[p+1];y1 = yis[p];y2 = yis[p+1];
        if (x1 != x2) xy_mid = xy_mid + abs(x1-x2);
        if (y1 != y2) xy_mid = xy_mid + abs(y1-y2);
    }


}

int step(int x1,int x2) {
    if (x1 != x2) {
        if (x1 < x2) return  x1 +1;
        else return  x1 -1;
    } //end of if

} // end of int step


int *walker(int time,int locate[]) {
    int xc = 1;
    int x1,x2,y1,y2;
    x1 = xis[0]; y1 = yis[0];
    for(int i = 0;i<time;i++){
        x2 = xis[xc]; y2 = yis[xc];
        if(x1 != x2) {if (y1 == y2) x1 = step(x1,x2);}
        if(x1 == x2) {if  (y1 != y2) y1 = step(y1,y2);}
        if(x1 == x2) {if (y1==y2) xc = xc + 1;}
        if(x1 == xis[ini-1]) { if(y1 == yis[ini-1]) xc = 0;}
    }
    locate[0] = x1;locate[1] = y1;
    return locate;

} // end of walker

int *cop1_out,*cop2_out,cop1[2],cop2[2];
int patrol,subtime;

void ans() {
    x_mid = xy_mid/2;
    if (xy_mid%2 == 0) {patrol = t_dis/2;}
    else {patrol = t_dis/2-1;}

    if (time<=x_mid) ans1 = time; //여기 까지는 아무 문제 없음

    else {
        subtime = (time-x_mid)%(patrol*2);
        if (subtime >= patrol) {ans1 = t_dis-(patrol*2-subtime)+x_mid;}
        else {ans1 = t_dis-subtime+x_mid;}
    }
    ans2 = xy_mid+t_dis-ans1;

}

void echoback(){

    //printf("\n t_dis %d",t_dis);
    //printf("\n patrol %d",patrol);
    //printf("\n subtime %d",subtime);
    //printf("\n x_mid %d",x_mid);
    //printf("\n ans1 ans2 %d %d",ans1, ans2);
    printf("%d %d ",*(cop1_out+0),*(cop1_out+1));
    printf("\n%d %d ",*(cop2_out+0),*(cop2_out+1));

}




int main() { // drive routine
    read_data();
    ft();
    ans();
    cop1_out = walker(ans1,cop1);
    cop2_out = walker(ans2,cop2);
    echoback();

} // end of main
