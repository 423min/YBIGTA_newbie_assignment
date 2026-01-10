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

    T = int(input())
    for i in range(T):
        n, m = map(int, input().split())
        movie_num = list(map(int, input().split()))

        # 자리 배열: 1이면 영화 있음, 0이면 비어 있음
        arr = [0] * (n + m)

        # 초기 배치
        pos = [0] * (n + 1)
        for i in range(1, n + 1):
            index = m + i - 1
            pos[i] = index
            arr[index] = 1

        st = SegmentTree(arr, lambda a, b: a + b, 0, lambda x: x)

        # 다음에 꺼낸 영화를 올려놓을 인덱스
        top = m - 1

        result = []
        for i in movie_num:
            num = pos[i]
            if num == 0:
                movie_above = 0
            else:
                movie_above = st.query(1, 0, n+m-1, 0, num-1)
            result.append(str(movie_above))

            st.update(num, 0)
            st.update(top, 1)
            pos[i] = top
            top -= 1
        
        print(" ".join(result))

if __name__ == "__main__":
    main()