# Libraries
import numpy as np
import pandas as pd
import streamlit as st
import scipy.stats as sp
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io

# Webtool sidebar
st.title('Data cleaning webtool')

st.sidebar.header('Welcome to the data cleaning webtool')
st.sidebar.write('Easily scroll through the webtool by pressing the link below')
st.sidebar.markdown('[Uploading your datafile](#upload-anchor)') 
st.sidebar.markdown('[Managing duplicate values](#manage-duplicates)')
st.sidebar.markdown('[Managing missing values](#manage-missing)')
st.sidebar.markdown('[Data type converter](#convert-int-to-decimal)')
st.sidebar.markdown('[Split or concatenate columns](#split-concatenate-columns)')
st.sidebar.markdown('[Date-to-Gene converter](#convert-dates-to-gene-names)')  # Provided the link to the gene-to-date converter
show_docs = st.sidebar.checkbox('**Check documentation**', value = True)  # Need to add more documentation - complete demo with snapshots  

# Section 1:  Doucmentation
if show_docs:
    st.header("Webtool user manual")
    st.subheader("Data cleaning webtool is a web tool that serves as a one-stop solution to clean larg datafiles produced from your research. ")
    st.write("With this webtool, you can perform some common data cleaning procedures by simply uploading your file and selecting how you would like your data to be cleaned.")
    st.write("Currently, we offer the following functions:")
    st.write("1. Duplicate value management")
    st.write("2. Missing value management")
    st.write("3. Data type conversion")
    st.write("4. Column splitting and concatenation")
    st.subheader("How do I use this web tool?")
    st.subheader("Getting started")
    st.write("To get yourself started, first you should choose a data file type that you want to be cleaned. We allow you to upload .xls, .xlsx, .csv, and .tsv files. Make sure that your file is of long format instead of a wide format. If you have not uploaded your file, an example file is already loaded. So you can still explore the functions of this webtool and check out what best suits the needs for your data.")
    st.subheader('Navigation')
    st.write('You can navigate through the webtool by scrolling up and down the main title page. For easy navigation, we have the main headings and a few notes on the datafile tagged in the sidebar on the left for easy access to the file section!')
    st.subheader("Functions")
    st.write("1. Duplicate value management")
    st.write("This function is performed automatically without you having to manually manage the data. You will be able to choose the column to check duplicate values from a dropdown menu. The detected duplicate values will be returned back to you. Next, you choose how you wish to handle the detected duplicates. You can take the mean value of each of the duplicate rows, keep the first row, keep the last row, or simply ignore it.")
    st.write("2. Missing value management")
    st.write("This function is also performed automatically. It will identify rows with empty cells and have you to decide how you would like to manage those missing values. You can delete those rows or fill in a placeholder value for all of them. This is useful since a lot of downatream processing may have issues if there are empty cells")
    st.write("3. Data type converter")
    st.write("This function allows you to convert data types of specific rows into integers, floats, or strings. You need to choose whether you wish to initiate this function first with a dropdown menu. Then simply choose what data types you want the columns to be converted to and the names of the columns to convert.")
    st.write("4. Split or concatenate columns")
    st.write("This function allows you to either split or concatenate columns. You need to choose whether you wish to initiate this function first with a dropdown menu. Then you can choose whether you want to perform a split, a concatenation, or both. Additionally post-splitting, you can choose which columns you want to keep and which columns you want to delete.")
    st.subheader("Save your file")
    st.write("After all the functions are successfully performed, you can save your cleaned file by clicking 'Download Excel File'. And you are good to perform your downstream processes on your clean date file!")
    st.subheader("Extra resources")
    st.write("Finally, to pay homage to our greatest lecturer ever, Dr. Chan Kuan Rong, we have included a link to his webtool where you can convert dates that were converted automatically from gene names by Excel back to the original gene names but with the new approved format of gene names that even Excel cannot tamper with. You can download your clean file and proceed to the Date-to-Gene tool with the included link if you so wish. Do check out the documentation in their webtool for more information.")
    st.write("This webtool was made as part of an assignment for the DUke NUS Medical School, GMS6907 module. Creators: Shree Pooja, Qing Xin, Vinaya Venkat, He Shan")
    
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
    url = "https://raw.githubusercontent.com/VinayaVenkat26/GSMV6907-Group1/main/Data_cleaning_webtool/Streamlit_demo_dataset.xlsx"
    df = pd.read_excel(url,index_col = 0) 
    st.write('No file uploaded. Showing example data.')
    st.write(df)
    
   



# Section 3: Check for duplicate values in row titles
st.markdown('<a name="manage-duplicates"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('2. Managing duplicate values')

# Function to check for duplicates in a specified column or index
def check_duplicates_in_column_or_index(df, column_name, use_index=False):
    if df is not None and not df.empty:
        if use_index:
            index_dups = df.index.duplicated().any()
            if index_dups:
                duplicated_values = df[df.index.duplicated(keep=False)]
                st.write('Duplicate values in index:')
                st.write(duplicated_values)
                return 'Duplicate values in index found.', duplicated_values
            else:
                return 'No duplicate values in index were found.'
        else:
            if column_name in df.columns:
                col_dups = df[column_name].duplicated().any()
                if col_dups:
                    duplicated_values = df[df[column_name].duplicated(keep=False)]
                    st.write(f'Duplicate values in column "{column_name}":')
                    duplicates_only_df = st.write(duplicated_values)
                    return f'Duplicate values in column "{column_name}" found.'
                else:
                    return f'No duplicate values in column "{column_name}" were found.', duplicated_values
            else:
                return f'Column "{column_name}" not found in the DataFrame.'

# Function to handle duplicates in a specified column or index
def handle_duplicates_in_column_or_index(df, column_name, selected_action, use_index=False):
    handled_successfully = False  # Initialize a flag

    if df is not None and not df.empty:
        if use_index:
            if selected_action == 'Choose only the first value':
                df = df.loc[~df.index.duplicated(keep='first')]
                st.write('Only the first value in index kept.')
                handled_successfully = True  # Set the flag to True
            elif selected_action == 'Choose only the last value':
                df = df.loc[~df.index.duplicated(keep='last')]
                st.write('Only the last value in index kept.')
                handled_successfully = True  # Set the flag to True
            elif selected_action == 'Ignore':
                st.write('No action taken for duplicates in index.')

        else:
            if selected_action == 'Take mean of duplicates':
                # indicating duplicated values
                duplicated_values = df[df[column_name].duplicated(keep=False)]
                #creating a mask to stire index position
                mask = df[column_name].duplicated(keep='first')
                df = df[~mask]
                # Now I will have to take the mean of the rows in duplicated vlaues, checking columns one by one for integer values

                # Function to check if a column is numeric
                def is_numeric(column):
                    numeric_types = [int, float, np.number]
                    return column.dtype in numeric_types
                # Iterate through the columns in duplicated_values
                for column in duplicated_values.columns:
                    if is_numeric(duplicated_values[column]):
                    # Calculate the mean for numeric columns and store it in the first row
                        duplicated_values.at[0, column] = duplicated_values[column].mean()
                else:
                    # For non-numeric columns, keep the first occurrence
                    duplicated_values[column] = duplicated_values[column].iloc[0]

                # The result will be a row in duplicated_values with means for numeric columns and the first occurrence for non-numeric columns.

                st.write(duplicated_values)
                st.write(f'Mean of duplicates in column "{column_name}" taken.')
                handled_successfully = True  # Set the flag to True
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
index_name = df.index.name if df.index.name else "[Index]"
all_columns_plus_index = list(df.columns) + [index_name]

selected_column_or_index = st.selectbox('Select a column or the index to check for duplicates:', all_columns_plus_index)

use_index = (selected_column_or_index == index_name)
if use_index:
    st.write(check_duplicates_in_column_or_index(df, None, use_index=True))
else:
    st.write(check_duplicates_in_column_or_index(df, selected_column_or_index, use_index=False))

# b. Handle duplicates
if st.checkbox('Handle duplicates in this column or index'):
    if use_index:
        selected_action = st.selectbox(
            'How would you like to handle duplicates in the index?',
            ('Choose only the first value', 'Choose only the last value', 'Ignore')
        )
    else:
        selected_action = st.selectbox(
            f'How would you like to handle duplicates in column "{selected_column_or_index}"?',
            ('Take mean of duplicates', 'Choose only the first value', 'Choose only the last value', 'Ignore')
        )
    df, handled_successfully = handle_duplicates_in_column_or_index(df, selected_column_or_index, selected_action, use_index)
    if handled_successfully:
        st.subheader("Cleaned DataFrame:")
        st.dataframe(df)
    else:
        st.write('Error')



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
    columns_to_convert = st.multiselect("Select the columns to convert:", df.columns)

    if columns_to_convert:
        if selected_conversion_type == "Convert to Floats":
            df[columns_to_convert] = df[columns_to_convert].astype(float)

        elif selected_conversion_type == "Convert to Integers":
            # Check for NaN or infinite values in the columns
            if df[columns_to_convert].isnull().any().any() or np.isinf(df[columns_to_convert]).any().any():
                action = st.radio("NaN or infinite values detected. How would you like to handle them?",
                                  ["Replace with specific value", "Drop rows containing NaN or inf", "Do nothing"])
                if action == "Replace with specific value":
                    replace_val = st.number_input("Enter the value to replace NaN or infinite values with:", value=0)
                    df[columns_to_convert] = df[columns_to_convert].fillna(replace_val).replace([np.inf, -np.inf], replace_val)
                elif action == "Drop rows containing NaN or inf":
                    df.dropna(subset=columns_to_convert, inplace=True)
                    df = df[~np.isinf(df[columns_to_convert]).any(axis=1)]
            df[columns_to_convert] = df[columns_to_convert].astype(int)

        elif selected_conversion_type == "Convert to Strings":
            df[columns_to_convert] = df[columns_to_convert].astype(str)

        st.write(df)
    else:
        st.write("Please select the columns you wish to convert.")

else:
    st.write("We will NOT be converting data types in your file.")



# Section 6: Split or concatenate columns
st.markdown('<a name="split-concatenate-columns"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('5. Split or concatenate columns')

# Code for splitting or concatenating columns

selected_option_splitconcat = st.selectbox("Would you like to split or concatenate columns in your file?", ["NO", "YES"])

if selected_option_splitconcat == "YES":

    st.subheader('Options:')
    operation = st.radio("Select an action:", ("Split", "Concatenate", "Both"))

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

    elif operation == "Concatenate":
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
        
    else:
            # Do both
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
        merged_df_split = pd.concat([df, split_values], axis=1)
        st.write(merged_df_split)
        
        # Concatenate columns
        st.subheader("Concatenate Columns")
        st.write("Select the columns to concatenate:")
        concat_columns = st.multiselect("Columns to concatenate:", merged_df_split.columns)
        separator = st.text_input("Separator for concatenation:", " ")
        concat_df = merged_df_split[concat_columns].astype(str).agg(separator.join, axis=1)

            # Display the concatenated values along with the original dataset
        st.write("Concatenated Values")
        st.write(concat_df)
        st.write("Merged Dataset with Concatenated Column")
        merged_df = pd.concat([merged_df_split, concat_df.rename("Concatenated_Column")], axis=1)
        st.write(merged_df)

        # Set the value of the action variable
    action = st.radio("Choose action:", ("Keep Selected Columns", "Delete Selected Columns"))
    
        # Continue with the action based on the user's choice
    if action == "Keep Selected Columns":
        columns_to_keep = st.multiselect("Please select all columns to keep:", merged_df.columns)
        result_df = merged_df[columns_to_keep]
    else:
        columns_to_delete = st.multiselect("Please select all columns to delete:", merged_df.columns)
        result_df = merged_df.drop(columns=columns_to_delete)


    # Display the resulting dataset
        st.subheader("Resulting Dataset")
        st.write(result_df)

else:
    st.write("We will NOT be splitting or concatenating columns in your file.")
    result_df = df
    

# Section 7: Conclusion , retieving the data from the webtool

# Function to create a download link for the processed data

def get_binary_file_downloader_html(df):

    # Create a BytesIO object to store the Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=True)
    
    b64 = base64.b64encode(output.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="cleaned_data.xlsx">Download Excel File</a>'
    return href

st.subheader('All done!!')
st.write('Your datafile has been cleaned')
st.write("You can download the processed data as an Excel file.")
st.markdown(get_binary_file_downloader_html(result_df), unsafe_allow_html=True)


# Section 8: Convert dates to gene names
st.markdown('<a name="convert-dates-to-gene-names"></a>', unsafe_allow_html=True)  # Create an anchor for this section
st.subheader('Extra resource -  Date-to-Gene Tool')

st.write("If you want to perform a Date-to-Gene conversion in your file (especially if you have gene names in your excel datafile), you can click the link below to launch the Date-to-Gene tool made by Dr. Chan Kuan Rong")

st.write("https://share.streamlit.io/kuanrongchan/date-to-gene-converter/main/date_gene_tool.py")
