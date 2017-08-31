from __future__ import with_statement
from bs4 import BeautifulSoup
from collections import OrderedDict
from nltk.corpus import stopwords
import sys, time, urllib.request, json, operator, itertools

# Homebrewed simple keyword extractor
# author: Xiao Cheng

phrase_length = 3

# a stopped word list from https://raw.githubusercontent.com/Alir3z4/stop-words/0e438af98a88812ccc245cf31f93644709e70370/english.txt
common="a about above after again against all am an and any are aren't as at be because been before being below between both but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
words = {}
minifreq = 7

# defaulted apiurl if not specified as command line arg
apiurl = "https://content.guardianapis.com/search?tag=technology/cookies-and-web-tracking&page-size=86&api-key=641403c5-641b-4b14-bef8-f1fa7efd271b"

# return a list of keyword that the article has
def parse_article(content):
    word_list = []
    all_words = content.split()
    for i in range(len(all_words)):
        for inc in range(phrase_length):
            if i + inc < len(all_words):
                word = clean(' '.join(all_words[i:i+inc])).lower()
                if word not in word_list:
                    word_list.append(word)
    return word_list

def postprocessing():
    if '-' in words:
        del words['-']
    if '–' in words:
        del words['–']
    for i in range(phrase_length):
        for combinations in itertools.combinations(common.split(), i):
            word = ' '.join(combinations)
            if word in words:
                del words[word]
    low_freq = []
    for word, freq in words.items():
        if freq < minifreq:
            low_freq.append(word)
    for word in low_freq:
        del words[word]
    stopWords = set(stopwords.words('english'))
    for w in stopWords:
        if w in words:
            del words[w]

# Print the words dictionary with highest frequency
def print_freq():
    sorted_words = OrderedDict(sorted(words.items(), key=lambda t:t[1]))
    for k in sorted_words:
        print("%s %s" %(k, sorted_words[k]))

# extract a single word from a string
def clean(word):
    if word.startswith('“'):
        return clean(word[1:])
    elif word.endswith('.') or word.endswith('!') or word.endswith('?') or word.endswith('”') or word.endswith('...') or word.endswith(',') or word.endswith(":"):
        return clean(word[:-1])
    else:
        return word

if __name__ == "__main__":
    if len(sys.argv) == 2:
        apiurl = sys.argv[1]

    response = urllib.request.urlopen(apiurl)
    data = json.load(response)
    count = 1
    for article in data["response"]["results"]:
        #print("Current parsing article number: %d" % count)
        count += 1
        try:
            #print("* Parsing %s" % article["webUrl"])
            webpage = BeautifulSoup(urllib.request.urlopen(article["webUrl"]), 'html.parser')
            article_content = webpage.find('div', {'class':'content__article-body'}).text
            word_list = parse_article(article_content)
            for word in word_list:
                if word in words:
                    words[word] += 1
                else:
                    words[word] = 1
        except AttributeError:
            pass
    postprocessing()
    print_freq()
