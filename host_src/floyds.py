import numpy as np
import csv

def addturnweights(mat):
    turn90 = 10 #distance equivalent of turn 90degrees
    turn180 = 20 # '' ''
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == -1:
                mat[i][j] = turn90
            elif mat[i][j] == -2:
                mat[i][j] = turn180
    return mat

def zerotoinfinity(mat):
    #turns 0s in matrix to infinity
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == 0:
                mat[i][j] = 10**7
    return mat


def getweightsmatrix(inputfile='src/weights.csv'):
    #turns csv into 2x2 matrix
    weights = []

    with open(inputfile, 'r') as csv1:
        reader = csv.reader(csv1)
        for row in reader:
            weights.append(row)

    weights = [[int(element) for element in row] for row in weights]
    return weights

x= zerotoinfinity(addturnweights(getweightsmatrix('src/testweights.csv'))) #change testweights to weights

def floydWarshall(graph,V):
    for k in range(V-1):
        for i in range(V-1):
            for j in range(V-1):
                if ((graph[i][j] == -1 or 
                    graph[i][j] > (graph[i][k] + graph[k][j]))
                    and (graph[k][j] != -1 and graph[i][k] != -1)):
                    graph[i][j] = graph[i][k] + graph[k][j]
    return graph


