#!/usr/bin/env python
# encoding: utf-8


from __future__ import with_statement
from collections import OrderedDict
from nltk.corpus import stopwords
import pandas as pd
import sys, operator, itertools, threading
from multiprocessing.dummy import Pool as ThreadPool

# Homebrewed simple keyword extractor
# author: Xiao Cheng

phrase_length = 3
min_threshold = 0.05
worker = 4

# a stopped word list from https://raw.githubusercontent.com/Alir3z4/stop-words/0e438af98a88812ccc245cf31f93644709e70370/english.txt
common="a about above after again against all am an and any are aren't as at be because been before being below between both but by can can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves"
minifreq = 0
total_word = 0
words = {}
lock = threading.RLock()

# return a list of keyword that the article has
def parse_article(content):
    word_list = []
    try:
        all_words = content.split()
        for i in range(len(all_words)):
            for inc in range(phrase_length):
                if i + inc < len(all_words):
                    word = clean(' '.join(all_words[i:i+inc])).lower()
                    if word not in word_list:
                        word_list.append(word)
    except:
        pass
    with lock:
        for word in word_list:
            if word in words:
                words[word] += 1
            else:
                words[word] = 1

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
    with open("iwf.txt", "w+") as f:
        for k in sorted_words:
            f. write("%s %s\n" %(k, float(sorted_words[k])/total_word))

# extract a single word from a string
def clean(word):
    if word.startswith('“'):
        return clean(word[1:])
    elif word.endswith('.') or word.endswith('!') or word.endswith('?') or word.endswith('”') or word.endswith('...') or word.endswith(',') or word.endswith(":"):
        return clean(word[:-1])
    else:
        return word

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 get_word_file.py <filename>")

    
    filename = sys.argv[1]
    df = pd.read_csv(filename)
    total_word, a = df.shape
    minifreq = min_threshold * total_word
    count = 0
    with ThreadPool(worker) as p:
        for article_content in df['body']:
            count += 1
            print(count)
            if not isinstance(article_content, float):
                p.map(parse_article, (article_content,))
    postprocessing()
    print_freq()

