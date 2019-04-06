import numpy as np
import math


class PerturbClass:
    '''generates a Rotation matrix of given dimension and type'''

    def __init__(self, size, matrix_type='orthonormal'):
        self.matrix_type = matrix_type
        self.dim = size
        self.ROT_set()

    def ROT_set(self):
        '''returns a set of rotation matrices'''
        if self.matrix_type == 'orthonormal':
            y = self.generate_orthoMat()
        else:
            y = self.generate_projMat()
        self.ROT_mat = y

    def generate_projMat(self):
        dim = self.dim
        while True:
            a = np.random.rand(dim, dim)
            if (np.linalg.matrix_rank(a) == a.shape[0]):
                return a

    def generate_orthoMat(self):
        dim = self.dim
        random_state = np.random
        H = np.eye(dim)
        D = np.ones((dim, ))
        for n in range(1, dim):
            x = random_state.normal(size=(dim - n + 1, ))
            D[n - 1] = np.sign(x[0])
            x[0] -= D[n - 1] * np.sqrt((x * x).sum())
            # Householder transformation
            Hx = (np.eye(dim - n + 1) - 2. * np.outer(x, x) / (x * x).sum())
            mat = np.eye(dim)
            mat[n - 1:, n - 1:] = Hx
            H = np.dot(H, mat)
            # Fix the last sign such that the determinant is 1
        D[-1] = (-1)**(1 - (dim % 2)) * D.prod()
        # Equivalent to np.dot(np.diag(D), H) but faster, apparently
        H = (D * H.T).T
        H = np.matrix(H)
        return H


def main():
    mat = PerturbClass(5, 'orthonormal').ROT_mat
    mat_inverse = np.linalg.inv(mat)

if __name__ == "__main__":
    main()

