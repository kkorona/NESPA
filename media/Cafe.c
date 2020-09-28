#include <stdio.h>

int main(void)
{
	int n, k, i, an, bn, x, y, j;
	scanf("%d %d", &n, &k);
	int a[n];
	for (int i = 0;i < n;i++)
	{
		a[i] = 0;
	}
	j = k;
	while (k--)
	{
		scanf("%d", &i);
		if (a[i-1] == i)
		{
			a[i-1] = 0;
			continue;
		}
		a[i-1] = i;
		an = i;
		bn = i - 2;
		if (i == n)
			an = 0;
		if (i == 1)
			bn = n - 1;
		while (an < n)
		{
			if (a[an] != 0) {
				x = a[an];
				an = 0;
				break;
			} else if (an == n-1 && a[an] == 0){ 
				an = 0;
			} else {
				an++;
			}
		}
		while (bn >= 0)
		{
			if (a[bn] != 0){
				y = a[bn];
				bn = 0;
				break;
			} else if (bn == 0 && a[bn] == 0){
				bn = n-1;
			} else {
				bn--;
			}
		}
		printf("%d %d %d\n", i, y, x);
	}
	
	return 0;
}
