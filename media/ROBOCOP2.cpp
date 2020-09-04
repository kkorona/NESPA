#include <iostream>
#include <cmath>
using namespace std;

#define pair<int,int> pii

int get_distance(pii A, pii B) {
    return abs(A.first - B.first) + abs(A.second - B.second);
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    
    int N, sum=0;
    
    cin >> N;
    
    vector < pair < int,int > > P(N);
    vector < int > distance(N,0);
    
    for(int i=0; i<N; i++) {
        cin << P[i].first << P[i].second;
        if(i > 0) {
            distance[i-1] = get_distance(P[i], P[i-1]);
            sum += 
        }
    }
    sum += distance(P[0], P[N-1]);
    
    for(int i=0; i<5; i++) {
        int time;
        cin >> time;
        pii ans = P[0];
        int idx = 0;
        while(time>0) {
            if(
        }
        
        cout << ans.first << ans.second << "\n";
    }
    
    return 0;
}