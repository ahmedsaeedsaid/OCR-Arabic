import os
from pre_processing import *
import pandas as pd
directory_list = list()
Y=[]
X=[]
for root, dirs, files in os.walk("punctuation marks", topdown=False):

    for dir_name in dirs:
        url='punctuation marks/'+dir_name+'/'
        for file_name in os.listdir(url):
            Y.append(dir_name)
            X.append('dataset/'+dir_name+'/'+file_name)

dic={'class':Y,'image':X}
df=pd.DataFrame.from_dict(dic)
df.to_csv('arabic_punctuation.csv', index=False)

