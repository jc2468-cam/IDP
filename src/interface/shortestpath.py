from floyds import x

def initialise(V):
    global dis, Next
 
    for i in range(V):
        for j in range(V):
            dis[i][j] = graph[i][j]
 
            # No edge between node i and j
            if (graph[i][j] == INF):
                Next[i][j] = -1
            else:
                Next[i][j] = j

def constructPath(u, v):
    global graph, Next
    u = u-1
    v = v-1
     
    # If there's no path between node u and v return empty array
    if (Next[u][v] == -1):
        return {}
 
    # Storing the path in a vector
    path = [u+1]
    while (u != v):
        u = Next[u][v]
        path.append(u+1)
 
    return path

def floydWarshall(V):
    global dist, Next
    for k in range(V):
        for i in range(V):
            for j in range(V):
                 
                # can't travel through edge which doesn't exist
                if (dis[i][k] == INF or dis[k][j] == INF):
                    continue
                if (dis[i][j] > dis[i][k] + dis[k][j]):
                    dis[i][j] = dis[i][k] + dis[k][j]
                    Next[i][j] = Next[i][k]
 
def printPath(path):
    n = len(path)
    for i in range(n-1):
        print(path[i], end=" -> ")
    print (path[n - 1])

if __name__ == '__main__':
    MAXM,INF = 2000,10**4
    dis = [[-1 for i in range(MAXM)] for i in range(MAXM)]
    Next = [[-1 for i in range(MAXM)] for i in range(MAXM)]
 
    graph = x
    V = len(graph)-1
 
    # Function to initialise the distance and Next array
    initialise(V)
 
    # Calling Floyd Warshall Algorithm, updates nextand distance array
    floydWarshall(V)
    path = []
 
    print("Shortest path: ", end = "")
    path = constructPath(2,45) # nodes to travel between
    print(path)
 
 
