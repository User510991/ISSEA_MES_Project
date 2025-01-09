import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

url="https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F2.csv"

df = pd.read_csv(url,sep=";",decimal=",")
df = df.set_index('Annee')
df_new=df.iloc[-1]
last_index = df.index[-1]
liste_exp=[l for l in df.columns if l not in ["PIB_hbt", "CO2","Renouv","Annee"]]
prediction_period = st.sidebar.slider("Nombre de périodes pour la prédiction", 1, 20, 10)
st.sidebar.subheader("Variables Explicatives")
selected_vars = st.sidebar.multiselect("Sélectionnez les variables à modifier", liste_exp)
a=1
for j in selected_vars:
    # Demander combien de nombres l'utilisateur veut entrer
    num_entries = st.number_input("Sur combien d'années portent vos renseignement ?", min_value=0, max_value=int(prediction_period), value=3)
    # Liste pour stocker les nombres
    numbers = []
    # Demander à l'utilisateur d'entrer les nombres un par un
    for i in range(num_entries):
        number = st.number_input(f"Entrez le nombre {i+1}", key=f"number_{i}")
        df_new.loc[last_index+i,j]=number
        #if j in ["FBCF","Imp_renouv"]:
        #elif j=="bal_ext_BS":
        numbers.append(number)
    if a==1:
        for i in range(num_entries,prediction_period):
            df_new.loc[last_index+i+1,j]=np.nan
        a=0
    
df_new["log_Bext"]=np.log(-df_new["bal_ext_BS"])
df_new["log_fbcf"]=np.log(df_new["FBCF"])
df_new["log_Irenouv"]=np.log(df_new["Imp_renouv"])
# Remplacement des NaN par la dernière valeur valide
df_filled = df_new.fillna(method='ffill')
col_names=[i for i in df_filled.columns if i not in ["FBCF","Imp_renouv","bal_ext_BS"]]
df_t=df_filled[col_names]
df_t.to_csv('data_new.csv', index=True)
df_predictions_initial= pd.read_csv("predictions_initial.csv")
df_predictions_modified = pd.read_csv("predictions_modified.csv")
df_impact = pd.read_csv("impact.csv")
