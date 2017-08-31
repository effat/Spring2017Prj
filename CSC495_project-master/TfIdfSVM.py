import numpy as np
from pandas import *
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import svm
#from sklearn import *



dataset=read_csv('privacyArticles_4_18.csv')
#count columns of the file
nCol=len(dataset.iloc[0,:])
print(nCol)
# separate the data from the target attributes
X = dataset.iloc[:,1:nCol-2]# dependant attributes
#print(X)
y = dataset.iloc[:,nCol-1]# classLabel
#print(y)
#print(dataset)
clf = svm.SVC(kernel='linear', C=1)
#scores = cross_val_score(clf, X, y, cv=10)
scores =cross_val_score(clf, X, y, cv=10, scoring='precision') #accuracy, precision
print("Recall: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2)) # recall=43%, precision=78%
