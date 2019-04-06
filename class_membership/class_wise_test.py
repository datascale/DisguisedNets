import sys
import numpy as np
import pandas as pd

test_fname=sys.argv[1]
test_labels=sys.argv[2]

test_set = pd.read_csv(test_fname)
label_df = pd.read_csv(test_labels)

s = label_df['label']
#s = test_set['label']

#comment the following if the test file does not have the labels in it
#test_set = test_set.loc[:,test_set.columns!='label']

for i in range(10):
    t = s[s==i]
    target_indices = t.index.tolist()
    print 'class %s prepared'%i
    target_records = test_set.ix[target_indices]
    #target_records.insert(0,'label',i)
    target_records.to_csv('./datasets/class_subsets/test_class_%s'%i,sep=',',index=None)
