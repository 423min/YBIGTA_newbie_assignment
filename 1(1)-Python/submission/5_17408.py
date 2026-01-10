from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Callable


"""
TODO:
- SegmentTree 구현하기
"""


T = TypeVar("T")
U = TypeVar("U")


class SegmentTree(Generic[T, U]):
    # 구현하세요!
    def __init__(self, arr: list[T], merge: Callable[[U, U], U], 
                 identity: U, lift: Callable[[T], U]) -> None:
        """
        SegmentTree 객체 초기화하기
        
        :param arr: segment tree를 만들 원본 array
        :type arr: list[T]
        :param merge: 두 자식 노드의 값을 하나의 노드 값으로 합치는 함수
        :type merge: Callable[[U, U], U]
        :param identity: query에서 구간이 겹치지 않을 때 반환되는 항등원
        :type identity: U
        :param lift: 원본 배열 원소를 tree 노드에 저장할 값으로 변환하는 함수
        :type lift: Callable[[T], U]
        """

        self.arr = arr
        self.n = len(arr)

        self.merge = merge
        self.identity = identity
        self.lift = lift

        self.tree: list[U] = [identity] * (4 * self.n + 5)

        if self.n > 0:
            self.build(1, 0, self.n - 1)
    

    def build(self, node: int, left: int, right: int) -> None:
        """
        원본 array를 기반으로 segment tree의 모든 노드 값을 재귀적으로 채우기
        
        :param node: 현재 tree에서 처리 중인 노드의 인덱스
        :type node: int
        :param left: 현재 노드가 담당하는 구간의 시작 인덱스
        :type left: int
        :param right: 현재 노드가 담당하는 구간의 끝 인덱스
        :type right: int
        """

        if left == right:
            self.tree[node] = self.lift(self.arr[left])
            return
        
        mid = (left + right) // 2
        new_left = node * 2
        new_right = node * 2 + 1

        self.build(new_left, left, mid)
        self.build(new_right, mid + 1, right)
        self.tree[node] = self.merge(self.tree[new_left], self.tree[new_right])
    

    def query(self, node: int, start: int, end: int, left: int, right: int) -> U:
        """
        지정된 구간 [left, right]에 대한 query 결과를 반환하기
        
        :param node: 현재 tree에서 처리 중인 노드의 인덱스
        :type node: int
        :param start: 현재 노드가 담당하는 구간의 시작 인덱스
        :type start: int
        :param end: 현재 노드가 담당하는 구간의 끝 인덱스
        :type end: int
        :param left: 조회할 구간의 시작 인덱스
        :type left: int
        :param right: 조회할 구간의 끝 인덱스
        :type right: int

        :return: 구간 [left, right]에 대한 query 결과
        :rtype: U
        """

        # 노드가 지정된 범위 밖에 있는 경우
        if right < start or end < left:
            return self.identity
        
        # 노드가 지정된 범위 안에 있는 경우
        if left <= start and end <= right:
            return self.tree[node]
        
        # 일부만 겹치는 경우
        mid = (start + end) // 2
        left_child = self.query(node * 2, start, mid, left, right)
        right_child = self.query(node * 2 + 1, mid + 1, end, left, right)
        return self.merge(left_child, right_child)
    

    def update(self, index: int, value: T, node: int = 1, start: int = 0, end: Optional[int] = None) -> None:
        """
        특정 인덱스의 값을 갱신하고 관련된 segment tree의 노드들을 재계산하기
        
        :param index: 값을 변경할 array의 인덱스
        :type index: int
        :param value: 변경할 새로운 값
        :type value: T
        :param node: 현재 tree에서 처리 중인 노드의 인덱스
        :type node: int
        :param start: 현재 노드가 담당하는 구간의 시작 인덱스
        :type start: int
        :param end: 현재 노드가 담당하는 구간의 끝 인덱스
        :type end: Optional[int]
        """
        if end is None:
            end = self.n - 1

        if start == end:
            self.tree[node] = self.lift(value)
            return
        
        mid = (start + end) // 2
        if index <= mid:
            self.update(index, value, node * 2, start, mid)
        else:
            self.update(index, value, node * 2 + 1, mid + 1, end)

        self.tree[node] = self.merge(self.tree[node * 2], self.tree[node * 2 + 1])


import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


class Pair(tuple[int, int]):
    """
    힌트: 2243, 3653에서 int에 대한 세그먼트 트리를 만들었다면 여기서는 Pair에 대한 세그먼트 트리를 만들 수 있을지도...?
    """
    def __new__(cls, a: int, b: int) -> 'Pair':
        return super().__new__(cls, (a, b))

    @staticmethod
    def default() -> 'Pair':
        """
        기본값
        이게 왜 필요할까...?
        """
        return Pair(0, 0)

    @staticmethod
    def f_conv(w: int) -> 'Pair':
        """
        원본 수열의 값을 대응되는 Pair 값으로 변환하는 연산
        이게 왜 필요할까...?
        """
        return Pair(w, 0)

    @staticmethod
    def f_merge(a: Pair, b: Pair) -> 'Pair':
        """
        두 Pair를 하나의 Pair로 합치는 연산
        이게 왜 필요할까...?
        """
        return Pair(*sorted([*a, *b], reverse=True)[:2])

    def sum(self) -> int:
        return self[0] + self[1]


def main() -> None:
    # 구현하세요!
    input = sys.stdin.readline

    N = int(input())
    A = list(map(int, input().split()))
    M = int(input())

    st = SegmentTree[int, Pair](A, Pair.f_merge, Pair.default(), Pair.f_conv)
    result: list[str] = []

    for i in range(M):
        q = list(map(int, input().split()))
        if q[0] == 1:
            i, v = q[1], q[2]
            A[i-1] = v
            st.update(i-1, v)
        else:
            l, r = q[1], q[2]
            pair = st.query(1, 0, N-1, l-1, r-1)
            result.append(str(pair.sum()))
    
    print("\n".join(result))


if __name__ == "__main__":
    main()