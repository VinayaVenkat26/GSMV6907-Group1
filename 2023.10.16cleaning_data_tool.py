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
st.sidebar.markdown('5. [Converting dates to gene names in transcriptomic datafiles](#convert-dates-to-gene-names)')  # Provided the link to the gene-to-date converter
st.sidebar.markdown('To upload your data, click [here](#upload-anchor)')  # Mamaged to override the error when no file is uploaded
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

if upload is not None:
    if option == 'Excel':
        df = pd.read_excel(upload, index_col=0)
    elif option == 'CSV':
        df = pd.read_csv(upload, index_col=0)
    elif option == 'TSV':
        df = pd.read_csv(upload, sep='\t', index_col=0)
else:
    # Load an example datafile or display a message if no file is uploaded
    df = pd.read_excel('C:\\Users\\vinaya\\Downloads\\Example data file for STREAMLIT APP.xlsx', index_col = 0)  # Change to URL once the example file in github is loaded
    st.write('No file uploaded. Showing example data.')
    st.write(df)

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
    st.write(check_duplicates(df))


# Decide
def handle_duplicates(df):
    dup_check = check_duplicates(df)
    
    if dup_check == "No duplicates were found in rows or columns.":
        st.write('Moving on to the next cleaning step....')
    else:
        dup_handle = st.selectbox('How would you like to handle your duplicates? (Select one)', ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value', 'Ignore'))
        return dup_handle


# Call the function
dup_handle = handle_duplicates(df)

# Ignore
if dup_handle == 'Ignore':
    st.write('Moving on to the next cleaning step')

mean_operation = None
keep_first = None
keep_last = None

# Means
if dup_handle == 'Take mean of duplicates':
    mean_operation = st.selectbox('Calculate mean for:',['Rows','Columns'])
                                 
if mean_operation == 'Rows':
    st.subheader('Data after mean')
    df = df.groupby(df.index).mean()
    
if  mean_operation == 'Columns': 
    st.subheader('Data after mean')
    df = df.groupby(df.columns).mean()


# Keep first
if dup_handle == 'Choose only the first value':    
    keep_first = st.selectbox('Keep first of:',['Rows','Columns'])

if keep_first == 'Rows':
    st.subheader('After deleting unwanted duplicates')
    df = df[~df.index.duplicated(keep='first')]
    
if  keep_first == 'Columns':
    st.subheader('After deleting unwanted duplicates')
    df = df.loc[:, ~df.columns.duplicated(keep='first')]

# Keep last
if dup_handle == 'Choose only the last value':    
    keep_last = st.selectbox('Keep last of:',['Rows','Columns'])

if keep_last == 'Rows':
    st.subheader('After deleting unwanted duplicates')
    df = df[~df.index.duplicated(keep='last')]
    
if  keep_last == 'Columns': 
    st.subheader('After deleting unwanted duplicates')
    df = df.loc[:, ~df.columns.duplicated(keep='last')]


# Section 4: Manage missing values

st.subheader('3. Managing missing values')
st.markdown('<a name="manage-missing"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Find rows and columns with missing values
missing_values = df.isna()
missing_rows = missing_values.any(axis=1)
missing_cols = missing_values.any()

if any(missing_rows) or any(missing_cols):

    # Display rows with missing values                        # This part requires more troubleshooting
    if any(missing_rows):
        st.write("Rows with missing values:")
        st.write(df[missing_rows])
        missing_rows_indices = df[missing_rows].index.tolist()
        selected_rows = []  # Initialize as an empty list

        if st.button('Compute Missing Values for Selected Rows'):
            for row_index in missing_rows_indices:
                if row_index in selected_rows:
                    action = st.selectbox(f"Select action for row {row_index}:", ["Delete Row", "Fill with Value"])
                    if action == "Delete Row":
                        df = df.drop(index=row_index)
                    elif action == "Fill with Value":
                        filler_value = st.text_input(f"Fill missing values for row {row_index} with:")
                        df.loc[row_index] = df.loc[row_index].fillna(filler_value)
                        

    # Display columns with missing values
    if any(missing_cols):
        st.write("Columns with missing values:")
        st.write(df.loc[:, missing_cols])
        missing_cols_names = missing_cols[missing_cols].index.tolist()
        selected_cols = []  # Initialize as an empty list

        if st.button('Compute Missing Values for Selected Columns'):
            for col_name in missing_cols_names:
                if col_name in selected_cols:
                    action = st.selectbox(f"Select action for column {col_name}:", ["Delete Column", "Fill with Value"])
                    if action == "Delete Column":
                        df = df.drop(columns=col_name)
                    elif action == "Fill with Value":
                        filler_value = st.text_input(f"Fill missing values for column {col_name} with:")
                        df[col_name] = df[col_name].fillna(filler_value)
                        
else:
    st.write("No missing values were found in the dataframe. Moing to the next step...")


# Section 5: Integer to decimal conversion and vice versa
st.subheader('4. Integer to decimal conversion and vice versa')
st.markdown('<a name="convert-int-to-decimal"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for integer to decimal conversion...

selected_option_convert = st.selectbox("Would you like to convert data type in your file?", ["YES", "NO"])

if selected_option_convert == "YES":
    selected_conversion_type = st.selectbox("What conversion type would you like to perform?", ["Convert to Integers", "Convert to Floats", "Convert to Strings"])
    if selected_conversion_type == "Convert to Floats":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        columns_to_convert_split = columns_to_convert.split(",")
        df[columns_to_convert_split] = df[columns_to_convert_split].astype(float)
        df
        
    elif selected_conversion_type == "Convert to Integers":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        columns_to_convert_split = columns_to_convert.split(",")
        df[columns_to_convert_split] = df[columns_to_convert_split].astype(int)
        df
    
    elif selected_conversion_type == "Convert to Strings":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        columns_to_convert_split = columns_to_convert.split(",")
        df[columns_to_convert_split] = df[columns_to_convert_split].astype(str)
        df
    
else:
    st.write("We will NOT be converting data types in your file")


# Section 6: Split or concatenate columns
st.subheader('5. Split or concatenate columns')
st.markdown('<a name="split-concatenate-columns"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for splitting or concatenating columns...



# Section 7: Convert dates to gene names
st.subheader('6. Converting dates to gene names in transcriptomic datafiles')
st.markdown('<a name="convert-dates-to-gene-names"></a>', unsafe_allow_html=True)  # Create an anchor for this section

st.write("If you want to perform a Date-to-Gene conversion in your file, you can click the link below to launch the Date-to-Gene tool made by Dr. Chan Kuan Rong")

st.write("https://share.streamlit.io/kuanrongchan/date-to-gene-converter/main/date_gene_tool.py")
