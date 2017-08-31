# CSC495_project
Class Project

###Install npm
`apt-get install npm` or equivalent

###Install Dependencies
`npm install guardian-js`

###Run
`./run.sh > errors.txt`

## Keyword Extraction

### To access the database
Go to **http://152.46.19.233/phpmyadmin/**

user:privacy

passwd:pr1vacyB0x

table **articles** containes articles from the gurdian searched by privacy_keywords extracted from the 86 tagged articles

table **test_set** contains articles from the guardian manully tagged as web-tracking

you can export the table as a csv file from the export functionality

### We use python3 for all our python scripts
```bash
pip3 install -r requirements.txt
python3 // run python interpreter to complete download packages for nltk
import nltk
nltk.download()
```

### Get common words among web-tracking tagged articles
```bash
python3 get_word_freq.py > privacy_keywords.txt
```

### Get common words among all articles, csv file is exported from phpMyAdmin
Current parsing artilce number will be shown to show the process. A file named iwf.txt will be generated after the script finishes. Multithreading has been implemented but due to GIL, multithreads cannot run on multi core with cPython. The script took 1.5hr on a dual core i5 Macbook Pro. The solution was to implement multiprocess but it would take some time to rewrite a large part of the script.
```bash
python3 get_word_freq.py <csv file>
```

### Homebrewed TF-IDF on two common keywords list
```bash
python3 keywords_compare.py privacy_keywords.txt iwf.txt > filtered_keywords.txt
```

The three keywords files can be found in the repo
privacy_keywords.txt, iwf.txt, filtered_keywords.txt

### Classifier Codes
Codes for classifier is in ClassifierCodes folder
