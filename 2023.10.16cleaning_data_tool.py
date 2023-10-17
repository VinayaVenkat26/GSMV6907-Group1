# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sp
import matplotlib.pyplot as plt
import seaborn as sns


# Information on the webtool
st.title('Data cleaning webtool')

st.sidebar.header('Welcome to the data cleaning webtool')
st.sidebar.write('In this webtool, we will be cleaning your data file in the following ways:')
st.sidebar.markdown('1. [Managing duplicate values](#manage-duplicates)')
st.sidebar.markdown('2. [Managing missing values](#manage-missing)')
st.sidebar.markdown('3. [Integer to decimal conversion and vice versa](#convert-int-to-decimal)')
st.sidebar.markdown('4. [Split or concatenate columns](#split-concatenate-columns)')
st.sidebar.markdown('5. [Converting dates to gene names in transcriptomic datafiles](#convert-dates-to-gene-names)')  # Provide the link to the gene-to-date converter
st.sidebar.markdown('To upload your data, click [here](#upload-anchor)')
st.sidebar.checkbox('Check documentation')


# Section 2: Upload datafile
st.subheader('1. Uploading your datafile')
st.markdown('<a name="upload-anchor"></a>', unsafe_allow_html=True)  # Create an anchor for this section

option = st.selectbox('Please choose the file format you are uploading', ('Excel', 'CSV', 'TSV'))
st.sidebar.write('You have selected:', option)

upload = st.file_uploader(f'Upload your {option} file here')

st.sidebar.subheader('*Please note:*')
st.sidebar.write('*1. The webtool will consider the first column in the file as the index*')
st.sidebar.write('*2. Add an Excel file with only one sheet in it to prevent errors*')

# Convert the uploaded file to a DataFrame
df = None
if option == 'Excel':
    df = pd.read_excel(upload, index_col=0)
    df
elif option == 'CSV':
    df = pd.read_csv(upload, index_col=0)
    df
elif option == 'TSV':
    df = pd.read_csv(upload, sep='\t', index_col=0)
    df

# Section 3: Check for duplicate values
st.subheader('2. Managing duplicate values')
st.markdown('<a name="manage-duplicates"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Need to find the duplicates rows/columns and show that to the reader to decide
def check_duplicates(df):
    if df is not None and not df.empty:  # Check if df is not None and not empty
        row_dups = not df.index.is_unique
        col_dups = not df.columns.is_unique

        if row_dups and col_dups:
            return "Both rows and columns have duplicates."
        elif row_dups:
            duplicated_values = df[df.duplicated()]
            st.write(duplicated_values)
            return "Rows have duplicates."
        elif col_dups:
            duplicated_values = df[df.duplicated()]
            st.write(duplicated_values)
            return "Columns have duplicates." 
        else:
            return "No duplicates were found in rows or columns."

if df is not None and not df.empty:
    st.sidebar.write(check_duplicates(df))


# Decide
dup_check = check_duplicates(df)
if dup_check != "No duplicates were found in rows or columns.":
    st.write('How would you like to handle your duplicates? (Select one)')
    dup_handle = st.selectbox('Please choose the file format you are uploading', ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value'))
else:
    st.write('Moving on to the next cleaning step')




# Section 4: Manage missing values
st.subheader('3. Managing missing values')
st.markdown('<a name="manage-missing"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Only need to display rows or columns with missing values


st.write("Your dataframe has missing values here:")
missing_values = df.isnull().sum()
st.write(missing_values)





# Section 5: Integer to decimal conversion and vice versa
st.subheader('4. Integer to decimal conversion and vice versa')
st.markdown('<a name="convert-int-to-decimal"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for integer to decimal conversion...




# Section 6: Split or concatenate columns
st.subheader('5. Split or concatenate columns')
st.markdown('<a name="split-concatenate-columns"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for splitting or concatenating columns...



# Section 7: Convert dates to gene names
st.subheader('6. Converting dates to gene names in transcriptomic datafiles')
st.markdown('<a name="convert-dates-to-gene-names"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for converting dates to gene names...


