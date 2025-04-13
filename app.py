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
# Merge data for comprehensive patient information
merged_data = encounters.merge(patients, left_on='PATIENT', right_on='Id', suffixes=('_encounter', '_patient'))
 
# Title
st.title("Patient Health Information")
 
# Sidebar for user input
st.sidebar.header("Search Patient")
 
# Search by Patient ID
patient_id = st.sidebar.text_input("Enter Patient ID")
 
if patient_id:
    # Filter data based on Patient ID
    patient_data = merged_data[merged_data['Id_patient'] == patient_id]
   
    if not patient_data.empty:
        st.subheader("Patient Information")
        st.write(patient_data[['FIRST', 'LAST', 'BIRTHDATE', 'GENDER']])
       
        st.subheader("Medical History")
        st.write("Medical history is not included in the provided data.")
       
        st.subheader("Recent Visits")
        st.write(patient_data[['START', 'STOP']])
       
        st.subheader("Medications")
        st.write("Medications are not included in the provided data.")
       
        st.subheader("Hospital Stay Duration (hours)")
        stay_duration = (pd.to_datetime(patient_data['STOP']) - pd.to_datetime(patient_data['START'])).dt.total_seconds() / 3600
        st.write(stay_duration.values)
       
        st.subheader("Visit Cost")
        try:
            visit_cost = pd.to_numeric(patient_data['TOTAL_CLAIM_COST']).sum()
            st.write(f"${visit_cost:.2f}")
        except ValueError as e:
            st.warning(f"Error calculating visit cost: {e}")
       
        st.subheader("Procedures Covered by Insurance")
        covered_by_insurance = procedures[procedures['ENCOUNTER'].isin(patient_data['Id']) & (encounters['PAYER'] != "b1c428d6-4f07-31e0-90f0-68ffa6ff8c76")]['BASE_COST'].sum()
        st.write(covered_by_insurance)
    else:
        st.warning("No patient found with the given ID.")
 
# Additional feature: List all patients
st.sidebar.header("List of All Patients")
if st.sidebar.button("Show All Patients"):
    st.subheader("All Patients")
    st.write(patients)
 
# Additional feature: Search by Name
st.sidebar.header("Search by Name")
patient_name = st.sidebar.text_input("Enter Patient Name")
 
if patient_name:
    # Filter data based on Patient Name
    patient_data = merged_data[merged_data['FIRST'].str.contains(patient_name, case=False, na=False) | merged_data['LAST'].str.contains(patient_name, case=False, na=False)]
   
    if not patient_data.empty:
        st.subheader("Patient Information")
        st.write(patient_data)
    else:
        st.warning("No patient found with the given name.")
 
# Calculate and display average statistics
st.sidebar.header("Statistics")
 
if st.sidebar.button("Show Statistics"):
    st.subheader("Average Hospital Stay Duration (hours)")
    avg_stay = (pd.to_datetime(encounters['STOP']) - pd.to_datetime(encounters['START'])).dt.total_seconds().mean() / 3600
    st.write(f"{avg_stay:.2f} hours")
   
    st.subheader("Average Cost per Visit")
    try:
        avg_cost = pd.to_numeric(encounters['TOTAL_CLAIM_COST']).mean()
        st.write(f"${avg_cost:.2f}")
    except ValueError as e:
        st.warning(f"Error calculating average cost per visit: {e}")
   
    st.subheader("Number of Procedures Covered by Insurance")
    covered_encounters = encounters[encounters['PAYER'] != "b1c428d6-4f07-31e0-90f0-68ffa6ff8c76"]
    num_covered = procedures[procedures['ENCOUNTER'].isin(covered_encounters['Id'])].shape[0]
    st.write(num_covered) 

