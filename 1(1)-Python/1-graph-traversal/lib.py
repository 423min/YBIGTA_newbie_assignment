from __future__ import annotations
import copy
from collections import deque
from collections import defaultdict
from typing import DefaultDict, List, Deque


"""
TODO:
- __init__ 구현하기
- add_edge 구현하기
- dfs 구현하기 (재귀 또는 스택 방식 선택)
- bfs 구현하기
"""


class Graph:
    def __init__(self, n: int) -> None:
        """
        그래프 초기화
        n: 정점의 개수 (1번부터 n번까지)
        """
        self.n = n
        # 구현하세요!
        self.graph: DefaultDict[int, List[int]] = defaultdict(list)

    
    def add_edge(self, u: int, v: int) -> None:
        """
        양방향 간선 추가
        """
        # 구현하세요!
        if 1 <= u <= self.n and 1 <= v <= self.n:
            self.graph[u].append(v)
            self.graph[v].append(u)
        
    
    def dfs(self, start: int) -> list[int]:
        """
        깊이 우선 탐색 (DFS)
        
        구현 방법 선택:
        1. 재귀 방식: 함수 내부에서 재귀 함수 정의하여 구현
        2. 스택 방식: 명시적 스택을 사용하여 반복문으로 구현
        """
        # 구현하세요!
        visited = [0] * (self.n + 1)
        result = []

        def DFS(u: int) -> None:
            """
            DFS (재귀 방식 구현)
            
            :param u: 현재 방문 중인 정점 번호
            :type u: int
            """
            visited[u] = 1
            result.append(u)

            for v in sorted(self.graph[u]):
                if not visited[v]:
                    DFS(v)
        
        DFS(start)
        return result

    
    def bfs(self, start: int) -> list[int]:
        """
        너비 우선 탐색 (BFS)
        큐를 사용하여 구현
        """
        # 구현하세요!
        visited = [0] * (self.n + 1)
        queue: Deque[int] = deque()
        result = []

        visited[start] = 1
        queue.append(start)
        
        while queue:
            u = queue.popleft()
            result.append(u)
            for v in sorted(self.graph[u]):
                if not visited[v]:
                    visited[v] = 1
                    queue.append(v)
        
        return result

    
    def search_and_print(self, start: int) -> None:
        """
        DFS와 BFS 결과를 출력
        """
        dfs_result = self.dfs(start)
        bfs_result = self.bfs(start)
        
        print(' '.join(map(str, dfs_result)))
        print(' '.join(map(str, bfs_result)))
