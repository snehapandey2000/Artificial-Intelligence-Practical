v = [[] for i in range(100)]


def addEdge(x, y):
    v[x].append(y)
    v[y].append(x)


def printPath(stack):
    for i in range(len(stack) - 1):
        print(stack[i], end=" -> ")
    print(stack[-1])


def DFS(vis, x, y, stack):
    stack.append(x)
    if (x == y):
        printPath(stack)
        return
    vis[x] = True
    if (len(v[x]) > 0):
        for j in v[x]:
            if (vis[j] == False):
                DFS(vis, j, y, stack)
    del stack[-1]


def DFSCall(x, y, n, stack):
    vis = [0 for i in range(n + 1)]
    DFS(vis, x, y, stack)


n = 10
stack = []

addEdge(1, 2)
addEdge(1, 3)
addEdge(2, 4)
addEdge(2, 5)
addEdge(2, 6)
addEdge(3, 7)
addEdge(3, 8)
addEdge(3, 9)

DFSCall(4, 8, n, stack)
