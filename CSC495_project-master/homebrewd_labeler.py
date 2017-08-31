import pandas as pd
import sys
thread_hold = 40

def main():
    df = pd.read_csv(sys.argv[1])
    total, m = df.shape
    keywords = []
    labeled = 0
    with open("filtered_keywords.txt") as f:
        for line in f:
            keywords.append(line.rstrip('\n'))
        with open("results.csv", 'w+') as results:
            for index, row in df.iterrows():
                print("Count %s/%s" %(index,total))
                word_list = parse_article(row[1])
                count = 0
                for word in word_list:
                    if word in keywords:
                        count += 1
                    if count >= thread_hold:
                        labeled += 1
                        break
                results.write("%s,%s\n" % (row[0],count>=thread_hold))
    print labeled

def parse_article(content):
    word_list = []
    try:
        all_words = content.split()
        for word in all_words:
            if word not in word_list:
                word_list.append(word)
    except:
        pass
        
    return word_list

# extract a single word from a string
def clean(word):
    if word.startswith('"'):
        return clean(word[1:])
    elif word.endswith('.') or word.endswith('!') or word.endswith('?') or word.endswith('"') or word.endswith('...') or word.endswith(',') or word.endswith(":"):
        return clean(word[:-1])
    else:
        return word

if __name__ == "__main__":
    main()