# from turtle import width
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
# import os
# import subprocess
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.feature_selection import RFE
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.model_selection import RandomizedSearchCV
# from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
# from sklearn.decomposition import PCA, KernelPCA
# from sklearn.tree import DecisionTreeClassifier
# from sklearn import tree
# from sklearn.svm import SVC
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.pipeline import Pipeline
# from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import precision_score
# from sklearn.metrics import recall_score
# from sklearn.metrics import f1_score
# from sklearn.metrics import roc_auc_score
# from sklearn.metrics import cohen_kappa_score
# from sklearn import metrics
# from sklearn.model_selection import GridSearchCV
# from sklearn.naive_bayes import GaussianNB
# from sklearn.metrics import roc_curve, auc
# from sklearn.metrics import roc_auc_score
# import pickle

    # st.title(f"Welcome to GitHub Project Recommendation System And User Analytics")
st.set_page_config(
    page_title="GitHub Project Recommendation System",
    page_icon="GitHub-icon.png",
)
components.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative&display=swap');
h1
{
  color:black;
  font-size:40px;
}
hr.new5 {
  border: 5px dashed red;
  border-radius: 60px;
}

</style>

    
                        <div >
                        
                          <h1 style="font-family: 'Cinzel Decorative', cursive;">Welcome to GitHub Project Recommendation System And User Analytics</h1>
                        </div>
                       
<hr class="new5">
                    
                        """,
                        height=300,
                      width=700,
                      )
# if selected == "Knowledge Based":
    
  
