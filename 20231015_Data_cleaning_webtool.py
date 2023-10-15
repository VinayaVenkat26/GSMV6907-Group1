# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sp
import matplotlib.pyplot as plt
import seaborn as sns

# Information on the webtool
st.title('Data cleaning webtool')

st.header('Welcome to the data cleaning webtool')
st.write('In this webtool, we will be cleaning your data file in the following ways:')
st.write('1. Managing duplilcate values')
st.write('2. Managing missing values')
st.write('3. Integer to decimal conversion and vice versa')
st.write('4. Split or concatenate columns')
st.write('In transcriptomic datafiles, converting dates to gene names if converted by excel') # Give the link to the gene to date converter


# Uploading datafile
st.header('1. Uploading your datafile')

option = st.selectbox('Please choose the file format you are uploading', ('Excel', 'CSV', 'TSV'))
st.write('You have selected:', option)

upload = st.file_uploader(f'Upload your {option} file here')

st.subheader('*Please note:*')
st.write('*1. The webtool will consider the first column in the file as the index*')
st.write('*2. Add an excel file with only one sheet in it to prevent errors*')


st.header('2. Checking for duplicates')
# Convert the uploaded file to a DataFrame
df = None
if option == 'Excel':
    df = pd.read_excel(upload, index_col = 0)
elif option == 'CSV':
    df = pd.read_csv(upload, index_col = 0)
elif option == 'TSV':
    df = pd.read_csv(upload, sep='\t', index_col = 0)

# Options for data cleaning

# Need to find the duplicates rows/columns and show that to the reader to decide
def check_duplicates(df):
    if df is not None and not df.empty:  # Check if df is not None and not empty
        row_dups = not df.index.is_unique
        col_dups = not df.columns.is_unique

        if row_dups and col_dups:
            return "Both rows and columns have duplicates."
        elif row_dups:
            return "Rows have duplicates."
        elif col_dups:
            return "Columns have duplicates."
        else:
            return "No duplicates were found in rows or columns."

if df is not None and not df.empty:
    st.write(check_duplicates(df))

# Decide
dup_check = check_duplicates(df)
if dup_check != "No duplicates were found in rows or columns.":
    st.write('How would you like to handle your duplicates? (Select one)')
    dup_handle = st.selectbox('Please choose the file format you are uploading', ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value'))
else:
    st.write('Moving on to the next cleaning step')