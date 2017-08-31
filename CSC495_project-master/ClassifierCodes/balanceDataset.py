import numpy as np
from pandas import *
import random



dataset=read_csv('privacyArticles_k_20.csv')#privacyArticles_4_25_Top20.csv privacyArticles_4_19_Top20
n=len(dataset)

filename="Modified_k_20.csv" #ModifiedTop20 ModifiedTop20_4_25.csv
#appendFile = open('privacyFilter.csv','w')


nCol=len(dataset.iloc[0,:])
# get positive examples, class label=1
mask=dataset.iloc[:,nCol-1]==1
df=dataset[mask]

# get neg examples, class label=0
negData=dataset[dataset.iloc[:,nCol-1]==0]
random_choice =np.random.choice(negData.index.values,len(df),replace=False) # sample w/o replacement, len(df) times
dfNeg=negData.ix[random_choice]

# combine pos and neg examples
final_data=concat([df,dfNeg])

# write to csv
final_data.to_csv(filename, sep=',', index=False)
print(len(final_data))
