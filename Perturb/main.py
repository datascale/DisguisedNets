import math
import sys
import time
import numpy as np
import pandas as pd
from general import Data_All,Data_Arr,TransProp
from perturb_mat import PerturbMat
from perturb_pixels import PerturbPix

class PerturbData:
    def __init__(self,data_train,data_test,rot_keys,perm_keys,trans_prop):
        self.t_p = trans_prop
        np_data_train=data_train
        np_data_test=data_test
        self.rot_keys=rot_keys
        self.shuffle_arr = perm_keys
        self.action = 'permute' if trans_prop.rot_type =='permutation' else 'rot+pert'
        self.pert_train_pixels,self.y_train=self._transform(np_data_train)
        self.pert_test_pixels=self._transform(np_data_test)
        
    def write2file(self,header_lbl='pixel'):
        self._write2file(self.pert_train_pixels,self.y_train,header_lbl)
        self._write2file(self.pert_test_pixels,[],header_lbl)

    def _transform(self,np_data):
        perturbed_pixels=[]
        y = []
        for pixels in np_data.as_np_arrays:
            pixels_in = pixels[np_data.data_type:]
            rotated_pixel=PerturbPix(pixels_in,self.rot_keys,self.t_p.image_size,self.t_p.block_size,self.shuffle_arr,self.action,self.t_p.noise_level)
            pxs = rotated_pixel.pert_pixels
            perturbed_pixels.append(pxs)
            if np_data.data_type ==1:
                y.append(pixels[0])
        if np_data.data_type==1:
            y = [int(i) for i in y]
            return perturbed_pixels,y
        else:
            return perturbed_pixels

    def _write2file(self,prtb_data,y=[],header_lbl="pixel"):
        headerc =[header_lbl+str(i) for i in range(len(prtb_data[0]))]
        data = pd.DataFrame(prtb_data, columns=headerc)
        data_type = "test"
        if len(y) == len(prtb_data):
            data.insert(0,'label',y)
            data_type = "train"
        data.to_csv('mnist_%s_%s_%s_%s.csv'%(data_type,self.t_p.noise_level,self.t_p.block_size[0],self.t_p.block_size[1]),sep=',',index=False)


def main():
    np.set_printoptions(threshold=np.nan)
    f_name = sys.argv[1]
    image_size=(int(sys.argv[2]),int(sys.argv[3]))
    block_size=(int(sys.argv[4]),int(sys.argv[5]))
    data_train=Data_All(f_name+'_train.csv',image_size)
    data_test=Data_All(f_name+'_test.csv',image_size,0)
    noise_expansion = float(sys.argv[6])
    rot_type = sys.argv[7]
    trans_prop = TransProp(image_size,block_size,rot_type,noise_expansion)
    #trans_prop.print_params()
    
    rot_keys=PerturbMat(trans_prop.image_size,trans_prop.block_size,trans_prop.rot_type).Rot_mat
    shuffle_arr=np.arange(trans_prop.count_sub_mats)

    #if trans_prop.rot_type =='permutation':
    np.random.shuffle(shuffle_arr)
    start_pert_time = time.time()
    d1=PerturbData(data_train,data_test,rot_keys,shuffle_arr,trans_prop)
    end_pert_time = time.time()
    f = open('time_transf.csv','a')
    #print >>f, str(end_pert_time - start_pert_time)
    d1.write2file()

if __name__=="__main__":
    main()
