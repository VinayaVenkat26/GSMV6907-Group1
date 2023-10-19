# Webtool user manual
##### Data cleaning webtool is a web tool that serves as a one-stop solution for your large data files from your research

With this webtool, you can perform some common data cleaning procedures by simply uploading your file and selecting how you would like your data to be cleaned.

Currently, we offer the following functions:
1. Duplicate value management
2. Missing value management
3. Data type conversion
4. Column splitting and concatenation

## How do I use this web tool?

### Getting started
To get yourself started, first you should choose a data file type that you want to be cleaned. We allow you to upload .xls, .xlsx, .csv, and .tsv files. 
Make sure that your file is of long format instead of a wide format. 
If you have not uploaded your file, an example file is already loaded. 
So you can still explore the functions of this webtool and check out what best suits the needs for your data.

### Navigation 
You can navigate through the webtool by scrolling up and down the main title page. 
For easy navigation, we have the main headings and a few notes on the datafile tagged in the sidebar on the left for easy access to the file section!

### Functions
  #### 1. Duplicate value management
    This function is performed automatically without you having to manually manage the data. 
    You will be able to choose the column to check duplicate values from a dropdown menu. 
    The detected duplicate values will be returned back to you. 
    Next, you choose how you wish to handle the detected duplicates. 
    You can take the mean value of each of the duplicate rows, keep the first row, keep the last row, or simply ignore it.
    
  #### 2. Missing value management
    This function is also performed automatically. 
    It will identify rows with empty cells and have you to decide how you would like to manage those missing values. 
    You can delete those rows or fill in a placeholder value for all of them. 
    This is useful since a lot of downatream processing may have issues if there are empty cells
    
  #### 3. Data type converter
    This function allows you to convert data types of specific rows into integers, floats, or strings. 
    You need to choose whether you wish to initiate this function first with a dropdown menu. 
    Then simply choose what data types you want the columns to be converted to and the names of the columns to convert.
    
  #### 4. Split or concatenate columns
    This function allows you to either split or concatenate columns. 
    You need to choose whether you wish to initiate this function first with a dropdown menu. 
    Then you can choose whether you want to perform a split, a concatenation, or both. 
    Additionally post-splitting, you can choose which columns you want to keep and which columns you want to delete.
    
  ### Save your file
    After all the functions are successfully performed, you can save your cleaned file by clicking 'Download Excel File'. 
    And you are good to perform your downstream processes on your clean date file!
    
  ### Extra resources
    "Finally, to pay homage to our greatest lecturer ever, Dr. Chan Kuan Rong, we have included a link to his webtool where you can convert dates that were converted automatically from gene names by Excel back to the original gene namesbut with the new approved format of gene names that even Excel cannot tamper with.
    You can download your clean file and proceed to the Date-to-Gene tool with the included link if you so wish. 
    Do check out the documentation in their webtool for more information.
    
  This webtool was made as part of an assignment for the DUke NUS Medical School, GMS6907 module. Creators: Shree Pooja, Qing Xin, Vinaya Venkat, He Shan
    
