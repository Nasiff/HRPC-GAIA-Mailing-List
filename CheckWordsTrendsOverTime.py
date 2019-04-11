from bigbang.archive import load as load_archive
from bigbang.archive import Archive
import bigbang.mailman as mailman
import bigbang.process as process
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint as pp
import pytz
import numpy as np
import math
import nltk
from itertools import repeat
from nltk.stem.lancaster import LancasterStemmer
st = LancasterStemmer()
from nltk.corpus import stopwords
import re

#pd.options.display.mpl_style = 'default' # pandas has a set of preferred graph formatting options

#insert a list of the urls of downloaded mailing lists that you want to include in the analysis. 
#data will be merged: multiple mailing lists are treated as a unique corpus

import os 
cwd = os.getcwd()    

archives_names = ["gaia"]


archives_paths = list()
for archive_name in archives_names:
    archives_paths.append('archives/'+archive_name+'.csv')
    

archives_list = [load_archive(archive_path).data for archive_path in archives_paths]
    
archives = Archive(pd.concat(archives_list))

archives_data = archives.data

#insert a list of *single* words to be tracked e.g. checkwords = ['rights', 'economy', 'human']
checkwords = ["human", "rights", "social", "justice", "infrastructure", "accessibility"]

#to stem or not to stem? 
#if stem is set to True, then checkwords should be stemmed words (no plurals, no suffixes, etc.)
#if stem is set to False, then checkwords are searched for their literal spelling
stem = False

#The oldest date and more recent date for the whole mailing lists are displayed, so you WON't set an invalid time frame 
print archives_data['Date'].min()
print archives_data['Date'].max()

#you can filter the data by date range

#set the date frame
date_from = pd.datetime(2014,10,1,tzinfo=pytz.utc)
date_to = pd.datetime(2019,2,28,tzinfo=pytz.utc)

def filter_by_date(df,d_from,d_to):
    return df[(df['Date'] > d_from) & (df['Date'] < d_to)]

archives_data_filtered = filter_by_date(archives_data, date_from, date_to)

def count_word(text,word):
    if not text:
        return 0
    
    if len(word.split(" ")) <= 1:
        ## normalize the text - remove apostrophe and punctuation, lower case
        normalized_text = re.sub(r'[^\w]', ' ',text.replace("'","")).lower()
    
        tokenized_text = nltk.tokenize.word_tokenize(normalized_text)

        if stem:
            tokenized_text = [st.stem(t) for t in tokenized_text]
    
        return tokenized_text.count(word)
    else:
        return text.lower().count(word)

for word in checkwords:
    archives_data_filtered[word] = archives_data_filtered['Body'].apply(lambda x: count_word(x,word))

#save each email in a file based on which checkword it contains. good for doing some qualitative analysis
#set the path where the data are to be saved
path = './archives'
import os
for word in checkwords:
    print "Saving data for checkword "+word+"..."
    archives_data_filtered[archives_data_filtered[word] > 0].to_csv(os.path.join(path,word+'.csv'))

archives_data_filtered = archives_data_filtered.dropna(subset=['Date'])
archives_data_filtered['Date-ordinal'] = archives_data_filtered['Date'].apply(lambda x: x.toordinal())

archives_data_sums = archives_data_filtered.groupby('Date-ordinal').sum()

from datetime import date

for_export = archives_data_sums.copy()

dates_again = pd.Series(for_export.index,
                  index=for_export.index).apply(lambda x: 
                                                date.fromordinal(x))

for_export['Date'] = dates_again

for_export.to_csv("archives/word_counts_by_date.csv")
#
plt.figure(figsize=(12.5, 7.5))

colors = 'rgbkm'

window = 5

for i in range(len(checkwords)):
    # smooth_sums = pd.rolling_mean(archives_data_sums,window)
    smooth_sums = archives_data_sums.rolling(window).mean()
    plt.plot_date(smooth_sums.index,
                  smooth_sums[checkwords[i]],
                  colors[i],
                  label=checkwords[i])

plt.legend(bbox_to_anchor=(.2, 1))


