import streamlit as st
import pandas as pd

# Add a title to your web app
st.title("Excel Data Cleaning Tool")

# Create a folder-like button for file upload
uploaded_file = st.file_uploader("📂 Upload an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    # Load the Excel file into a Pandas DataFrame
    df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview:")
    st.write(df)

    st.subheader("Data Cleaning Options:")

    # User selects whether to split or concatenate
    operation = st.selectbox("Choose operation:", ["Split", "Concatenate"])

    if operation == "Split":
        st.subheader("Split Data")

        # Get user input for columns to split
        split_columns = st.multiselect("Select columns to split:", df.columns)

        # Get user input for separator
        separator = st.text_input("Specify the separator:", "/")

        if st.button("Split"):
            # Split selected columns and create new rows
            for col in split_columns:
                df = df.assign(**{f"{col}_split": df[col].str.split(separator)})
                df = df.explode(f"{col}_split")

            st.subheader("Split Data Result:")
            st.write(df)

    elif operation == "Concatenate":
        st.subheader("Concatenate Data")

        # Get user input for columns to concatenate
        concat_columns = st.multiselect("Select columns to concatenate:", df.columns)

        # Get user input for separator
        separator = st.text_input("Specify the separator:", "/")

        if st.button("Concatenate"):
            # Concatenate selected columns into a new column
            df["Concatenated_Column"] = df[concat_columns].astype(str).agg(separator.join, axis=1)
            st.subheader("Concatenated Data Result:")
            st.write(df)

    # Allow the user to download the modified DataFrame as an Excel file
    st.subheader("Download Processed Data")
    st.write("You can download the processed data as an Excel file.")
    st.markdown(get_binary_file_downloader_html(df), unsafe_allow_html=True)

# Function to create a download link for the processed data
def get_binary_file_downloader_html(df):
    csv = df.to_excel(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/excel;base64,{b64}" download="cleaned_data.xlsx">Download Excel File</a>'
    return href
