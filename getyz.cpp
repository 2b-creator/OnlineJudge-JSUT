#include <iostream>
using namespace std;

int count_yz(int n)
{
    int count = 0;
    for (int i = 1; i <= n; i++)
    {
        if (n % i == 0)
        {
            count++;
        }
    }
    return count;
}

int main(int argc, char const *argv[])
{
    int maxs = INT_MIN;
    int maxs_n = 0;
    for (int i = 1; i < 256; i++)
    {
        if (count_yz(i) > maxs)
        {
            maxs = count_yz(i);
            maxs_n = i;
        }
    }
    cout << maxs << " " << maxs_n;

    return 0;
}
