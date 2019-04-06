import math
import sys
import time
import numpy as np
import pandas as pd
from perturb_mat import PerturbMat
from perturb_pixels import PerturbPix

class Data_All:
    def __init__(self,f_name,image_size,data_type=1):
        self.as_np_arrays= np.genfromtxt(f_name,delimiter=',',skip_header=1)
        self.count = len(self.as_np_arrays)
        self.n = image_size[0]
        self.d = image_size[1]
        self.data_type=data_type

class Data_Arr:
    def __init__(self,array,image_size,data_type=1):
        self.as_np_arrays= array
        self.count = len(self.as_np_arrays)
        self.n = image_size[0]
        self.d = image_size[1]
        self.data_type=data_type

class TransProp:
    def __init__(self,image_size,block_size,rot_type,noise_expansion=1.0):
        self.image_size = image_size
        self.block_size = block_size
        self.n,self.d = image_size
        self.l = block_size[0]
        self.m = block_size[1]
        self.noise_level = noise_expansion
        self.rot_type = rot_type
        self.count_sub_mats=int(math.ceil((self.n*self.d)/(self.l*self.m*1.0)))

