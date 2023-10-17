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
st.sidebar.markdown('3. [Date type converter](#convert-int-to-decimal)')
st.sidebar.markdown('4. [Split or concatenate columns](#split-concatenate-columns)')
st.sidebar.markdown('5. [Date-to-Gene converter](#convert-dates-to-gene-names)')  # Provided the link to the gene-to-date converter
st.sidebar.markdown('To upload your data, click [here](#upload-anchor)')  # Managed to override the error when no file is uploaded
st.sidebar.checkbox('Check documentation')  # Need to add more documentation - complete demo with snapshots  


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

# Section 3: Check for duplicate values in row titles
st.subheader('2. Managing duplicate values in row titles')
st.markdown('<a name="manage-duplicates"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Function to check for duplicates in a specified column
def check_duplicates_in_column(df, column_name):
    if df is not None and not df.empty:  # Check if df is not None and not empty
        if column_name in df.columns:
            col_dups = df[column_name].duplicated().any()
            if col_dups:
                duplicated_values = df[df[column_name].duplicated(keep=False)]
                st.write(f'Duplicate values in column "{column_name}":')
                st.write(duplicated_values)
                return f'Duplicate values in column "{column_name}" found.'
            else:
                return f'No duplicate values in column "{column_name}" were found.'
        else:
            return f'Column "{column_name}" not found in the DataFrame.'

# Function to handle duplicates in a specified column
def handle_duplicates_in_column(df, column_name, selected_action):
    if df is not None and not df.empty:  # Check if df is not None and not empty
        if column_name in df.columns:
            if selected_action == 'Take mean of duplicates':
                df[column_name] = df.groupby(column_name)[column_name].transform('mean')
                st.write(f'Mean of duplicates in column "{column_name}" taken.')
                df
            elif selected_action == 'Choose only the first value':
                df = df[~df[column_name].duplicated(keep='first')]
                st.write(f'Only the first value in column "{column_name}" kept.')
                df
            elif selected_action == 'Choose only the last value':
                df = df[~df[column_name].duplicated(keep='last')]
                st.write(f'Only the last value in column "{column_name}" kept.')
                df
            elif selected_action == 'Ignore':
                st.write(f'No action taken for duplicates in column "{column_name}".')
            return df
        else:
            st.write(f'Column "{column_name}" not found in the DataFrame.')
            return None

if df is not None and not df.empty:
    selected_column = st.selectbox('Select a column to check for duplicates:', df.columns)
    if selected_column:
        st.write(check_duplicates_in_column(df, selected_column))

        if st.checkbox('Handle duplicates in this column'):
            selected_action = st.selectbox(
                f'How would you like to handle duplicates in column "{selected_column}"?',
                ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value', 'Ignore')
            )
            if selected_action != 'Ignore':
                df = handle_duplicates_in_column(df, selected_column, selected_action)
                st.write(f'Moving on to the next step...')
    else:
        st.write('Please select a valid column.')

    df = df.loc[:, ~df.columns.duplicated(keep='last')]


# Section 4: Manage missing values

st.subheader('3. Managing missing values')
st.markdown('<a name="manage-missing"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Find rows and columns with missing values
missing_rows = df.isna().any()

# Display rows with missing values
if any(missing_rows):
    st.write("Rows with missing values:")
    st.write(df[missing_rows])
    missing_rows_indices = df[missing_rows].tolist()
    selected_rows = []  # Initialize as an empty list
    st.checkbox('Handle the missing values', value = False)

    if st.checkbox ==True :
        for row_index in missing_rows_indices:
            if row_index in selected_rows:
                action = st.selectbox(f"Select action for row {row_index}:", ["Delete Row", "Fill with Value"])
                if action == "Delete Row":
                    df = df.drop(index=row_index)
                elif action == "Fill with Value":
                    filler_value = st.text_input(f"Fill missing values for row {row_index} with:")
                    df.loc[row_index] = df.loc[row_index].fillna(filler_value)                       
else:
    st.write("No missing values were found in the dataframe. Skipping the management process.")

# Section 5: Integer to decimal conversion and vice versa
st.subheader('4. Data type converter')
st.markdown('<a name="convert-int-to-decimal"></a>', unsafe_allow_html=True)  # Create an anchor for this section

selected_option_convert = st.selectbox("Would you like to convert data types in your file?", ["NO", "YES"])

if selected_option_convert == "YES":
    selected_conversion_type = st.selectbox("What conversion type would you like to perform?", ["Convert to Integers", "Convert to Floats", "Convert to Strings"])
    if selected_conversion_type == "Convert to Floats":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        if columns_to_convert != "":
            columns_to_convert_split = columns_to_convert.split(",")
            df[columns_to_convert_split] = df[columns_to_convert_split].astype(float)
            df
        else:
            st.write("Please type the names of the columns you wish to convert above.")

    elif selected_conversion_type == "Convert to Integers":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        if columns_to_convert != "":
            columns_to_convert_split = columns_to_convert.split(",")
            df[columns_to_convert_split] = df[columns_to_convert_split].astype(int)
            df
        else:
            st.write("Please type the names of the columns you wish to convert above.")

    elif selected_conversion_type == "Convert to Strings":
        columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputing more than 1 column, e.g., apple,orange,avocado)")
        if columns_to_convert != "":
            columns_to_convert_split = columns_to_convert.split(",")
            df[columns_to_convert_split] = df[columns_to_convert_split].astype(str)
            df
        else:
            st.write("Please enter the names of the columns you wish to convert above.")

else:
    st.write("We will NOT be converting data types in your file")

# Section 6: Split or concatenate columns
st.subheader('5. Split or concatenate columns')
st.markdown('<a name="split-concatenate-columns"></a>', unsafe_allow_html=True)  # Create an anchor for this section

# Your code for splitting or concatenating columns...

# Section 7: Convert dates to gene names
st.subheader('6. Date-to-Gene Tool')
st.markdown('<a name="convert-dates-to-gene-names"></a>', unsafe_allow_html=True)  # Create an anchor for this section

st.write("If you want to perform a Date-to-Gene conversion in your file, you can click the link below to launch the Date-to-Gene tool made by Dr. Chan Kuan Rong")

st.write("https://share.streamlit.io/kuanrongchan/date-to-gene-converter/main/date_gene_tool.py")
