# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sp
import matplotlib.pyplot as plt
import seaborn as sns


# Webtool sidebar
st.title('Data cleaning webtool')
st.write('Made by Group 1: Shree Pooja, Qing Xin, Vinaya Venkat, He Shan')

st.sidebar.header('Welcome to the data cleaning webtool')
st.sidebar.write('Easily scroll through the webtool by pressing the link below')
st.sidebar.markdown('[Uploading your datafile](#upload-anchor)') 
st.sidebar.markdown('[Managing duplicate values](#manage-duplicates)')
st.sidebar.markdown('[Managing missing values](#manage-missing)')
st.sidebar.markdown('[Data type converter](#convert-int-to-decimal)')
st.sidebar.markdown('[Split or concatenate columns](#split-concatenate-columns)')
st.sidebar.markdown('[Date-to-Gene converter](#convert-dates-to-gene-names)')  # Provided the link to the gene-to-date converter
show_docs = st.sidebar.checkbox('Check documentation')  # Need to add more documentation - complete demo with snapshots  

# Section 1:  Doucmentation

docu = st.sidebar.checkbox("Documentation")
if docu:
    st.title("Data Cleaner User Manual")
    st.subheader("Data Cleaner is a web tool that serves as a one-stop solution for your large data files from your research")
    st.write("With Data Cleaner, you can perform multiple data cleaning procedures by simply uploading your file and selecting how you would like your data to be cleaned.")
    st.write("Currently, we provide the following functions:")
    st.write("1. Duplicate value management")
    st.write("2. Missing value management")
    st.write("3. Data type conversion")
    st.write("4. Column splitting and concatenation")
    st.write("5. Date-to-Gene conversion (by Dr. Chan Kuan Rong)")
    st.subheader("How do I use this web tool?")
    st.write("To get yourself started, first you should choose a data file type that you want to be cleaned. We allow you to upload .xls, .xlsx, .csv, and .tsv files. Make sure that your file is a long file instead of a wide file.")

# Section 2: Upload datafile
st.markdown('<a name="upload-anchor"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('1. Uploading your datafile')

option = st.selectbox('Please choose the file format you are uploading', ('None','Excel', 'CSV', 'TSV'))
st.write('You have selected:', option)

upload = st.file_uploader(f'Upload your file here')

st.sidebar.subheader('*Please note:*')
st.sidebar.write('*1. The webtool will consider the first column in the file as the index*')
st.sidebar.write('*2. Add an Excel file with only one sheet in it to prevent errors*')

# Convert the uploaded file to a DataFrame
df = None

if upload is not None:
    if option == 'Excel':
        df = pd.read_excel(upload, index_col = 0)
    elif option == 'CSV':
        df = pd.read_csv(upload, index_col = 0)
    elif option == 'TSV':
        df = pd.read_csv(upload, sep='\t', index_col = 0)
else:
    # Load an example datafile 
    url = "https://raw.githubusercontent.com/VinayaVenkat26/GSMV6907-Group1/main/Streamlit%20demo%20dataset.xlsx"
    df = pd.read_excel(url,index_col = 0) 
    st.write('No file uploaded. Showing example data.')
    st.write(df)
    
   



# Section 3: Check for duplicate values in row titles
st.markdown('<a name="manage-duplicates"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('2. Managing duplicate values')


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
    handled_successfully = False  # Initialize a flag

    if df is not None and not df.empty:
        if column_name in df.columns:
            if selected_action == 'Take mean of duplicates':
                if pd.api.types.is_numeric_dtype(df[column_name]):
                    df[column_name] = df.groupby(column_name)[column_name].transform('mean')
                    st.write(f'Mean of duplicates in column "{column_name}" taken.')
                    handled_successfully = True  # Set the flag to True
                else:
                    st.write(f'Column "{column_name}" is not numeric. Cannot take the mean of duplicates.')
            elif selected_action == 'Choose only the first value':
                df = df[~df[column_name].duplicated(keep='first')]
                st.write(f'Only the first value in column "{column_name}" kept.')
                handled_successfully = True  # Set the flag to True
            elif selected_action == 'Choose only the last value':
                df = df[~df[column_name].duplicated(keep='last')]
                st.write(f'Only the last value in column "{column_name}" kept.')
                handled_successfully = True  # Set the flag to True
            elif selected_action == 'Ignore':
                st.write(f'No action taken for duplicates in column "{column_name}".')

    return df, handled_successfully  # Return the DataFrame and the flag

# User selection

# a. Check duplicates
if df is not None and not df.empty:
    selected_column = st.selectbox('Select a column to check for duplicates:', df.columns)
    if selected_column:
        st.write(check_duplicates_in_column(df, selected_column))

# b. Handle duplicates
if st.checkbox('Handle duplicates in this column'):
    selected_action = st.selectbox(
                f'How would you like to handle duplicates in column "{selected_column}"?',
                ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value', 'Ignore')
    )
    if selected_action != 'Ignore':
        df, handled_successfully = handle_duplicates_in_column(df, selected_column, selected_action)
        if handled_successfully:
            st.subheader("Cleaned DataFrame:")
            df
            st.write(f'Duplicates handled successfully. Moving on to the next step...')





# Section 4: Manage missing values
st.markdown('<a name="manage-missing"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('3. Managing missing values')

def handle_missing_values(df):
    missing_rows = df[df.isnull().any(axis=1)]
    if not missing_rows.empty:
        st.write("Rows with missing values:")
        st.dataframe(missing_rows)
        
        # Add options for the user
        st.subheader("Options:")
        option = st.radio("Select an action:", ("Delete Rows with Missing Values", "Fill Missing Values"))
        
        if option == "Delete Rows with Missing Values":
            df = df.dropna(axis=0, how = 'any')
            st.write("Rows with missing values deleted.")
        else:
            # Allow the user to specify a value for filling missing values
            fill_value = st.text_input("Enter a value to fill missing values:")
            if st.button("Fill Missing Values"):
                df = df.fillna(fill_value)
                st.write("Missing values filled with the specified value.")

        # Display the cleaned DataFrame (either with deleted rows or filled values)
        st.subheader("Cleaned DataFrame:")
        st.dataframe(df)
    else:
        st.write("No rows with missing values found.")
        
    return df

# call the function
df = handle_missing_values(df)





# Section 5: Integer to decimal conversion and vice versa
st.markdown('<a name="convert-int-to-decimal"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('4. Data type converter')

selected_option_convert = st.selectbox("Would you like to convert data types in your file?", ["NO", "YES"])

if selected_option_convert == "YES":
    selected_conversion_type = st.selectbox("What conversion type would you like to perform?", ["Convert to Integers", "Convert to Floats", "Convert to Strings"])
    columns_to_convert = st.text_input("Enter the names of the columns you want to convert (separate each column name by a comma without a space if inputting more than 1 column, e.g., apple,orange,avocado)")
    
    if columns_to_convert != "":
        columns_to_convert_split = columns_to_convert.split(",")
        non_existent_columns = [col for col in columns_to_convert_split if col not in df.columns]

        if non_existent_columns:
            st.write(f"The following columns do not exist in the DataFrame: {', '.join(non_existent_columns)}")
        else:
            if selected_conversion_type == "Convert to Floats":
                df[columns_to_convert_split] = df[columns_to_convert_split].astype(float)
                st.subheader("Cleaned DataFrame:")
                df
            elif selected_conversion_type == "Convert to Integers":
                df[columns_to_convert_split] = df[columns_to_convert_split].astype(int)
                st.subheader("Cleaned DataFrame:")
                df
            elif selected_conversion_type == "Convert to Strings":
                df[columns_to_convert_split] = df[columns_to_convert_split].astype(str)
                st.subheader("Cleaned DataFrame:")
                df
    else:
        st.write("Please recheck the column name. It does not exist")
else:
    st.write("We will NOT be converting data types in your file")




# Section 6: Split or concatenate columns
st.markdown('<a name="split-concatenate-columns"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('5. Split or concatenate columns')

# Code for splitting or concatenating columns
st.subheader('Options:')
operation = st.radio("Select an action:", ("Split", "Concatenate"))

if operation == "Split":
        # Split columns
    st.subheader("Split Columns")
    column_to_split = st.selectbox("Select the column to split:", df.columns)
    separator = st.text_input("Separator for splitting:", ",")
        
        # Ensure the selected column is treated as a string before splitting
    split_values = df[column_to_split].astype(str).str.split(separator, expand=True)

        # Label the split columns with the original column name
    split_values.columns = [f"{column_to_split}_{i + 1}" for i in range(split_values.shape[1])]

        # Display the split values along with the original dataset
    st.write(split_values)
    st.write("Merged Dataset with Split Columns")
    merged_df = pd.concat([df, split_values], axis=1)
    st.write(merged_df)

else:
        # Concatenate columns
    st.subheader("Concatenate Columns")
    st.write("Select the columns to concatenate:")
    concat_columns = st.multiselect("Columns to concatenate:", df.columns)
    separator = st.text_input("Separator for concatenation:", " ")
    concat_df = df[concat_columns].astype(str).agg(separator.join, axis=1)

        # Display the concatenated values along with the original dataset
    st.write("Concatenated Values")
    st.write(concat_df)
    st.write("Merged Dataset with Concatenated Column")
    merged_df = pd.concat([df, concat_df.rename("Concatenated_Column")], axis=1)
    st.write(merged_df)

    # Set the value of the action variable
action = st.radio("Choose action:", ("Keep Selected Columns", "Delete Selected Columns"))

# Continue with the action based on the user's choice
if action == "Keep Selected Columns":
    columns_to_keep = st.multiselect("Columns to keep:", merged_df.columns)
    result_df = merged_df[columns_to_keep]
else:
    columns_to_delete = st.multiselect("Columns to delete:", merged_df.columns)
    result_df = merged_df.drop(columns=columns_to_delete)

# Display the resulting dataset
    st.subheader("Resulting Dataset")
    st.write(result_df)
    


# Section 7: Convert dates to gene names
st.markdown('<a name="convert-dates-to-gene-names"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('6. Date-to-Gene Tool')

st.write("If you want to perform a Date-to-Gene conversion in your file, you can click the link below to launch the Date-to-Gene tool made by Dr. Chan Kuan Rong")

st.write("https://share.streamlit.io/kuanrongchan/date-to-gene-converter/main/date_gene_tool.py")




# Section 8: conclusion , retieving the data from the webtool

