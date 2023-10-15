import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np 
from scipy.stats import pearsonr, spearmanr

st.write('Welcome to the data cleaning webtool')
st.write('Please choose the file format you are uploading (Compatible file formats: CSV, TSV)')

file_type = st.selectbox ("Pick one", ["CSV", "TSV"])

# Conversion type selection
conversion_type = st.radio("Select conversion type", ["Integer to Decimal", "Decimal to Integer"])

#Uploading data
# File uploader widget based on selected file type
file_format = "csv" if file_type == "CSV" else "tsv"
uploaded_file = st.file_uploader(f"Upload a {file_type} file", type=[file_format])


if uploaded_file is not None:
    # Read the file into a DataFrame
    try:
        delimiter = '\t' if file_format == "tsv" else ','
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
        st.write(f"Data from the uploaded {file_type} file:")
        st.write(df)
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

# Check for missing values
    st.write("Missing Values:")
    missing_values = df.isnull().sum()
    st.write(missing_values)
    
# Check for duplicated values
    st.write("Duplicated Values:")
    duplicated_values = df[df.duplicated()]
    st.write(duplicated_values)
    
 # Perform integer to decimal or decimal to integer conversion for float columns only
    float_columns = df.select_dtypes(include=['float64']).columns

    for column in float_columns:
        if conversion_type == "Integer to Decimal":
            df[column] = df[column].astype(float)
        elif conversion_type == "Decimal to Integer":
            df[column] = df[column].apply(lambda x: int(x) if not np.isnan(x) else x)

    st.write("Converted Data:")
    st.write(df)