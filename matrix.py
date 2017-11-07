import stars_data
import math

class Model3D:
    def __init__(self, stars_data):
        self.stars_data = stars_data

class Matrix:
    def __init__(self, height, width, m):
        if m is None:
            self.height = height
            self.width = width
            row = [0 for x in range(0, width)]
            self.m = [row for x in range(0, self.height)]
        elif type(m) is list:
            self.m = m
            self.height = len(m)
            self.width = len(m[0])

    def getValue(self, x, y):
        return self.m[x][y]

    def setValue(self, x, y, value):
        self.m[x][y] = value

    def __mul__(self, other):
        if type(other) is not Matrix:
            return

        new_matrix = Matrix(None, None, matrix_mult(self.m, other.m))

        return new_matrix

def matrix_mult(m1,m2):
    s=0     #сумма
    t=[]    #временная матрица
    m3=[] # конечная матрица
    if len(m2)!=len(m1[0]):
        print("Матрицы не могут быть перемножены")
    else:
        r1=len(m1) #количество строк в первой матрице
        c1=len(m1[0]) #Количество столбцов в 1
        r2=c1           #и строк во 2ой матрице
        c2=len(m2[0])  # количество столбцов во 2ой матрице
        for z in range(0,r1):
            for j in range(0,c2):
                for i in range(0,c1):
                   s=s+m1[z][i]*m2[i][j]
                t.append(s)
                s=0
            m3.append(t)
            t=[]
    return m3