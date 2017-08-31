import numpy as np
from pandas import *


dataset=read_csv('privacyArticles.csv')
n=len(dataset)

filename="privacyExtract.csv"
#appendFile = open('privacyFilter.csv','w')

#title="weblink, cookie, cookies, privacy, site, sites, web, website, websites, browse, browser, technology, information, advertising, google, data, classLabel"
#appendFile.write(title)
#appendFile.write('\n')

mask=dataset.iloc[:,16]==1

df=dataset[mask]
df.to_csv(filename, sep=',', index=False)
#appendFile.close()
