import numpy as np
import skimage
import random
from skimage import data, io
from skimage.measure import block_reduce
from skimage.transform import warp,rescale,resize
from matplotlib import pyplot as plt


class PolyTransform:
    def __init__(self,matz,poly_degree=2,Poly_Key=[]):
        self.transformed_mat = []
        if len(Poly_Key)==0:
            Poly_Key = PolyClass(matz[0].shape,poly_degree).poly_mat_key

        def downscale_local_max(image, factors, cval=0, clip=True):
            return block_reduce(image, factors, np.max, cval)

        for mat in matz:
            #print mat.shape
            dest_mat = Poly_Key.copy()
            source_mat = mat.copy().flatten()
            for i in range(len(dest_mat)):
                for j in range(len(dest_mat[0])):
                    if dest_mat[i,j]!=0:
                        dest_mat[i,j] = source_mat[int(Poly_Key[i,j])-1]
            sz = Poly_Key.shape
            x_fac = sz[0]/32
            y_fac = sz[1]/32
            dest_mat = downscale_local_max(dest_mat,(x_fac,y_fac))
            dest_mat = resize(dest_mat,(32,32))
            self.transformed_mat.append(dest_mat.flatten())


class PolyClass:
    
    def __init__(self,mat_shape,poly_degree=2, c_cushion=15):
        self.mat_shape = mat_shape
        self.x_coeffs = self._n_l_params()
        self.y_coeffs = self._n_l_params()
        self.c_cushion = c_cushion
        self.poly_degree=poly_degree
        self.poly_mat_key = self.transfm_mat()    

    def _n_l_params(self):
        alpha = random.randint(1,20)
        beta = random.randint(1,20)
        c = random.randint(1,1)
        return alpha,beta,c

    def _new_indx(self,x,y):
        new_x = (self.x_coeffs[0]*x**3 + self.x_coeffs[1]*x**2+random.randint(1,self.c_cushion))
        new_y = (self.y_coeffs[0]*y**3 + self.y_coeffs[1]*y**2+random.randint(1,self.c_cushion))
        return new_x,new_y

    def transfm_mat(self):
        n,k=self.mat_shape
        x_coeffs = self.x_coeffs
        y_coeffs=self.x_coeffs
        k_new_mat,n_new_mat = self._new_indx(k,n)
        new_mat = np.zeros((n_new_mat,k_new_mat))
        Z=[]
        for i in range(n):
            for j in range(k):
                new_x,new_y = self._new_indx(i,j)
                Z.append(list((new_x,new_y)))
        Z = np.array(Z)
        max_x=max(Z[:,0])
        max_y=max(Z[:,1])
        new_mat = np.zeros((max(max_x,max_y)+1,max(max_x,max_y)+1))

        r=1
        s=0
        #mat= mat.flatten()
        count=0
        
        for i,j in Z:
            new_mat[i-1,j-1]=r
            r+=1
            
        shrink_mat = new_mat[~(new_mat==0).all(1)]
        shrink_mat = (shrink_mat.T[~(shrink_mat.T==0).all(1)]).T    
        return shrink_mat

def main():
    
    np.set_printoptions(threshold='nan',linewidth=600)

    n =5
    k = 5
    mat = np.random.randint(0,255,(n,k))
    #print mat
    transformed_mat =PolyTransform([mat],2).transformed_mat
    #print transformed_mat
    
if __name__=='__main__':
    main()
