import streamlit as st
import pandas as pd
import os
 
# Define the directory where your CSV files are located
data_dir = 'C:/Users/User/Desktop/Data Analytics Project/Dataset/work_flow/'
# Update this with the correct path
 
def load_data(data_dir):
    encounters = pd.read_csv(os.path.join(data_dir, 'clean_encounter.csv'))
    patients = pd.read_csv(os.path.join(data_dir, 'clean_patients.csv'))
    organizations = pd.read_csv(os.path.join(data_dir, 'organizations.csv'))
    payers = pd.read_csv(os.path.join(data_dir, 'payers.csv'))
    procedures = pd.read_csv(os.path.join(data_dir, 'procedures.csv'))
    return encounters, patients, organizations, payers, procedures
 
def clean_numeric_data(df, column_name):
    df[column_name] = df[column_name].str.replace(',', '').astype(float)
    return df
 
encounters, patients, organizations, payers, procedures = load_data(data_dir)
 
# Clean the 'TOTAL_CLAIM_COST' column in encounters
encounters = clean_numeric_data(encounters, 'TOTAL_CLAIM_COST')
 

