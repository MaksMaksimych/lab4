"""Формируется матрица F следующим образом: если в Е количество нулевых элементов в
нечетных столбцах в области 4 больше, чем количество отрицательных  элементов в четных
строках в области 1, то поменять в В симметрично области 2 и 3 местами, иначе В и Е
поменять местами несимметрично. При этом матрица А не меняется.
После чего вычисляется выражение: ((F+A)– (K * F) )*AT .
Выводятся по мере формирования А, F и все матричные операции последовательно"""

import random
import time


def matrix_output(mat):
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:3} ", end='')
        print()
    print()


def mat_x_mat(mat1, mat2):
    mult_result = [[0] * len(mat1) for i in range(len(mat1))]
    for i in range(len(mat1)):
        for u in range(len(mat1)):
            for j in range(len(mat1)):
                mult_result[i][u] += mat1[i][j] * mat2[j][u]
    return mult_result


def transposition(mat):
    transposed_result = [[0] * len(mat) for i in range(len(mat))]
    for i in range(len(mat)):
        for j in range(len(mat)):
            transposed_result[i][j] = mat[j][i]
    return transposed_result


#  Ввод размерности
while True:
    try:
        n = int(input('Введите размерность матрицы - n(от 4 до 50):\n'))
        if 4 <= n <= 50:
            break
        else:
            print('Недопустимая размерность')
    except ValueError:
        print('Недопустимая размерность')

#  Ввод числа k
while True:
    try:
        k = int(input("Введите K (целое число):\n"))
        break
    except ValueError:
        print("Введено некорректное значение")

start = time.time()

#  Создание матрицы А
A = [[random.randint(-10, 10) for j in range(n)] for i in range(n)]
print('Сгенерированная матрица А:')
matrix_output(A)

#  Иницилизация подматриц
ndiv2 = n // 2
B = [[0] * ndiv2 for i in range(ndiv2)]
C = [[0] * ndiv2 for i in range(ndiv2)]
E = [[0] * ndiv2 for i in range(ndiv2)]
D = [[0] * ndiv2 for i in range(ndiv2)]
for i in range(ndiv2):
    for j in range(ndiv2):
        B[i][j] = A[i][j]
        C[i][ndiv2 - 1 - j] = A[i][n - 1 - j]
        D[ndiv2 - 1 - i][j] = A[n - 1 - i][j]
        E[ndiv2 - 1 - i][ndiv2 - 1 - j] = A[n - 1 - i][n - 1 - j]
print("\nПодматрица B:")
matrix_output(B)
print("\nПодматрица C:")
matrix_output(C)
print("\nПодматрица D:")
matrix_output(D)
print("\nПодматрица E:")
matrix_output(E)

#  Транспонированная A
print("\nТранспонированная матрица A:")
matrix_output(transposition(A))

#  Иницилизация матрицы F
F = [[0] * n for i in range(n)]
for i in range(n):
    for j in range(n):
        F[i][j] = A[i][j]

#  Количество нулевых элементов в нечетных столбцах в области 4 в С
area4_res = 0
for i in range(ndiv2):
    for j in range(ndiv2):
        if i >= j and i >= ndiv2 // 2 and i + j >= ndiv2 - 1 and j % 2 == 0 and E[i][j] == 0:
            area4_res += 1

# количество отрицательных  элементов в четных строках в области 1

area1_res = 0
for i in range(ndiv2):
    for j in range(ndiv2):
        if i >= j and i + j <= ndiv2 - 1 and j % 2 == 1 and E[i][j] < 0:
            area1_res += 1

#  Преобразование матрицы F согласно условию
print("\nМатрица F до преобразований:")
matrix_output(F)
if area4_res > area1_res:  # Если верно, то симметрично  меняем 2 и 3 область в B
    for i in range(ndiv2):
        for j in range(ndiv2):
            if i >= j and i + j < ndiv2 - 1:
                replace_b = F[i][j]
                for k in range(ndiv2):
                    for p in range(ndiv2):
                        if k <= p and k + p > ndiv2 - 1 and p - k == j - i:
                            F[i][j] = F[k][p]
                            F[k][p] = replace_b
else:  # Иначе, меняем B и E несимметрично
    for i in range(n - 1, ndiv2 - 1, -1):
        for j in range(n - 1, ndiv2 - 1, -1):
            replace_F = F[i][j]
            if n % 2 == 0:
                F[i][j] = F[i - ndiv2][j - ndiv2]
                F[i - ndiv2][j - ndiv2] = replace_F
            else:
                F[i][j] = F[i - ndiv2 - 1][j - ndiv2 - 1]
                F[i - ndiv2 - 1][j - ndiv2 - 1] = replace_F
ispr = F[ndiv2][ndiv2]
F[n - 1][n - 1] = F[ndiv2][ndiv2]
F[n - 1][n - 1] = ispr
print("\nМатрица F после преобразований:")
matrix_output(F)

kf = [[0] * n for i in range(n)]
sum = [[0] * n for i in range(n)]     # Вспомогательные матрицы
vichit = [[0] * n for i in range(n)]

print("\nЧисло К умноженное на матрицу F: ")
for i in range(n):
    for j in range(n):
        kf[i][j] = F[i][j] * k
        print(f"{kf[i][j]:3} ", end='')
    print()

print("\nСумма матриц F и A: ")
for i in range(n):
    for j in range(n):
        sum[i][j] = A[i][j] + F[i][j]
        print(f"{sum[i][j]:3} ", end='')
    print()

print("\nВычитание двух скобок: ")
for i in range(n):
    for j in range(n):
        vichit[i][j] = sum[i][j] - kf[i][j]
        print(f"{vichit[i][j]:3} ", end='')
    print()

print("\nОкончательный результат: ")
FA = mat_x_mat(vichit, transposition(A))
matrix_output(FA)

finish = time.time()
print(f"Время работы программы: {finish - start} секунд")