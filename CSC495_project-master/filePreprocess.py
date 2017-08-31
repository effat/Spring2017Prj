from sklearn.feature_extraction.text import TfidfVectorizer
import numpy
from sklearn.feature_extraction.text import CountVectorizer
"""
    Input: a filename
	Output: a row appended to the file preprocess.csv
	
	The program counts the frequency of words [defined in vocabulary], for a file "fname".
	"fname.txt" contains the text of the Guardian 2002 article provided by Prof.
	
	We consider the guardian article related to 3rd party cookies if at least 5 different words of the vocabulary list [I just added some related words to 3rd party cookies]
	appear in the article. These articles are assigned as classLabel=1 (i.e. these are positive examples for our classifiers)
	
	Otherwise, the classLabel is zero.
	
	As an example: an article related to cookie (biscuit) may only contain words relaed to cookie/cookies, but not any words like-web, privacy, sites
	
	We could collect atricle from a definite time frame (say for last 10 years) and preprocess each file.
	Afterwards we could feed it into the classifier by 10 fold CV.
	
	We could test our classifier by several kernel functions of SVM, and NB classifier.
	
	
	In the preprocess.csv file, the 1st column now contains the filename, it could be replaced by weblink of the article.
	
"""

fname="cookie.txt"
file = open(fname, "r") 
ref_docs = []
for line in file:

	ref_docs.append(line)
	
	
	
count_vectorizer = CountVectorizer(stop_words='english', vocabulary=['cookie','cookies','privacy','site','sites','web','website','websites','browse'])
counts = count_vectorizer.fit_transform(ref_docs)
freq_count=counts.toarray().sum(axis=0) #sum up the frequencies of the words in vocabulary

sum=0
classLabel=0
for i in freq_count:
	if freq_count[i]>0:
		sum=sum+1
		
			
if sum>5:
	classLabel=1
	
	
appendFile = open('preprocess.csv','a')

appendFile.write(fname)
appendFile.write(',')

for i in freq_count:
	appendFile.write(str(freq_count[i]))
	appendFile.write(',')
	
		
appendFile.write(str(classLabel))
appendFile.close() 
