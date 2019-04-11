from bigbang.archive import Archive
from bigbang.archive import load as load_archive
import bigbang.parse as parse
import bigbang.graph as graph
import bigbang.mailman as mailman
import bigbang.process as process
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pprint import pprint as pp
import pytz
import os


#Insert a list of archive names
archives_names = ["gaia"]

cwd = os.getcwd()  

archives_paths = list()
for archive_name in archives_names:
    archives_paths.append('archives/'+archive_name+'.csv')
    

archives_list = [load_archive(archive_path).data for archive_path in archives_paths]
    
archives = Archive(pd.concat(archives_list))

archives_data = archives.data

#The oldest date and more recent date for the whole mailing lists are displayed, so you WON't set an invalid time frame 
print archives_data['Date'].min()
print archives_data['Date'].max()


#set the date frame
date_from = pd.datetime(2000,11,1,tzinfo=pytz.utc)
date_to = pd.datetime(2111,12,1,tzinfo=pytz.utc)

def filter_by_date(df,d_from,d_to):
    return df[(df['Date'] > d_from) & (df['Date'] < d_to)]

#create filtered network
archives_data_filtered = filter_by_date(archives_data, date_from, date_to)
network = graph.messages_to_interaction_graph(archives_data_filtered)

#export the network in a format that you can open in Gephi. 
#insert a file name
file_name = 'architecture_discuss_for_gephi.gexf'

nx.write_gexf(network, cwd+file_name)