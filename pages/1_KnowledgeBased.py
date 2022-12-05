import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
st.set_page_config(
    page_title="GitHub Project Recommendation System",
    page_icon="GitHub-icon.png",
)
components.html("""
     <style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap');</style>
    <h1 style="color:ZBlack;font-family: 'Cinzel Decorative', cursive;
font-size:30px">Enter the details to Recommend Projects</h1>    """,height=100,width=700)
with st.form(key = "form1"):
      tagL = st.text_input('Enter your interests and preferred languages(comma seperated)')
     
      submit = st.form_submit_button(label = "Submit")
      if submit:
        tagsL = tagL.split(",")
        st.write("Your interests",tagsL)
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
                    df.loc[df['Repository Name'].str.contains(tag), tag] += 1
                    df.loc[df['Description'].str.contains(tag), tag] += 1
                df.loc[df['Tags'].str.contains(tag + ","), tag] += 1
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
        new_element = pd.DataFrame(0, [df.index.max() + 1], columns=df.columns)
        for j in (tagsL):
            if j is not None:
                if j.lower() in df.columns:
                    #print("Setting to 1", j.lower())
                    new_element[j.lower()] += 1

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
        repos.extend(["Interested Repo"]) # We add to the csv reponame list, the repo name from github 
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
        st.write("Similar repos to you Interests")
        small2 = df_dist[i].drop_duplicates().nsmallest(2)
        headers = {'content-type': 'application/json',
                    'Accept-Charset': 'UTF-8',
                    'Accept': 'application/vnd.github.mercy-preview+json'}
        # st.write(small2[1])
        for recomended_repo in (df_dist[i][df_dist[i] <= small2[1]].index[0:12]):
                data1 = requests.get('https://api.github.com/repos/%s'% recomended_repo,headers=headers,auth=HTTPBasicAuth(st.secrets['db_username'],st.secrets['db_token']) ).json()
            # print(data1)
                if data1['description']:
                    components.html(""" <style>@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@600;700&display=swap');</style>
                                        <a href="%s" class="data-card" target="_blank" style="display: flex;
                                                                                            flex-direction: column;
                                                                                            max-width: 20.75em;
                                                                                            min-height: 20.75em;
                                                                                            overflow: hidden;
                                                                                            border-radius: 15px;
                                                                                            text-decoration: none;
                                                                                            background: #753BBD;
                                                                                            margin: 1em;
                                                                                            padding: 2.75em 2.5em;
                                                                                            box-shadow: 0 1.5em 2.5em -.5em rgba(#000000, .1);
                                                                                            transition: transform .45s ease, background .45s ease">
                                        <image src="%s" style="border-radius: 50px;margin-left:100px;margin-bottom:35px" height="100" width="100">
                                        <h3 style="color: white;word-wrap:break-word;
                                        font-size: 2.1em;
                                        font-weight: 600;
                                        line-height: 1;
                                        padding-bottom: .5em;
                                        margin: 0 0 0.142857143em;
                                        border-bottom: 2px solid white;
                                        transition: color .45s ease, border .45s ease;">%s</h3>
                                        <p style="color: white;word-wrap:break-word;
                                                    font-size:1.25em;
                                                    font-weight: 600;
                                                    line-height: 1.8;
                                                    margin: 0 0 1.25em;
                                                    ">%s</p>
                                        <span class="link-text" style="color:white;" >
                                            View 
                                            <svg style="margin-left:0.5em;transition: transform .6s ease;" width="25" height="16" viewBox="0 0 25 16" fill="#FFFFFF" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M17.8631 0.929124L24.2271 7.29308C24.6176 7.68361 24.6176 8.31677 24.2271 8.7073L17.8631 15.0713C17.4726 15.4618 16.8394 15.4618 16.4489 15.0713C16.0584 14.6807 16.0584 14.0476 16.4489 13.657L21.1058 9.00019H0.47998V7.00019H21.1058L16.4489 2.34334C16.0584 1.95281 16.0584 1.31965 16.4489 0.929124C16.8394 0.538599 17.4726 0.538599 17.8631 0.929124Z" fill="white"/>
                                        </svg>
                                            </span>
                                        </a>"""%(data1['html_url'],data1['owner']['avatar_url'],recomended_repo,data1['description']),height=500,width=500)

        
