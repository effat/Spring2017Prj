from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import pymysql
import pymysql.cursors

conn = pymysql.connect(host='152.46.19.233',user='privacy',password='pr1vacyB0x',db='privacy') #db connection string
title="weblink, cookie, cookies, privacy, site, sites, web, website, websites, browse, browser, technology, information, advertising, google, data, classLabel"


try:
    #initialize CountVectorizer to count frequencies of user provided vocabularies, stop words are stop words of English
    count_vectorizer = CountVectorizer(stop_words='english', vocabulary=['cookie','cookies','privacy','site','sites','web','website','websites','browse','browser','technology','information','advertising','google','data'])
    appendFile = open('privacyArticles.csv','w')
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

        if sum>2:
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
