import numpy as np
from fractions import Fraction
import copy

Index = int


class Simplex:
    def __init__(self, matrix: np.ndarray[np.ndarray[int|float|Fraction]]):
        self.matrix = matrix.astype(Fraction)
        self.n = matrix.shape[1]-1
        self.m = matrix.shape[0]-1
        self.current_x = np.array(range(self.n-self.m+1,self.n+1))
        self.current_state = np.zeros(self.m)
        
    def print(self) -> None:
        print("",*range(1,self.n+1),sep="\t", end="\t")
        print("B")
        for i,x in enumerate(list(self.current_x) + ["Z"]):
            print(x, *self.matrix[i], self.current_state[i] if i < self.m else "", sep="\t")
        
    def find_min(self) -> Index|None:
        return np.argmin(self.matrix[-1])
        
    def resolving_element(self) -> tuple[Index,Index]|None:
        if (col_index:= self.find_min()) is None:
            return None, None
        a = []
        for row in self.matrix:
            if (row[-1] > 0 and row[col_index] > 0) and Fraction(row[-1],row[col_index]) > 0:
                a.append(Fraction(row[-1],row[col_index]))  
            else:
                a.append(np.inf)
        self.current_state = np.array(a)
        if np.all([i>=np.inf for i in self.current_state]):
            return None, None
        return (np.argmin(self.current_state),col_index)
    
    def step(self) -> bool:
        (n,m) = self.resolving_element()
        self.print()
        if n is None or np.all(self.matrix[-1][:-1] >= 0):
            return False
        previous_matrix = copy.deepcopy(self.matrix)
        self.current_x[n] = m+1 
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                if j == m and i != n:
                    self.matrix[i,j] = Fraction(0)
                elif previous_matrix[n,m] == 0:
                    self.matrix[i,j] = Fraction(0)
                elif i == n:
                    self.matrix[i,j] = Fraction(previous_matrix[i,j], previous_matrix[n,m])
                else:
                    self.matrix[i,j] = Fraction(previous_matrix[n,m] * previous_matrix[i,j] - previous_matrix[i,m] * previous_matrix[n,j], previous_matrix[n,m])
        return True