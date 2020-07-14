"""
Simple graph implementation
"""
from queue import Queue
from util import Stack


class Graph:
    """
    Represent a graph as a dictionary of
    vertices mapping labels to edges.
    """
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
        return

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        self.vertices[v1] = self.vertices[v1].union({v2})
        return

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return list(self.vertices[vertex_id])

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = Queue()
        q.put(starting_vertex)
        visited = set()

        while not q.empty():
            cur = q.get()
            if cur not in visited:
                print(cur)
            visited = visited.union({cur})

            for v in self.vertices[cur]:
                if v not in visited:
                    q.put(v)

        return

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = Stack()
        s.push(starting_vertex)
        visited = set()

        while s.size() != 0:
            cur = s.pop()
            if cur not in visited:
                print(cur)
            visited = visited.union({cur})

            for v in self.vertices[cur]:
                if v not in visited:
                    s.push(v)

        return

    def dft_recursive(self, starting_vertex, visited=set()):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if starting_vertex in visited:
            return visited
        else:
            print(starting_vertex)
            visited = visited.union({starting_vertex})
            for v in self.vertices[starting_vertex]:
                visited = self.dft_recursive(v, visited=visited)

        return visited

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = Queue()
        parent_q = Queue()
        q.put(starting_vertex)
        parent_q.put(starting_vertex)
        visited = set()
        paths = {}
        parent = None
        child_count = len(self.vertices[starting_vertex])

        while not q.empty():
            child_count -= 1
            cur = q.get()
            visited = visited.union({cur})
            if parent:
                paths[cur] = list(paths[parent])
                paths[cur].append(cur)
            else:
                paths[cur] = [cur]

            if cur == destination_vertex:
                return paths[cur]

            for v in self.vertices[cur]:
                if v not in visited:
                    parent_q.put(v)
                    q.put(v)

            if child_count == 0:
                parent = parent_q.get()
                child_count = len(self.vertices[parent])

        return paths[cur]

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = Stack()
        s.push(starting_vertex)
        visited = set()
        paths = {}
        parent = None

        while s.size() > 0:
            cur = s.pop()
            visited = visited.union({cur})
            if parent:
                paths[cur] = list(paths[parent])
                paths[cur].append(cur)
            else:
                paths[cur] = [cur]

            if cur == destination_vertex:
                return paths[cur]

            for v in self.vertices[cur]:
                if v not in visited:
                    s.push(v)

            parent = cur

        return paths[cur]

    def dfs_recursive(self, starting_vertex, destination_vertex,
                      parent=None, paths={}):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        if parent is None:
            paths[starting_vertex] = [starting_vertex]
            parent = starting_vertex
        else:
            paths[starting_vertex] = list(paths[parent]) 
            paths[starting_vertex].append(starting_vertex)
            parent = starting_vertex

        for n in self.vertices[starting_vertex]:
            if n not in paths:
                self.dfs_recursive(n, destination_vertex, parent, paths)

        if destination_vertex in paths:
            return paths[destination_vertex]
        



if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
