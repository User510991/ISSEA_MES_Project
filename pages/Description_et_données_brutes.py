import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Assuming 'df' is your DataFrame (replace with your actual DataFrame)
# Example DataFrame (replace with your actual data)
url="https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F2.csv"

df = pd.read_csv(url,sep=";",decimal=",")
df = df.set_index('Annee')

st.title("Statistiques Descriptives")

# Sidebar for table selection
selected_tables_raw = st.sidebar.multiselect("Choisir les tables", df.columns)
reverse_selected_tables =st.sidebar.checkbox("Toutes les variables sauf celles sélectionnées")
if len(selected_tables_raw):
  if reverse_selected_tables:
    selected_tables =[col for col in df.columns if col not in selected_tables_raw]
  else:
    selected_tables=selected_tables_raw
 
# Sidebar for showing all data
show_all_table= st.sidebar.checkbox("choisir toutes les variables")
if show_all_table:
  selected_tables=df.columns
show_all_data= st.sidebar.checkbox("Afficher les données brutes")
# Main content area
if len(selected_tables_raw):
  st.write("### Statistiques descriptives")
  st.write(df[list(selected_tables)].describe())  # Display basic descriptive statistics
else:
  st.warning("Veuillez sélectionner au moins une colonne pour afficher les statistiques descriptives.")
if show_all_data:
  st.write("### Données brutes")
  st.write(df[list(selected_tables)])
