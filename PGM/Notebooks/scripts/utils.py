import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

def load_data():
   iris = load_iris()
   mins = np.min(iris.data,axis=0)
   maxs = np.max(iris.data,axis=0)
   mini_iris = np.round((iris.data - mins)/(maxs-mins)*2).astype(int)
   data = pd.DataFrame(mini_iris)
   data['type'] = iris.target

   #Shuffle data
   data = data.iloc[np.random.permutation(len(data))]
   data.columns = ["attr.a","attr.b","attr.c","attr.d","class"]
   return data

