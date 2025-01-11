import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import subprocess
import tempfile
import rpy2.robjects as ro

# Définir le script R pour installer les packages nécessaires
install_r_packages = """
install.packages(c("moments", "urca", "readxl", "tseries", "ggplot2", "FinTS", 
                   "caschrono", "nortest", "lmtest", "strucchange", "vars", 
                   "dynlm", "tsDyn", "dLagM", "dynamac", "TSstudio", "ARDL", 
                   "TSA", "car", "nardl", "CPAT", "systemfit", "AER", "foreign", 
                   "xtable", "stargazer", "timeSeries", "Hmisc", "texreg", "forecast"))
"""

def remove_column_spaces(df):
    """
    Enlève tous les espaces entourant les noms des colonnes d'un DataFrame.

    Paramètre :
    - df : pandas.DataFrame

    Retourne :
    - pandas.DataFrame avec les noms de colonnes nettoyés
    """
    df.columns = df.columns.str.strip()
    return df
# Exécuter le script R pour installer les packages
#ro.r(install_r_packages)
def create_lag_column(df, column_name, lag, new_column_name=None):
    """
    Crée une colonne retardée d'ordre `lag` à partir d'une colonne existante.
    
    Args:
        df (pd.DataFrame): Le DataFrame d'entrée.
        column_name (str): Le nom de la colonne à décaler.
        lag (int): L'ordre du retard (nombre de lignes à décaler).
        new_column_name (str, optional): Le nom de la nouvelle colonne. Si None, le nom sera généré automatiquement.
    
    Returns:
        pd.DataFrame: Le DataFrame avec la nouvelle colonne ajoutée.
    """
    if new_column_name is None:
        new_column_name = f"{column_name}{lag}"
    
    df[new_column_name] = df[column_name].shift(lag)
    return df

def plot_predictions(data, title, variable, confidence_lower, confidence_upper):
    fig = go.Figure()

    # Ligne de prédiction
    fig.add_trace(go.Scatter(
        x=data['Date'], 
        y=data[variable],
        mode='lines',
        name='Prédiction',
        line=dict(color='blue')
    ))

    # Bande d'incertitude
    fig.add_trace(go.Scatter(
        x=pd.concat([data['Date'], data['Date'][::-1]]),
        y=pd.concat([data[confidence_upper], data[confidence_lower][::-1]]),
        fill='toself',
        fillcolor='rgba(0, 0, 255, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        name='Intervalle de confiance'
    ))

    # Mise en forme du graphique
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title=variable,
        legend_title="Légende",
        template="plotly_white"
    )

    return fig

def add_rows_with_tail_values(df, num_rows):
    """Adds rows to the DataFrame with the same values as the tail.

    Args:
        df: The input DataFrame.
        num_rows: The number of rows to add.

    Returns:
        A new DataFrame with the added rows.
    """

    if num_rows <= 0 :
      return df
    
    tail_row = df.tail(1)
    new_rows = pd.concat([tail_row] * num_rows,ignore_index=True)
    return pd.concat([df, new_rows])

url="https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F2.csv"
df = pd.read_csv(url,sep=";",decimal=",")
df = df.set_index('Annee')
df_new=df#.iloc[-1:]
last_index = df.index[-1]
liste_exp=[l for l in df.columns if l != "Annee" ]# if l not in ["PIB_hbt", "CO2","Renouv","Annee"]]
prediction_period = st.sidebar.slider("Nombre de périodes pour la prédiction", 1, 20, 10)
st.sidebar.subheader("Variables Explicatives")
selected_vars = st.sidebar.multiselect("Sélectionnez les variables à modifier", liste_exp)
# Example usage
# Add 3 rows with the same values as the last row of df
df_extended = add_rows_with_tail_values(df, int(prediction_period))
df_init=df_extended#.iloc[-int(prediction_period):]
a=1
if selected_vars:
  for j in selected_vars:
      st.subheader(j)
      # Demander combien de nombres l'utilisateur veut entrer
      num_entries = st.number_input("Sur combien d'années portent vos renseignement ?", min_value=0, max_value=int(prediction_period), value=0)
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
      
  df_new["log_Bext"]=np.log(-df_new["bal_ext_BS "])
  df_new["log_PIB_hbt"]=np.log(df_new["PIB_hbt"])
  df_new["log_fbcf"]=np.log(df_new["FBCF"])
  df_new["log_Irenouv"]=np.log(df_new["Imp_renouv"])
  df_init["log_Bext"] = np.log(-df_init["bal_ext_BS "])
  df_init["log_fbcf"] = np.log(df_init["FBCF"])
  df_init["log_Irenouv"] = np.log(df_init["Imp_renouv"])
  df_init["log_PIB_hbt"]=np.log(df_init["PIB_hbt"])
  
  
  # Remplacement des NaN par la dernière valeur valide
  col_names=[i for i in df_new.columns if i not in ["FBCF","Imp_renouv","bal_ext_BS "]]
  columns_tofill=[i for i in col_names if  i not in ["log_PIB_hbt","PIB_hbt", "CO2","Renouv"]]
  df_filled=df_new.copy()
  df_filled[columns_tofill] = df_new[columns_tofill].fillna(method='ffill')
  df_init1=df_init.copy()
  df_init1[columns_tofill] = df_init[columns_tofill].fillna(method='ffill')
  df_filled[["inflat","chom","co2","ef_ser","esp_vie","renouv"]]=df_filled[["Inflat","Chomage","CO2","effet_serre","Esp_vie","Renouv"]]
  df_init1[["inflat","chom","co2","ef_ser","esp_vie","renouv"]]=df_init1[["Inflat","Chomage","CO2","effet_serre","Esp_vie","Renouv"]]

  col_names=[i for i in df_filled.columns if i not in ["FBCF","Imp_renouv","bal_ext_BS ","Inflat","Chomage","CO2","effet_serre","Esp_vie","Renouv"]]
  for vari in col_names:
    for i in range(1,6):
      df_filled=create_lag_column(df_filled, vari, i)
      df_init1=create_lag_column(df_init1, vari, i)

  col_names=[i for i in df_filled.columns if i not in ["FBCF","Imp_renouv","bal_ext_BS ","Inflat","Chomage","CO2","effet_serre","Esp_vie","Renouv"]]
  df_a=df_init1[col_names]#remove_column_spaces(df_init1[col_names])
  df_t=df_filled[col_names]#remove_column_spaces(df_filled[col_names])
  st.dataframe(df_t)
  st.dataframe(df_a)
  df_t.to_csv('data_new.csv', index=True)
  df_a.to_csv('data_new_init.csv', index=True)
  
  
  # Spécifier le chemin du script R
  script_r = 'pages/script.R'  # Nom de votre script R
  a=0
  # Appeler le script R avec les variables en argument
  try:
      # Appeler le script R
      result = subprocess.run(["Rscript", script_r], check=True, capture_output=True, text=True)
      st.success("Script R exécuté avec succès. Fichier CSV généré.")
      a=1
      st.write(f"Fichier sauvegardé : {file_path}")
  except subprocess.CalledProcessError as e:
      st.error(f"Erreur lors de l'exécution du script R : {e.stderr}")
      a=0
  if a:
    print(result)
    df_predictions_initial= pd.read_csv("predictions_initial.csv")
    df_predictions_modified = pd.read_csv("predictions_modified.csv")
    df_impact = pd.read_csv("impact.csv")
    
    # Exponentier log_pib_hab pour obtenir pib/hab
    df_predictions_initial['pib_hab'] = np.exp(df_predictions_initial['log_pib_hab'])
    df_predictions_modified['pib_hab'] = np.exp(df_predictions_modified['log_pib_hab'])
    
    # Fonction pour tracer les graphiques avec Plotly
  
    
    # Interface Streamlit
    st.title("Visualisation des prédictions 3SLS")
    
    # Options pour sélectionner l'équation
    equation = st.selectbox("Choisissez l'équation à visualiser :", ["PIB/hab", "CO2", "Renouv"])
    
    # Filtrer et afficher les données en fonction de l'équation sélectionnée
    if equation:
      if equation == "PIB/hab":
        st.subheader("Prédictions pour PIB/hab")
        fig_initial = plot_predictions(df_predictions_initial, "Prédictions Initiales - PIB/hab", 
                                          'pib_hab', 'pib_hab_lower', 'pib_hab_upper')
        st.plotly_chart(fig_initial, use_container_width=True)
    
        fig_modified = plot_predictions(df_predictions_modified, "Prédictions Modifiées - PIB/hab", 
                                         'pib_hab', 'pib_hab_lower', 'pib_hab_upper')
        st.plotly_chart(fig_modified, use_container_width=True)
    
      elif equation == "CO2":
          st.subheader("Prédictions pour CO2")
          fig_initial = plot_predictions(df_predictions_initial, "Prédictions Initiales - CO2", 
                                          'Co2', 'Co2_lower', 'Co2_upper')
          st.plotly_chart(fig_initial, use_container_width=True)
      
          fig_modified = plot_predictions(df_predictions_modified, "Prédictions Modifiées - CO2", 
                                           'Co2', 'Co2_lower', 'Co2_upper')
          st.plotly_chart(fig_modified, use_container_width=True)
      
      elif equation == "Renouv":
          st.subheader("Prédictions pour Renouv")
          fig_initial = plot_predictions(df_predictions_initial, "Prédictions Initiales - Renouv", 
                                          'Renouv', 'Renouv_lower', 'Renouv_upper')
          st.plotly_chart(fig_initial, use_container_width=True)
      
          fig_modified = plot_predictions(df_predictions_modified, "Prédictions Modifiées - Renouv", 
                                           'Renouv', 'Renouv_lower', 'Renouv_upper')
          st.plotly_chart(fig_modified, use_container_width=True)

  # Afficher l'impact
    st.subheader("Impact des prédictions")
    st.dataframe(df_impact)
