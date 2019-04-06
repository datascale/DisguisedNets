import numpy as np
import sys
import math
from perturb_class import PerturbClass


class PerturbMat:
    def __init__(self, image_size, block_size, mat_type='orthogonal'):
        self.matrix = np.matrix(np.random.rand(5, 5))
        self.Rot_mat = []
        n, d = image_size
        self.l, self.m = block_size

        self.count_rot_mat = int(math.ceil((n * d) / (self.l * self.m * 1.0)))

        if mat_type == 'orthogonal':
            self.generate_orthoM()
            #self.generate_projM()
        elif mat_type == 'projection':
            self.generate_projM()
        elif mat_type == 'permutation':
            self.generate_permM()

    def generate_orthoM(self):
        for i in range(self.count_rot_mat):
            x = PerturbClass(self.m).ROT_mat
            self.Rot_mat.append(x)

    def generate_projM(self):
        for i in range(self.count_rot_mat):
            x = PerturbClass(self.m, 'projection').ROT_mat
            self.Rot_mat.append(x)

    def generate_permM(self):
        for i in range(self.count_rot_mat):
            x = np.identity(self.m)
            self.Rot_mat.append(x)


def main():
    p1 = PerturbMat((28, 28), (4, 4), 'permutation')
    #print p1.count_rot_mat
    Z = p1.Rot_mat
    #print len(p1.Rot_mat)
    m1 = np.matrix(np.random.rand(4, 4))
    #print np.matmul(m1,Z[0])
    m2 = np.random.rand(16)
    #print m2
    #print Z[0]
    m3 = m2[Z[0]]
    #print m3


if __name__ == "__main__":
    main()

