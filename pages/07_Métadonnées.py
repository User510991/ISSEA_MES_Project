import streamlit as st
import openpyxl

# Titre de l'application Streamlit
st.title("Afficher un tableau Excel sur Streamlit")

# Charger le fichier Excel



    # Charger le fichier Excel avec openpyxl
workbook = openpyxl.load_workbook("https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Livre.xlsx")

    # Sélectionner la première feuille (ou une feuille spécifique)
sheet = workbook.active  # Ou sheet = workbook['Nom_de_la_feuille']

    # Créer une liste pour stocker les données du tableau
data = []

    # Lire les lignes de la feuille Excel
for row in sheet.iter_rows(values_only=True):
  data.append(row)

    # Afficher les données dans un tableau Streamlit
st.table(data)
