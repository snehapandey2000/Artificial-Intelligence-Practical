#include <bits/stdc++.h>
using namespace std;

int totalDistanceOf(vector<int> &solution, int solSize, vector<vector<int>> &a, int n, int s)
{

    int currPathDistance = 0;
    currPathDistance += a[s][solution[0]];
    for (int i = 0; i <= (solSize - 2); i++)
    {
        currPathDistance += a[solution[i]][solution[i + 1]];
    }

    currPathDistance += a[solution[solSize - 1]][s];
    return currPathDistance;
}

void print(vector<int> &a, int s)
{
    cout << s << " ";
    for (int i = 0; i < a.size(); i++)
        cout << a[i] << " ";
    cout << endl;
}

int travellingSalesmanProblem(vector<vector<int>> &a, int n, int s)
{

    cout << "\nShowing path from one solution to another\n";
    vector<int> solution;
    for (int i = 0; i < n; i++)
    {
        if (i != s)
            solution.push_back(i);
    }
    print(solution, s);
    int solSize = solution.size();
    int minPathDistance = totalDistanceOf(solution, solSize, a, n, s);
    cout << "Path length = " << minPathDistance << "\n";
    while (1)
    {
        int flag = 0;
        for (int i = 0; i < solSize; i++)
        {
            for (int j = i + 1; j < solSize; j++)
            {

                swap(solution[i], solution[j]);
                int newPathDistance = totalDistanceOf(solution, solSize, a, n, s);
                if (newPathDistance < minPathDistance)
                {
                    //move to next solution
                    minPathDistance = newPathDistance;
                    print(solution, s);
                    cout << "Path length = " << minPathDistance << "\n";
                    flag = 1;
                    break;
                }
                else
                {
                    print(solution, s);
                    cout << "Path length = " << newPathDistance << "\n";
                    cout << "But this path length is not better than current path so we will not choose this"
                         << "\n";
                    swap(solution[i], solution[j]);
                }
            }
            if (flag == 1)
                break;
        }
        if (flag == 0)
        {
            break;
        }
    }

    return minPathDistance;
}

int main()
{
    int n;
    cout << "Enter the number of cities :";
    cin >> n;
    cout << "Enter the connected cities in matrix form :\n";
    vector<vector<int>> a(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cin >> a[i][j];
        }
    }
    int s = 0;
    cout << "Minimum distance path = " << travellingSalesmanProblem(a, n, s) << endl;
    return 0;
}

// 5
// 0 10 12 13 50
// 10 0 15 26 30
// 12 15 0 18 50
// 13 26 18 0 40
// 50 30 50 40 0