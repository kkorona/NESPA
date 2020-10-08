#include <stdio.h>     // fopen, fscanf, fclose 함수가 선언된 헤더 파일
int num1, bcount, people[10][1000],eqs,total;

int init = 0;
int arr3[1000] = {0,};

void fusion(int arr1[],int arr2[]){

    for(int i = 0;i<1000;i++){
        arr3[i] = arr1[i] + arr2[i];
    }



}

void read_data() {
    scanf("%d",&eqs);
    int temp = 0;
    while(scanf("%d",&num1)!=EOF) {
            if (bcount > 0){
                //printf("hangs %d bcount = %d\n",num1,bcount);
                if ( bcount % 2 == 0) temp = num1;
                else people[init][num1] = temp;
                bcount = bcount - 1;


            }
            else {
                bcount = num1*2;
                //printf("init %d\n",init);
                init = init +1;
            }
    }  //end of while()
}


int main() {
    read_data();
    for(int j = 1; j<init+1;j++){
            fusion(people[j],arr3);
    }
    int countt = 0;
    for(int i =1000;i>=0;i--) {if (arr3[i]!=0) countt++; }
    if (countt > 0) printf("%d",countt);

    for(int i =1000;i>=0;i--) {
        if (arr3[i]!=0){
        printf("\n%d %d",arr3[i],i);
        }
    }
    if (countt == 0 ) {printf("%d\n%d %d",1,0,0);}


}


