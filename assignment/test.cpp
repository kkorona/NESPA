#include <iostream>
#include <vector>
using namespace std;

vector < vector < int > > board(102, vector<int>(102,0));
vector < int > paper(102,0);
bool boundary(int lo,int tar,int hi) {
    return lo <= tar && tar < hi;
}
int main()
{

    int N;
    cin >> N;

    for(int k=1; k<=N; k++) {
        int y,x,w,l;
        cin >> y >> x >> w >> l;
        for(int i=y; i<y+w; i++) {
            for(int j=x; j<x+l; j++) {
                board[i][j]=k;
            }
        }
    }

    for(int i=0; i<=101; i++) {
        for(int j=0; j<=101; j++) {
            paper[board[i][j]]++;
        }
    }

    for(int i=1; i<=N; i++) {
        cout << paper[i] << " ";
    }
    return 0;
}