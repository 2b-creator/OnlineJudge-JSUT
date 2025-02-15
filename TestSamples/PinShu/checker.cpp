#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#define MAX 240
using namespace std;
vector<string> out, ans;
int main(int argc, char *argv[])
{
    // argv[1] => 输入文件
    // argv[2] => 程序输出文件
    // argv[3] => 标准答案文件
    bool flag;
    char c;
    ifstream getout(argv[2]);
    flag = 0;
    out.push_back("");
    while (1)
    {
        while (1)
        {
            c = getout.get();
            if (c == -1)
            {
                flag = 1;
            }
            if (c == '\n' || c == -1)
            {
                out.push_back("");
                break;
            }
            out.back().push_back(c);
        }
        if (flag)
            break;
    }
    for (string &i : out)
        while ((!i.empty()) && (i.back() == ' ' || i.back() == '\t'))
            i.pop_back();
    while ((!out.empty()) && out.back().empty())
        out.pop_back();
    ifstream getans(argv[3]);
    flag = 0;
    ans.push_back("");
    while (1)
    {
        while (1)
        {
            c = getans.get();
            if (c == -1)
            {
                flag = 1;
            }
            if (c == '\n' || c == -1)
            {
                ans.push_back("");
                break;
            }
            ans.back().push_back(c);
        }
        if (flag)
            break;
    }
    for (string &i : ans)
        while ((!i.empty()) && (i.back() == ' ' || i.back() == '\t'))
            i.pop_back();
    while ((!ans.empty()) && ans.back().empty())
        ans.pop_back();
    if (ans.size() != out.size())
        return 0;
    for (int i = 0; i < ans.size(); i++)
    {
        if (ans[i] != out[i])
            return 0;
    }
    return MAX;
}