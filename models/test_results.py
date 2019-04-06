import pandas as pd
import sys

f_name = sys.argv[1]
actual = pd.read_csv(f_name,sep=',')

predict = pd.read_csv('./submission.csv',sep=',')

#print actual['label']

#print predict['Label']

matches= actual['label'] == predict['Label']

#print matches
print matches[(matches==True)].count()

