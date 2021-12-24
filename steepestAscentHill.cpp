#include <bits/stdc++.h>
using namespace std;

int totalDistanceOf(vector<int> &solution, int solSize, vector<vector<int>> &a, int n, int s)
{
    // cout << "Distance calculator/n";
    // store current Path weight(cost)
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
    cout << s << " --> ";
    for (auto x : a)
        cout << x << " --> ";
    cout << s;
}
//to be completed
int travllingSalesmanProblem(vector<vector<int>> &a, int n, int s)
{
    // cout << "start 1" << endl;
    // store all vertex except source vertex
    cout << "\nStarting from a random solution\n\n";
    vector<int> solution;
    for (int i = n - 1; i >= 0; i--)
    {
        if (i != s)
            solution.push_back(i);
    }
    print(solution, s);
    int solSize = solution.size();
    int minPathDistance = totalDistanceOf(solution, solSize, a, n, s);
    cout << "    :   Distance is ";
    cout << minPathDistance << "\n\n";

    while (1)
    {
        // cout << "start 2" << endl;
        int minPathTemp = INT_MAX;
        vector<int> minPathVector;

        cout << "------------------------------\n\n";
        cout << "\nCurrent solution : \n";
        print(solution, s);
        cout << "    :   Distance is ";
        cout << minPathDistance << "\n\n";
        vector<int> nextLevel;
        int flag = 0;
        for (int i = 0; i < solSize; i++)
        {
            // cout << "start 3" << endl;

            for (int j = i + 1; j < solSize; j++)
            {
                // cout << "start 4" << endl;
                // cout << "\nCurrent solution : \n";
                // print(solution, s);

                swap(solution[i], solution[j]);
                cout << "A solution in next level : \n";
                print(solution, s);
                int newPathDistance = totalDistanceOf(solution, solSize, a, n, s);
                cout << "    :   Distance is ";
                cout << newPathDistance << "\n\n";
                nextLevel.push_back(newPathDistance);
                if (newPathDistance < minPathTemp)
                {
                    //move to next solution
                    // flag = 1;
                    // cout << "This new path distance " << newPathDistance << " is smaller than current distance " << minPathDistance << endl;
                    // cout << "So we move on to this solution. Hence we moved to next level.";
                    minPathTemp = newPathDistance;
                    minPathVector = solution;
                    // cout << endl
                    //  << endl;
                }
                else
                {
                    // cout << "This new path " << newPathDistance << " is NOT smaller than current distance " << minPathDistance << endl;
                    // cout << "So we skip this solution and move on to next solution in the same level.";
                    // cout << endl
                    //  << endl;
                }
                swap(solution[i], solution[j]);

                // cout << "hi123\n";
            }
        }

        cout << "\nAll next level distances are as follows : [ ";
        for (int k = 0; k < nextLevel.size() - 1; k++)
        {
            cout << nextLevel[k] << " , ";
        }
        cout << nextLevel[nextLevel.size() - 1];
        cout << " ]\n";

        cout << "Best(minimum) path distance in the next level : " << minPathTemp << endl
             << endl;

        if (minPathTemp < minPathDistance)
        {
            cout << "This new best path distance " << minPathTemp << " is smaller than current distance " << minPathDistance << endl;
            cout << "So we move on to this solution. Hence we moved to next level.\n\n";
            minPathDistance = minPathTemp;
            solution = minPathVector;
        }
        else
        {
            cout << "\nNo better solution found so stop!!\n\n";
            break;
        }
    }

    cout << "Final path : ";
    print(solution, s);
    cout << endl;
    return minPathDistance;
}

// Driver Code
int main()
{
    int n;
    cout << "Enter num of cities :";
    cin >> n;
    cout << "Enter graph in matrix form :\n";
    vector<vector<int>> a(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cin >> a[i][j];
        }
    }
    int s = 0; //source fixed
    cout << "\nSteepest Ascent Hill climbing\n\n";
    cout << "Minimum distance path = " << travllingSalesmanProblem(a, n, s) << endl;
    return 0;
}

// 4
// 0 10 15 20
// 10 0 35 25
// 15 35 0 30
// 20 25 30 0