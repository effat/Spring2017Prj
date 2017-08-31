from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import pymysql
import pymysql.cursors
import numpy as np
from pandas import *


#read the keywords extracted from TF-IDF
dataset=read_csv('TfIdfKeyWords_1.csv')

#get only keywords labelled as 1 (1= privacy related)
mask=dataset.iloc[:,1]==1

#slice the privacy keywords from the rest
df=dataset[mask]

#extract top k keywords to build feature set for classifier. k=50
privacy_keys=[]
for i in range(0,50):
    privacy_keys.append(df.iloc[i,0])


#remove duplicate keywords from selected keywords for feature set
final_keys=list(set(privacy_keys))

#the column names of the output of csv file :
# each article will be one row in the output csv file
#Each row is represented : weblink, [feature keywords set], classlabel
myStr=",".join(final_keys)
title="weblink,"+myStr+",classLabel"

# database connection
conn = pymysql.connect(host='152.46.19.233',user='privacy',password='pr1vacyB0x',db='privacy') #db connection string


try:
    #initialize CountVectorizer to count frequencies of user provided vocabularies, here vocabularies are feature keyword set extracted in above step. stop words are stop words of English
    count_vectorizer = CountVectorizer(stop_words='english', vocabulary=final_keys)
    appendFile = open('privacyArticles_4_18.csv','w')
    appendFile.write(title) # column names
    appendFile.write('\n')


    cursor=conn.cursor()
    cursor.execute("SELECT ID, body FROM privacy.articles") # grab the ID and body text of all articles in the db
    rows_affected=cursor.rowcount
    print(rows_affected)
    rowCount=0
    result = cursor.fetchone() #grab one row from selected rows

    while result is not None:
        ref_docs =[result[1]]
        rowCount+=1

        if result[1] is None: #some rows have body field =None
            #print(rowCount)#
            result=cursor.fetchone() # do not parse this article, continue to the next row
            continue

        counts = count_vectorizer.fit_transform(ref_docs) # counts the frequencies of keywords
        freq_count=counts.toarray().sum(axis=0)


        sum=0
        classLabel=0
        for i in range(len(freq_count)):
            if freq_count[i]>0:
                sum=sum+1

        if sum>3:
            classLabel=1 #if 3 keywords are present, it is a positive example

        appendFile.write(result[0]) #write the weblink of the article
        appendFile.write(',')
        for i in range(len(freq_count)): #write all the frequencies of keywords
           appendFile.write(str(freq_count[i]))
           appendFile.write(',')

        appendFile.write(str(classLabel)) #write classLabel, i.e. category for this article. Privacy related article=1, otherwise=0
        appendFile.write('\n')
        result=cursor.fetchone() # fetch next record
    cursor.close()
    appendFile.close()

finally:
    conn.close()
