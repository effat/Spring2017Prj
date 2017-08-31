import numpy as np
from pandas import *
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import svm
from sklearn.utils import shuffle
from sklearn.model_selection import *
from sklearn.metrics import precision_score, recall_score, f1_score
#from sklearn import *



dataset=read_csv('Modified_k_20.csv')#ModifiedTop20
#count columns of the file
nCol=len(dataset.iloc[0,:])
print(nCol)
print(len(dataset))
#shuffle the dataset
dataset.iloc[np.random.permutation(len(dataset))]#np.random.shuffle(dataset)
# separate the data from the target attributes
X = dataset.iloc[:,1:nCol-2]# dependant attributes
#print(X)
y = dataset.iloc[:,nCol-1]# classLabel


clf = svm.SVC(kernel='linear', C=1)
#Translates slice objects to concatenation along the second axis.
X=np.c_[X]
#y=np.c_[y]

posPrecisions=[]
negPrecisions=[]

posRecalls=[]
negRecalls=[]

posF1=[]
negF1=[]

for i in range (5): # repeat 10 fold CV 5 times
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=i+1) # generate cross validation split
    for train_index, test_index in cv.split(X, y): # execute cross validation 10 times
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        posPrec=precision_score(y_test, y_pred,pos_label=1, average="binary")
        posPrecisions.append(posPrec)
        negPrec=precision_score(y_test, y_pred,pos_label=0, average="binary" )
        negPrecisions.append(negPrec)

        ## recall
        recallP=recall_score(y_test, y_pred, average="binary", pos_label=1)
        recallN=recall_score(y_test, y_pred, average="binary", pos_label=0)
        posRecalls.append(recallP)
        negRecalls.append(recallN)

        f1P=f1_score(y_test, y_pred, average="binary", pos_label=1)
        f1N=f1_score(y_test, y_pred, average="binary", pos_label=0)

        posF1.append(f1P)
        negF1.append(f1N)


#print(sum(precisions)/float(len(precisions))) # recall=43%, precision=78%
print(sum(posPrecisions)/float(len(posPrecisions)))
print(sum(negPrecisions)/float(len(negPrecisions)))

print("Recall---\n")
print(sum(posRecalls)/float(len(posRecalls)))
print(sum(negRecalls)/float(len(negRecalls)))

print("F1---\n")
print(sum(posF1)/float(len(posF1)))
print(sum(negF1)/float(len(negF1)))

print(len(posPrecisions))
