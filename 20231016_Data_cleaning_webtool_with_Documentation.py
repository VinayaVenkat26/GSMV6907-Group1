# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Information on the webtool
st.title('Data cleaning webtool')
st.markdown('Group project for GMS6907: Vinaya, Qing xin, Pooja, He Shan')

yes = st.sidebar.checkbox("Documentation")

if yes:
 st.header('Welcome to the data cleaning webtool')
 st.write('In this webtool, we will be cleaning your data file in the following ways:')
 st.write('1. Managing duplilcate values')
 st.write('2. Managing missing values')
 st.write('3. Integer to decimal conversion and vice versa')
 st.write('4. Split or concatenate columns')
 st.write('In transcriptomic datafiles, converting dates to gene names if converted by excel') # Give the link to the gene to date converter

### Reading input file from user

File = st.sidebar.file_uploader('Upload your own data in .csv format')

if File is not None:
	df = pd.read_csv(File)
	df = df.dropna()
else:
	st.stop()

    
if st.sidebar.checkbox('Show the dataset as a data table'):
        st.dataframe(data=df)

