import numpy as np
import math
import sys
from perturb_mat import PerturbMat
#from skimage.transform import rotate, swirl

class PerturbPix:

    def __init__(self,pixels,rot_mats,image_size,block_size,shuffle_arr,action='rot+pert',noise_expansion=1.0):
        self.pixels = pixels.copy()
        self.image_size = image_size
        self.block_size = block_size   
        
        self.rot_mats = rot_mats
        self.n_delta = noise_expansion
        self.pert_key= []

        self.px_as_submats= self._create_sub_mat(self.pixels)

        if action == 'permute':
            #self.pert_pixels_submats= self._permute()
            self.pert_pixels_submats=[self.px_as_submats[x] for x in shuffle_arr]
            self.pert_pixels = self._join_sub_mat(self.pert_pixels_submats)
        elif action =='rot+pert':
            self.rotated_mats=self._rotate()
            self.rotated_mats = [self.rotated_mats[x] for x in shuffle_arr]
            self.rot_pixels=self._join_sub_mat(self.rotated_mats)
            self.pert_pixels=self._perturb()
    

    def _create_sub_mat(self,pixels):
        n,d = self.image_size
        l,m = self.block_size
        submatrices=[]
        pixels=np.matrix(pixels).reshape(n,d)
        count_sub_mat = int(math.ceil((n*d)/(l*m*1.0)))
        r_st=0
        r_end=l
        a = int(d/m)
        b = int(n/l)
        for i in range(b):
            c_st=0
            c_end = m
            for j in range(a):
                subm=pixels[np.ix_(range(r_st,r_end),range(c_st,c_end))]
                submatrices.append(subm)
                c_st+=m
                c_end+=m
            r_st+=l
            r_end+=l
        px_as_submats=submatrices
        return px_as_submats

    def _join_sub_mat(self,submats):
        n,d = self.image_size
        l,m = self.block_size
        big_m=[]
        a = int(d/m)
        b = int(n/l)
        s=0
        for i in range(b):
            sub_m = np.matrix(submats[s]).copy()
            for j in range(a-1):
                sub_m = np.hstack((sub_m,np.matrix(submats[s+j+1].copy())))
            s+=a
            sub_m = sub_m.flatten()
            big_m.append(np.asarray(sub_m))
        return np.asarray(big_m).flatten()
    
    def _rotate(self):
        rotated_mats=[]
        for i in range(len(self.px_as_submats)):
            y = np.matmul(self.px_as_submats[i],self.rot_mats[i])
            rotated_mats.append(y)
        return rotated_mats
    '''
    def _swirl(self):
	rotated_mats=[]
	for i in range(len(self.px_as_submats)):
	    #y =rotate(self.px_as_submats[i],40*(i+1),resize=False)
	    x=[4,8,12,16,20,24,28]
            csv = self.px_as_submats[i]
            for l in x:
                for m in x:
                    csv = swirl(csv,(l,m),strength=10,radius=8)
            rotated_mats.append(csv)
	return rotated_mats
    '''

    def _perturb(self):
        n,d = self.image_size
        dim = n*d
        self.pert_key = np.multiply(np.random.rand(dim),self.n_delta)
        pert_pixels = np.add(self.rot_pixels,self.pert_key)
        #pert_pixels = np.add(self.pixels,self.pert_key)
        return pert_pixels


    def recover(self,rot_type='orthonormal'):
        rotated_twice=[]
        #remove noise and then nix the rotation
        rot_pixels = np.subtract(self.pert_pixels,self.pert_key)
        rotated_mats = self._create_sub_mat(rot_pixels)
        if rot_type=='orthonormal':
            for i in range(len(self.rotated_mats)):
                z = np.round(np.matmul(rotated_mats[i],self.rot_mats[i].T),2)
                rotated_twice.append(z)
        elif rot_type=='projection':
            for i in range(len(self.rotated_mats)):
                z = np.round(np.matmul(rotated_mats[i],np.linalg.inv(self.rot_mats[i])),2)
                rotated_twice.append(z)
        return self._join_sub_mat(rotated_twice).copy()


def main():
    np.set_printoptions(threshold=np.nan)
    np_data = np.genfromtxt('test_test.csv',delimiter=',')
    image_size= (6,6)
    block_size = (3,3)
    

    rot_mats = PerturbMat(image_size,block_size,'projection').Rot_mat
    perm_mats = PerturbMat(image_size,block_size,'permutation').Rot_mat
    
    count_sub_mats = len(rot_mats)
    shuffle_arr = np.arange(count_sub_mats)
    np.random.shuffle(shuffle_arr)
    #print shuffle_arr
    rotated_mats = []
    rotated_again=[]
    for pixels in np_data:
        #print pixels
        rotated_pixel=PerturbPix(pixels,rot_mats,image_size,block_size,shuffle_arr,'rot+pert',100.0)
        #print "rotated pixels"
        #print rotated_pixel.rot_pixels
        #print "perturbed pixels"
        #print rotated_pixel.pert_pixels
        # print "recovered pixels"
        # print rotated_pixel.recover('projection')
        #print perm_mats
        #permuted_pixels= PerturbPix(rotated_pixel.pert_pixels,perm_mats,image_size,block_size,'permute')
        #print permuted_pixels.pert_pixels

if __name__=="__main__":
    main()
