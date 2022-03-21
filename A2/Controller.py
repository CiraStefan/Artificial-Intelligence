from queue import PriorityQueue

#define directions
UP = 0
DOWN = 1
LEFT = 3
RIGHT = 2

#define indexes variations
v = [[-1, 0], [1, 0], [0, 1], [0, -1]]

class Controller:
    def __init__(self, map, drone):
        self._map = map
        self._drone = drone

    def heuristic(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return abs(x1 - x2) + abs(y1 - y2)

    def searchAStar(self, mapM, droneD, initialX, initialY, finalX, finalY):
        g_cost = {node: float('inf') for node in mapM.getNodeList()}
        initialNode = (initialX, initialY)
        finalNode = (finalX, finalY)
        g_cost[initialNode] = 0
        f_cost = {node: float('inf') for node in mapM.getNodeList()}
        f_cost[initialNode] = self.heuristic(initialNode, finalNode)
        childNode = tuple
        aPath = {}
        open_lst = PriorityQueue()
        open_lst.put((self.heuristic(initialNode, finalNode), self.heuristic(initialNode, finalNode), initialNode))

        while not open_lst.empty():
            currNode = open_lst.get()[2]
            if currNode == finalNode:
                break
            for d in (UP, DOWN, LEFT, RIGHT):
                if 0 <= currNode[0] + v[d][0] <= 19 and 0 <= currNode[1] + v[d][1] <= 19:
                    nextNode = (currNode[0] + v[d][0], currNode[1] + v[d][1])
                    if mapM.getSurf()[nextNode[0]][nextNode[1]] != 1:
                        childNode = nextNode
                        temp_g_cost = g_cost[currNode] + 1
                        temp_f_cost = temp_g_cost + self.heuristic(childNode, finalNode)

                        if temp_f_cost < f_cost[childNode]:
                            g_cost[childNode] = temp_g_cost
                            f_cost[childNode] = temp_f_cost
                            open_lst.put((temp_f_cost, self.heuristic(childNode, finalNode), childNode))
                            aPath[childNode] = currNode

        fwdPath = {}
        node = finalNode
        while node is not initialNode:
            fwdPath[aPath[node]] = node
            node = aPath[node]
        return fwdPath
        # pass

    def searchGreedy(self, mapM, droneD, initialX, initialY, finalX, finalY):
        f_cost = {node: float('inf') for node in mapM.getNodeList()}
        initialNode = (initialX, initialY)
        finalNode = (finalX, finalY)
        f_cost[initialNode] = 0
        found = False
        toVisit = PriorityQueue()
        aPath = {}
        visited = []
        toVisit.put((self.heuristic(initialNode, finalNode), initialNode))

        while not toVisit.empty() and not found:
            currNode = toVisit.get()[1]
            visited.append(currNode)
            if currNode == finalNode:
                break

            aux = PriorityQueue()
            for d in (UP, DOWN, LEFT, RIGHT):
                if 0 <= currNode[0] + v[d][0] <= 19 and 0 <= currNode[1] + v[d][1] <= 19:
                    nextNode = (currNode[0] + v[d][0], currNode[1] + v[d][1])
                    if mapM.getSurf()[nextNode[0]][nextNode[1]] != 1 and nextNode not in visited:
                        aux.put((self.heuristic(nextNode, finalNode), nextNode))
                        aPath[nextNode] = currNode

            toAddEl = aux.get()[1]
            toVisit.put((self.heuristic(toAddEl, finalNode), toAddEl))

        fwdPath = {}
        node = finalNode
        while node is not initialNode:
            fwdPath[aPath[node]] = node
            node = aPath[node]
        return fwdPath
