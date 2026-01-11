from lib import SegmentTree
import sys


"""
TODO:
- 일단 SegmentTree부터 구현하기
- main 구현하기
"""


def main() -> None:
    # 구현하세요!
    input = sys.stdin.readline
    MAX = 1000000

    st = SegmentTree([0] * (MAX + 1), lambda a, b: a + b, 0, lambda x: x)

    def find(B: int, node: int, start: int, end: int) -> int:
        """
        누적 개수를 기준으로 B번째에 해당하는 원소 인덱스 찾기
        
        :param B: 꺼낼 사탕의 순위
        :type B: int
        :param node: 현재 탐색 중인 segment tree의 노드 인덱스
        :type node: int
        :param start: 현재 노드가 담당하는 구간의 시작 인덱스
        :type start: int
        :param end: 현재 노드가 담당하는 구간의 끝 인덱스
        :type end: int

        :return: B번째에 해당하는 원소의 인덱스
        :rtype: int
        """

        if start == end:
            return start
        
        mid = (start + end) // 2
        left_count = st.tree[node * 2]

        if B <= left_count:
            return find(B, node * 2, start, mid)
        else:
            return find(B - left_count, node * 2 + 1, mid + 1, end)
        

    n = int(input())

    for i in range(n):
        temp = list(map(int, input().split()))
        if temp[0] == 1:
            B = temp[1]
            candy = find(B, 1, 0, MAX)
            print(candy)

            candy_count = st.query(1, 0, MAX, candy, candy)
            st.update(candy, candy_count - 1)

        else:
            B, C = temp[1], temp[2]
            candy_count = st.query(1, 0, MAX, B, B)
            st.update(B, candy_count + C)


if __name__ == "__main__":
    main()