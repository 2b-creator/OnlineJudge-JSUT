#include <iostream>
using namespace std;

int main(int argc, char const *argv[])
{
    int c, d, n;
    cin >> c >> d >> n;
    int sums = 0;
    for (int i = 1; i <= n; i++)
    {
        sums += (c * i + d);
    }
    cout << sums;
    return 0;
}
