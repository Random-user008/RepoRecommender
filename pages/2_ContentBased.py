import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import time

import warnings
warnings.filterwarnings('ignore')
st.set_page_config(
    page_title="GitHub Project Recommendation System",
    page_icon="GitHub-icon.png",
)
components.html("""
     <style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap');</style>
    <h1 style="color:ZBlack;font-family: 'Cinzel Decorative', cursive;
font-size:30px">Enter the details to Recommend Projects</h1>    """,height=100,width=700)
Username = st.text_input('Enter GitHub Username')
st.write("UserName Entered is: ",Username)
time.sleep(8)
st.write("LOADING... ")


  # Load data
df = pd.DataFrame()

#This is the standar csv, with the gravatar images for each repo     
df = pd.read_csv("https://raw.githubusercontent.com/kaayush71/shopping-cart-CSV/main/TopStaredRepositories.csv")
df.set_index(['Repository Name'])

# st.write(df.head(2))
## Cleaning data
# We fill the emptpy URL cells
df['Url'] = "http://github.com/" +         df['Username'] + "/" + df['Repository Name']
# We add a final comma character for the tag string, it will be usefull when we tokenize
df['Tags'].fillna("", inplace=True)
df['Tags'] = df['Tags'] + ","

# We do not want uppercase on any label
df['Language'] = df.loc[:, 'Language'].str.lower()
# Copy a backup variable, so we can change our main dataframe
df_backup = df.copy(deep=True)
# st.write(df.head(2))
mergedlist = []
for i in df['Tags'].dropna().str.split(","):
    mergedlist.extend(i)
tags = sorted(set(mergedlist))
# Encode languages in single column
just_dummies = pd.get_dummies(df['Language'])
for column in just_dummies.columns:
    if column not in df.columns:
        df[column] = just_dummies[column]
# st.write(df.head(2))
for tag in tags:
    if tag not in df.columns:
        df[tag] = 0
    try:
        if len(tag) > 4 :
            df.loc[df['Repository Name'].str.contains(tag), tag] = 1
            df.loc[df['Description'].str.contains(tag), tag] = 1
        df.loc[df['Tags'].str.contains(tag + ","), tag] = 1
    except Exception:
        pass
# Remove columns not needed
df.set_index(['Repository Name'])
COLUMNS_TO_REMOVE_LIST = ['', 'Username', 'Repository Name', 'Description',
                          'Last Update Date', 'Language', 'Number of Stars', 'Tags', 'Url','Gravatar' ,'Unnamed: 0']
# Stop words: links to (https://github)
RAGE_TAGS_LIST = [ 'github','algorithms','learn','learning','http' ,'https']



for column in COLUMNS_TO_REMOVE_LIST + RAGE_TAGS_LIST:
    try:
        del df[column]
    except Exception:
        pass

df.columns = df.columns.str.lower()

print ("Our final label matrix for repo list is")
# st.write(df.head(2))

corr = df.corr()
corr.iloc[0:5][0:5]
corr['machine-learning'].dropna().sort_values().tail(5).head(4)

GITHUBUSER=Username
# !pip install wheel
# !pip install pyjq
import requests
from requests.auth import HTTPBasicAuth
# import pyjq
github_user = GITHUBUSER
# We have do not have internet access inside the notebook, 
# but the coude to query github api would be
PERSONAL_TOKEN = "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"

# Token is not mandatory, but there is a query rate limit, for those API calls which do not use token.  

url = 'https://api.github.com/users/%s/repos?sort=updated' % github_user
headers = {'content-type': 'application/json',
          'Accept-Charset': 'UTF-8',
          'Accept': 'application/vnd.github.mercy-preview+json'}
r = requests.get(url,  headers=headers, auth=HTTPBasicAuth(
   "RISHABH175", PERSONAL_TOKEN))
# r = requests.get('https://api.github.com/users/kaayush71/repos',headers = headers)
json_response = r.json()


repo_topics = []
repo_languages = []
repo_names = ["github-recommendation-engine"]
repo_description = []

for ob in json_response:
  if ob['topics']:
    repo_topics = repo_topics + ob['topics']
  if ob['language']:
    repo_languages = repo_languages + ob['language'].split()
  # if ob['name']:
  #   repo_names = repo_names + ob['name'].split()
  if ob['description']:
    repo_description = repo_description + ob['description'].split()

# st.write(repo_topics)
# st.write(repo_languages)
# st.write(repo_names)
# st.write(repo_description)

# i=0 # first repo from the list
# repo_names       = pyjq.all(".[%s] | .name"        % i,  json_response)
# repo_languages   = pyjq.all(".[%s] | .language"    % i,  json_response)
# repo_description = pyjq.all(".[%s] | .description" % i,  json_response)
# repo_topics      = pyjq.all(".[%s] | .topics"      % i,  json_response)
# repo_names       = ["github-recommendation-engine"]
# repo_languages   = ["Python"]
# repo_description = ["A github repository suggestion system"]
# repo_topics  = ["github","machine-learning","recommendation-system"]
if repo_description[0] is None: repo_description = ['nodescription']

# We add a new element to the end of the DataFrame
new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)

label_list = repo_names[0].split('-')  + repo_languages + repo_description[0].replace(".", " ").replace(",", " ").split() + list(repo_topics)
print( "The labels from the repo are :" , label_list)

for j in (label_list):
    if j is not None:
        if j.lower() in df.columns:
            #print("Setting to 1", j.lower())
            new_element[j.lower()] = 1

# Concat new user repo dataframe to stared repos dataframe
df = pd.concat([df, new_element])
# Now user repo is on the last row of the label matrix
# st.write(df.tail(2))
df_reduced = pd.DataFrame()
NUM_ELEMENTS=len(df)-1
user_repo = df.iloc[NUM_ELEMENTS:]
for k in df.columns :
    existe = user_repo[k].values[0]
    if existe > 0 : df_reduced[k] = df[k]

df = df_reduced.copy(deep=True)

# Remember user repo is the last one
# st.write(df.tail(10))
from scipy.spatial import distance
from scipy.spatial.distance import squareform, pdist
repos = list(df_backup['Username'] + "/" + df_backup['Repository Name'])
repos.extend(repo_names) # We add to the csv reponame list, the repo name from github 
print(repos)
print (repos[-1] ,len(repos), df.shape, df_backup.shape)
# We calculate the euclidean distance for the binary label matrix 3
res = pdist(df, 'euclidean')

df_dist = pd.DataFrame(squareform(res), index=repos, columns=repos)

print("""This is the euclidean distance matrix for 
     - the user repo (github-recommendation-engine) 
     - other eight repos :
      The lower the distance, stronger the similarity between repos
      """)


import seaborn as sns
import matplotlib.pyplot as plt

f,ax = plt.subplots(figsize=(18, 18))
sns.heatmap(df_dist.iloc[972:,972:] , annot=True, linewidths=.5, fmt= '.1f',ax=ax , cmap='viridis' )

result_array = []
i = df_dist.columns[-1]
# We change 0 for 1000, to filter when calculating minimun distances 
# (because obviously, the repo that has more similarity with the repo list is itself. )
df_dist.loc[df_dist[i] == 0, i] = 1000
# Get minimun distance
min = df_dist[i].min()
# Filter all repo within that minimun distance
closest_repos = df_dist[i][df_dist[i] == min].index, i, min
# print results
st.write("Similar repos to %s are: " % GITHUBUSER )
for recomended_repo in (df_dist[i][df_dist[i] == min].index[0:12]):
 
    st.write(recomended_repo)
