#!/usr/bin/env python
# encoding: utf-8
import sys

def main():
    if len(sys.argv) != 3:
        print("python keywords_compare.py <privacy_keywords> <iwf>")
        exit(1)

    fw = []
    iwf = []
    with open(sys.argv[1]) as f:
        with open(sys.argv[2]) as f2:
            for line in f:
                fw.append(line.rstrip('\n').split(' ')[0])
            for iwfline in f2:
                iwf.append(iwfline.rstrip('\n').split(' ')[0])
            for word in fw:
                if word not in iwf:
                    print(word)

if __name__ == "__main__":
    main()
