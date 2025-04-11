import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

"""DEFINE FUNCTIONS"""
def affich():
   print('is working')

def  load_csv(patth,delimiter=',', encoding='utf-8'):
    df = pd.read_csv(patth,delimiter=delimiter, encoding=encoding)
    return df
def missing_value(df):
  missing_value=df.isnull().sum()
  return missing_value

def fillna_with_prefix(df):
    """
    Fill missing values in the 'GENDER' column using the 'PREFIX' column.
    'Mrs.', 'Ms.' -> 'female'
    'Mr.' -> 'male'
    """
    # Define a mapping from PREFIX to GENDER
    prefix_to_gender = {
        'Mrs.': 'F',
        'Ms.': 'F',
        'Mr.': 'M'
    }
    
    # Apply the mapping to fill missing values in the GENDER column
    df['GENDER'] = df.apply(
        lambda row: prefix_to_gender[row['PREFIX']] if pd.isnull(row['GENDER']) else row['GENDER'],
        axis=1
    )
    
    return df

def clean_dates(df, date_columns):
    for column, date_format in date_columns.items():
        if column in df.columns:
            # Replace '|' with '-' if necessary
            df[column] = df[column].astype(str).str.replace('|', '-')
            
            # Convert to datetime with specified format
            df[column] = pd.to_datetime(df[column], format=date_format, errors='coerce')
    
    return df