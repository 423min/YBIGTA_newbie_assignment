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