#include <stdio.h>
#include <stdlib.h>


int C, N;
int main(void) {
    scanf("%d", &C);
    for (int t = 0; t < C; t++) {
        scanf("%d", &N);
        int cnt = 0;
        double avg = 0;
        int * score = (int *) malloc(sizeof(int) * N);
        for (int i = 0; i < N; i++) {
            scanf("%d", &score[i]);
            avg += score[i];
        }
        avg /= N;
        for (int i = 0; i < N; i++) {
            if (score[i] > avg) cnt++;
        }
        printf("%.3lf%%\n", (double) cnt / N * 100);
        
    }
    return 0;
}


// printf("%.3lf%%", answer);
