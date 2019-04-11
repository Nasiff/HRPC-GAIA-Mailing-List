import bigbang.mailman as mailman
from bigbang.archive import load as load_archive
from bigbang.parse import get_date
from bigbang.archive import Archive
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
import math
import pytz
import pickle
import os

#specify if you want to have words stemmed (no prefixes, plurals, etc.) or literal 
stem = False


import os 
cwd = os.getcwd()    

archives_names = ["gaia"]


arch_paths = list()
for ml_name in archives_names:
    arch_paths.append('archives/'+ml_name+'.csv')
    

archives_list = [load_archive(arch_path).data for arch_path in arch_paths]
    
archives = Archive(pd.concat(archives_list))
archives_data = archives.data

#instert a word or sentence that you wanna look for
sub_text = 'justice'

#counting how many people wrote that
people_count = defaultdict(int)
for idx, mail in archives_data.iterrows():
    if mail['Body'] is not None: 
        if sub_text in mail['Body']:
            people_count[mail['From']] += 1

#insert how many top-people using that sentence you want to visualize
top_people = 10

print str(len(people_count.keys()))+' people are talking about "'+sub_text+'"'
i = 0
for people, count in sorted(people_count.iteritems(), reverse = True, key = lambda (k,v): (v,k)):
    print people+'   '+str(count)
    i+=1
    if i == top_people: break