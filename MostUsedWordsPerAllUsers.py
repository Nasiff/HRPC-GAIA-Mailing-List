from bigbang.archive import load as load_archive
from bigbang.archive import Archive
import pandas as pd
from nltk.corpus import stopwords
from nltk import tokenize
from collections import defaultdict
import csv
from pandas import DataFrame as df
from nltk.stem.lancaster import LancasterStemmer
import re
st = LancasterStemmer()
import time

#specify if you want to have words stemmed (no prefixes, plurals, etc.) or literal 
stem = False


import os 
cwd = os.getcwd()    

archives_names = ["gaia"]


archive_paths = list()
for archive_name in archives_names:
    archive_paths.append('archives/'+archive_name+'.csv')
    
print "archive_paths: " + str(len(archive_paths))

archives_list = [load_archive(arch_path).data for arch_path in archive_paths]

print "archives_list: " + str(len(archives_list))
    
archives = Archive(pd.concat(archives_list))
archives_data = archives.data

print "archives_data: " + str(len(archives_data))

#preparing a function to count top words per user

def count_words(texts):
    wordcount={}
    for text in texts:
            w = text.replace("'", "")
            k = re.sub(r'[^\w]', ' ', w)
            t = tokenize.word_tokenize(k)
            for g in t:
                try:
                    if stem: word = st.stem(g)
                    else: word = g
                except:
                    print g
                    pass
                if word in stopwords.words('english'):
                    continue
                if word not in wordcount:
                    wordcount[word] = [1]
                else:
                    wordcount[word][0] += 1
    return wordcount

#extract the list of users and compute the word count per each user (might take some time!)

user_wordcount = defaultdict(int)

users = list(archives_data["From"])

print "size before: " + str(len(user_wordcount.keys()))
start_time = time.time()

for user in set(users):
    try:
        messages = archives_data[archives_data["From"] == user]["Body"]
        user_wordcount[user]= count_words(messages)
    except: pass

print "size after: " + str(len(user_wordcount.keys()))
print "Time it takes to extract the list and compute word count per user: " + str((time.time() - start_time)) + " seconds"


#insert the number of top words you want to export
n_top_words = 10

#edit the file name in case...
users_topwords_f = open('users_topwords.csv', "wb")
users_w = csv.writer(users_topwords_f)

for user, wordcount in user_wordcount.iteritems():    
    for word, count in sorted(wordcount.iteritems(), reverse = True, key = lambda (k,v):(v,k))[:n_top_words]:
        users_w.writerow([user]+[word]+[count[0]])
users_topwords_f.close()
print 'File exported!'