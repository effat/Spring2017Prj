from bs4 import BeautifulSoup
import sys, time, urllib.request, json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 ugly_fetcher.py <url of api>")

    response = urllib.request.urlopen(sys.argv[1])
    data = json.load(response)
    count = 1
    with open("content.txt", 'w') as f:
        for article in data["response"]["results"]:
            print("Current Fetching Article Number: %d" % count )
            count += 1
            try:
                webpage = BeautifulSoup(urllib.request.urlopen(article["webUrl"]), 'html.parser')
                f.write(webpage.find('div', {'class':'content__article-body'}).text)
            except AttributeError:
                print(article["webUrl"])