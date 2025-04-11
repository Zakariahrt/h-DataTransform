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
def handle_duplicates(df, duplicates_file_path):
    """Save duplicated rows to a file and return a DataFrame without duplicates."""
    duplicated_df = df[df.duplicated()]
    df_cleaned = df.drop_duplicates()
    
    if not duplicated_df.empty:
        save_csv(duplicated_df, duplicates_file_path)
        print(f"Removed {len(duplicated_df)} duplicate rows. Duplicates saved to {duplicates_file_path}.")
    else:
        print("No duplicate rows found.")
    
    return df_cleaned    
