import copy
import timeit

optimal = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

class Node:
    def __init__(self, state, father=None, depth=0, heuristic=0):
        self.state = state 
        self.father = father 
        self.depth = depth 
        self.heuristic = heuristic  

    def __eq__(self, other):
        return self.state == other.state

    def __repr__(self):
        return str(self.state)

def findEmpty(state, val=0):
    for i in range(3):
        for j in range(3):
            if state[i][j] == val:
                return i, j
    return None

def parammeter(currState, perfectState): # Manhattan
    dist = 0
    out = 0
    for i in range(3):
        for j in range(3):
            if currState[i][j] == 0: continue
            i2, j2 = findEmpty(perfectState, currState[i][j])
            if i2 != i or j2 != j: out += 1
            dist += abs(i2 - i) + abs(j2 - j)
    return dist + out

def newNode(state, father):
    heuristic = parammeter(state, optimal)
    return Node(state, father, father.depth + 1, heuristic)

def goDown(state):
    l, c = findEmpty(state)
    if l < 2:
        state[l + 1][c], state[l][c] = state[l][c], state[l + 1][c]
    return state

def goUp(state):
    l, c = findEmpty(state)
    if l > 0:
        state[l - 1][c], state[l][c] = state[l][c], state[l - 1][c]
    return state

def goRight(state):
    l, c = findEmpty(state)
    if c < 2:
        state[l][c + 1], state[l][c] = state[l][c], state[l][c + 1]
    return state

def goLeft(state):
    l, c = findEmpty(state)
    if c > 0:
        state[l][c - 1], state[l][c] = state[l][c], state[l][c - 1]
    return state

def children(node):
    currState = node.state
    childrenList = []

    c1 = goUp(copy.deepcopy(currState))
    if c1 != currState:
        childrenList.append(newNode(c1, node))

    c2 = goDown(copy.deepcopy(currState))
    if c2 != currState:
        childrenList.append(newNode(c2, node))

    c3 = goLeft(copy.deepcopy(currState))
    if c3 != currState:
        childrenList.append(newNode(c3, node))

    c4 = goRight(copy.deepcopy(currState))
    if c4 != currState:
        childrenList.append(newNode(c4, node))

    return childrenList

def dfs_with_copy(node, maxDepth):
    stack = [(node, 0)]
    explored = set()

    while stack:
        currNode, depth = stack.pop()

        if currNode.state == optimal:
            return currNode  

        if depth < maxDepth:
            for child in children(currNode):
                if tuple(map(tuple, child.state)) not in explored:
                    explored.add(tuple(map(tuple, child.state)))
                    stack.append((child, depth + 1))
    return None  

def dfsModify(node, maxDepth):
    stack = [(node, 0)]
    explored = set()

    while stack:
        currNode, depth = stack.pop()

        if currNode.state == optimal:
            return currNode

        if depth < maxDepth:
            original_state = copy.deepcopy(currNode.state)
            for child in children(currNode):
                if tuple(map(tuple, child.state)) not in explored:
                    explored.add(tuple(map(tuple, child.state)))
                    stack.append((child, depth + 1))
                currNode.state = original_state
    return None

def idfs(node, maxDepth, use_copy=True):
    for depth in range(maxDepth):
        if use_copy:
            result = dfs_with_copy(node, depth)
        else:
            result = dfsModify(node, depth)
        if result:
            return result
    return None

def compare(firstState, maxDepth):
    copyVersion = timeit.timeit(lambda: idfs(firstState, maxDepth, use_copy = True), number = 1)
    modifyVersion = timeit.timeit(lambda: idfs(firstState, maxDepth, use_copy = False), number = 1)

    print(f"Tempo copiando e editando: {copyVersion}")
    print(f"Tempo modificando no: {modifyVersion}")

firstState = Node([[1, 2, 3], [4, 5, 6], [7, 0, 8]])

compare(firstState, maxDepth = 15)
