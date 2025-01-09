import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri

# Activer la conversion entre pandas et R
pandas2ri.activate()

# Charger les bibliothèques R nécessaires
base = importr("base")
utils = importr("utils")

# Streamlit Interface
st.title("Prédictions Basées sur un Modèle Économétrique R avec Plotly")
st.sidebar.title("Paramètres")

# Fonction pour installer un package R
def install_r_package(package_name):
    try:
        importr(package_name)
        st.write(f"Package R '{package_name}' est déjà installé.")
    except PackageNotInstalledError:
        st.write(f"Installation du package R : {package_name}...")
        ro.r(f'install.packages("{package_name}")')
        st.write(f"Package R '{package_name}' installé avec succès.")

# Liste des packages R nécessaires
required_packages = [
    "moments", "urca", "readxl", "tseries", "ggplot2", "FinTS", "caschrono", 
    "nortest", "lmtest", "strucchange", "vars", "dynlm", "tsDyn", "dLagM", 
    "dynamac", "TSstudio", "ARDL", "TSA", "car", "nardl", "CPAT", "systemfit", 
    "AER", "foreign", "xtable", "stargazer", "timeSeries", "Hmisc", "texreg", 
    "forecast"
]

# Vérifier et installer les packages R nécessaires
for package in required_packages:
    install_r_package(package)

# URL du modèle sauvegardé
url = "https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/Essaies/model_3sls.RData"

# Chemin temporaire pour sauvegarder le fichier
local_file = "model_fit.RData"

# Télécharger le fichier depuis l'URL
response = requests.get(url)
if response.status_code == 200:
    with open(local_file, "wb") as file:
        file.write(response.content)
    print(f"Fichier téléchargé et sauvegardé sous : {local_file}")
else:
    print("Erreur lors du téléchargement du fichier")
    exit(1)

# Charger le modèle R dans l'environnement
ro.r(f'load("{local_file}")')  # Charge l'objet R contenu dans le fichier
print("Modèle chargé avec succès.")


# Charge l'objet appelé `fit` contenant le modèle
# Charger le modèle R dans l'environnement
ro.r(f'load("{local_file}")')  # Charge l'objet R contenu dans le fichier
model_loaded=True
# Charger le modèle R
if model_loaded:
    # Charger les données d'origine
    ro.r('''
    load_data <- function(model) {
        return(as.data.frame(model$data))  # Remplacez `model$data` par la source correcte
    }
    ''')
    load_data = ro.globalenv["load_data"]
    data_r = load_data(ro.globalenv["fit"])
    data = pandas2ri.rpy2py(data_r)

    # Variables disponibles
    variables = list(data.columns)
    st.sidebar.subheader("Variables Explicatives")
    selected_vars = st.sidebar.multiselect("Sélectionnez les variables à modifier", variables, variables[:2])

    # Entrée utilisateur pour les variables sélectionnées
    future_values = {}
    for var in selected_vars:
        future_values[var] = st.sidebar.number_input(f"Valeur future pour {var}", value=float(data[var].mean()))

    # Période de prédiction
    prediction_period = st.sidebar.slider("Nombre de périodes pour la prédiction", 1, 20, 10)

    # Créer un jeu de données pour les prédictions
    modified_data = data.mean().to_dict()  # Moyennes des variables
    modified_data.update(future_values)  # Mettre à jour avec les valeurs utilisateur

    # Générer les données futures
    future_data = pd.DataFrame([modified_data] * prediction_period)
    future_data_r = pandas2ri.py2rpy(future_data)

    # Fonction de prédiction avec intervalles de confiance
    ro.r('''
    predict_with_ci <- function(model, newdata) {
        predictions <- predict(model, newdata = newdata, interval = "confidence")
        return(as.data.frame(predictions))
    }
    ''')
    predict_with_ci = ro.globalenv["predict_with_ci"]

    # Prédictions initiales (avec moyennes)
    initial_predictions_r = predict_with_ci(ro.globalenv["fit"], newdata=future_data_r)
    initial_predictions = pandas2ri.rpy2py(initial_predictions_r)

    # Prédictions modifiées (avec valeurs utilisateur)
    modified_predictions_r = predict_with_ci(ro.globalenv["fit"], newdata=future_data_r)
    modified_predictions = pandas2ri.rpy2py(modified_predictions_r)

    # Afficher les résultats
    st.subheader("Résultats des Prédictions")
    st.write("Prédictions initiales (avec moyennes) :")
    st.dataframe(initial_predictions)

    st.write("Prédictions avec vos valeurs :")
    st.dataframe(modified_predictions)

    # Graphique interactif avec Plotly
    fig = go.Figure()

    # Ajouter les prédictions initiales
    fig.add_trace(go.Scatter(
        x=list(range(len(initial_predictions))),
        y=initial_predictions["fit"],
        mode='lines',
        name='Initiales (fit)',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(initial_predictions))),
        y=initial_predictions["lwr"],
        mode='lines',
        name='Initiales (lwr)',
        line=dict(color='blue', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(initial_predictions))),
        y=initial_predictions["upr"],
        mode='lines',
        name='Initiales (upr)',
        line=dict(color='blue', dash='dot')
    ))

    # Ajouter les prédictions modifiées
    fig.add_trace(go.Scatter(
        x=list(range(len(modified_predictions))),
        y=modified_predictions["fit"],
        mode='lines',
        name='Modifiées (fit)',
        line=dict(color='green')
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(modified_predictions))),
        y=modified_predictions["lwr"],
        mode='lines',
        name='Modifiées (lwr)',
        line=dict(color='green', dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=list(range(len(modified_predictions))),
        y=modified_predictions["upr"],
        mode='lines',
        name='Modifiées (upr)',
        line=dict(color='green', dash='dot')
    ))

    # Mise en page
    fig.update_layout(
        title="Comparaison des Prédictions",
        xaxis_title="Période",
        yaxis_title="Valeur Prédite",
        legend_title="Légende",
        template="plotly_white"
    )

    st.plotly_chart(fig)
