import pandas as pd
import numpy as np
import ast
import sys
import logging

def fun(path,W,imp,res):
    df=pd.read_csv(path,index_col='Fund Name')
    print(df)
    df.info()
    n = df.shape[1]
    if (n<3):
        logging.warning('Error Enter the appropriate no. of parameters')
        return
    if (len(W)!=len(imp)!=len(df)):
        logging.warning(' The lengths of weights, impacts, and DataFrame are not equal')
        return



    #taking  weights=[1,1,1,1,1]
    #taking  impact=[1,-1,1,-1,1]

    normalised_df=df/np.sqrt((df ** 2).sum(axis=0))
    normalised_df=normalised_df*W

    # impact=[1,-1,1,-1,1]
    rough=normalised_df*imp
    

    best=rough.max().abs()
    
    worst=rough.min().abs()
    
    #Eucledian distance
    dist_best=np.sqrt(((normalised_df-best)**2).sum(axis=1))
  
    dist_worst=np.sqrt(((normalised_df-worst)**2).sum(axis=1))
  

    total_dist=dist_best+dist_worst
    performance=dist_worst/total_dist
    rank = pd.Series(performance, name='Performance').rank(ascending=False).astype(int)

    normalised_df['Topsis Score']=performance
    normalised_df['Rank']=rank
   
    normalised_df.to_csv(res, index=False)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 5:
        logging.warning('Invalid no. of arguements')
        sys.exit(1)


filepath=sys.argv[1]

weights=sys.argv[2]
weights=ast.literal_eval(weights)

impact=sys.argv[3]
impact=ast.literal_eval(impact)
output=sys.argv[4]
fun(filepath,weights,impact,output)