from __future__ import annotations
import copy


"""
TODO:
- __setitem__ 구현하기
- __pow__ 구현하기 (__matmul__을 활용해봅시다)
- __repr__ 구현하기
"""


class Matrix:
    MOD = 1000

    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix = matrix

    @staticmethod
    def full(n: int, shape: tuple[int, int]) -> Matrix:
        return Matrix([[n] * shape[1] for _ in range(shape[0])])

    @staticmethod
    def zeros(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(0, shape)

    @staticmethod
    def ones(shape: tuple[int, int]) -> Matrix:
        return Matrix.full(1, shape)

    @staticmethod
    def eye(n: int) -> Matrix:
        matrix = Matrix.zeros((n, n))
        for i in range(n):
            matrix[i, i] = 1
        return matrix

    @property
    def shape(self) -> tuple[int, int]:
        return (len(self.matrix), len(self.matrix[0]))

    def clone(self) -> Matrix:
        return Matrix(copy.deepcopy(self.matrix))

    def __getitem__(self, key: tuple[int, int]) -> int:
        return self.matrix[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: int) -> None:
        """
        (행, 열) 인덱스 위치에 값 설정하기
        
        :type key: tuple[int, int] (행, 열) 인덱스를 나타내는 튜플
        :param value: 해당 위치에 저장할 값
        :type value: int
        """
        self.matrix[key[0]][key[1]] = value

    def __matmul__(self, matrix: Matrix) -> Matrix:
        x, m = self.shape
        m1, y = matrix.shape
        assert m == m1

        result = self.zeros((x, y))

        for i in range(x):
            for j in range(y):
                for k in range(m):
                    result[i, j] += self[i, k] * matrix[k, j]

        return result

    def __pow__(self, n: int) -> Matrix:
        """
        분할 정복으로 행렬의 거듭제곱 계산하기
        
        :param n: 거듭제곱 지수
        :type n: int
        :return: 현재 행렬의 n제곱 결과 행렬
        :rtype: Matrix
        """
        x, m = self.shape
        assert x == m

        result = self.eye(x)
        base = self

        while n > 0:
            if n % 2 == 1:
                result = result @ base
                for i in range(x):
                    for j in range(x):
                        result[i, j] %= Matrix.MOD
            base = base @ base
            for i in range(x):
                for j in range(x):
                    base[i, j] %= Matrix.MOD
                    
            n //= 2
        
        return result
       

    def __repr__(self) -> str:
        """
        행렬을 문자열 형태로 표현하여 반환
        :return: 행렬의 문자열 표현
        """
        lines: list[str] = list(' '.join(map(str, row)) for row in self.matrix)
        result: str = '\n'.join(lines)
        return result