import streamlit as st
import os
import base64
import pandas as pd
import numpy as np

def set_background(image_path, opacity=0.5, color="#000000"):
    with open(image_path, "rb") as f:
        image_data = f.read()
    image_base64 = base64.b64encode(image_data).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: {color};
            opacity: {opacity};
            z-index: -1;
        }}
        .stApp h1, .stApp h2 {{
            color: blue !important;  /* Couleur bleue pour les titres */
        }}
        .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label, .stApp .streamlit-expanderHeader {{
            color: green !important;  /* Couleur verte pour les autres écritures */
            font-size: 20px !important;  /* Augmenter la taille de la police */
        }}
        .animated-title {{
            font-size: 2.5em;
            font-weight: bold;
            animation: text-animation 10s linear infinite;
            text-shadow: 2px 2px 4px #000000;
        }}
        @keyframes text-animation {{
            0% {{ transform: translateX(-100%); opacity: 0; }}
            10% {{ transform: translateX(0%); opacity: 1;}}
            90% {{transform: translateX(0%); opacity: 1;}}
            100% {{ transform: translateX(100%); opacity: 0; }}
        }}
        .fade-in-out {{
            animation: fade 3s ease-in-out infinite alternate;
            color: #ADD8E6;
        }}
        @keyframes fade {{
            0% {{ opacity: 0.2; color: #ADD8E6;}}
            50% {{ opacity: 1; color: #87CEEB; }}
            100% {{ opacity: 0.2; color: #ADD8E6; }}
        }}
        .fixed-text {{
            color: #006400; /* Vert foncé */
            font-size: 1.5em; /* Taille de police */
            font-weight: normal; /* Poids de police normal */
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    #st.set_page_config(page_title="Visualisation des Données", page_icon="")
    #background_path = "C://Users//djetek_user//Desktop//ISE 3//Pierre et Nathan projet//image_modelisation.jpg"
    #set_background(background_path, opacity=0.3, color="#FF4500")

    st.markdown("""<h1 class="animated-title">Base de donnés RDC</h1>""", unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Période étude : 1999 - 2023 </h2>', unsafe_allow_html=True)
    st.markdown('<h2 class="fade-in-out">Soit une serie de 24 ans. </h2>', unsafe_allow_html=True)
    st.title("Les données présentées sur cette page résultent d'une collecte d'informations à partir de differents rapports de la banque centrale du congo (BCC).")
    
if __name__ == '__main__':
    main()

import streamlit as st
import pandas as pd
from statsmodels.tsa.ardl import ARDL
from arch.unitroot import PhillipsPerron
import numpy as np

def test_stationarity_pp(series):
    """Effectue le test de Phillips-Perron et retourne la p-value."""
    pp_test = PhillipsPerron(series)
    return pp_test.pvalue  # p-value

def test_first_difference_stationarity_pp(df, var):
    """Vérifie la stationnarité de la première différence d'une série avec le test de Phillips-Perron."""
    return test_stationarity_pp(df[var].diff().dropna())

def main():
    st.title("Estimation d'un Modèle ARDL avec Test de Phillips-Perron")

    try:
        # Chargement des données
        df = pd.read_excel("https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F%204.xlsx")
        
        # Appliquer le logarithme népérien sur toutes les variables sauf les exceptions
        exceptions = ["Banque centrale - Taux directeur", "Inflation annuelle moyenne"]
        for col in df.columns[1:]:  # Exclure la première colonne (Année)
            if col not in exceptions:
                df[col] = np.log(df[col])

        # Initialiser les p-values
        p_value = None
        p_value_diff = None

        # Sélection de la variable dépendante
        dependent_var = st.selectbox("Sélectionnez la variable dépendante :", df.columns[1:])  # Exclure la première colonne (Année)

        # Sélection des variables indépendantes
        independent_vars = st.multiselect("Sélectionnez les variables indépendantes :", df.columns[1:])
        
        # Saisir le nombre de retards
        lags = st.number_input("Entrez le nombre de retards (lags) :", min_value=1, value=2)

        # Vérification de la stationnarité de la variable dépendante
        if st.button("Vérifier la stationnarité"):
            p_value = test_stationarity_pp(df[dependent_var])  # Utiliser directement la colonne
            st.write(f"p-value Phillips-Perron pour {dependent_var} : {p_value}")
            if p_value < 0.05:
                st.success(f"{dependent_var} est stationnaire.")
            else:
                st.warning(f"{dependent_var} n'est pas stationnaire.")
                st.write("Calcul de la première différence du logarithme népérien de la variable dépendante et des variables indépendantes :")
                
                # Calculer la première différence du logarithme népérien
                df[dependent_var] = df[dependent_var].diff().dropna()
                for var in independent_vars:
                    df[var] = df[var].diff().dropna()
                
                # Vérification de la stationnarité des variables après transformation
                p_value_diff = test_stationarity_pp(df[dependent_var].dropna())
                st.write(f"p-value Phillips-Perron pour la première différence de {dependent_var} : {p_value_diff}")
                if p_value_diff < 0.05:
                    st.success(f"La première différence de {dependent_var} est stationnaire.")
                else:
                    st.warning(f"La première différence de {dependent_var} n'est pas stationnaire.")

                for var in independent_vars:
                    p_value_diff_var = test_first_difference_stationarity_pp(df, var)  # Utiliser directement la colonne
                    st.write(f"p-value Phillips-Perron pour la première différence de {var} : {p_value_diff_var}")
                    if p_value_diff_var < 0.05:
                        st.success(f"La première différence de {var} est stationnaire.")
                    else:
                        st.warning(f"La première différence de {var} n'est pas stationnaire.")
# Créer un DataFrame pour les variables en première différence
                df_diff = df.copy()
                df_diff[dependent_var] = df_diff[dependent_var].diff()
                for var in independent_vars:
                    df_diff[var] = df_diff[var].diff()

                # Vérifier la stationnarité des variables en première différence
                stationary_vars = [dependent_var]  # Commencer avec la variable dépendante
                for var in independent_vars:
                    if test_first_difference_stationarity_pp(df_diff, var) < 0.05:
                        stationary_vars.append(var)

                # Estimation du modèle ARDL uniquement avec les variables stationnaires
                if len(stationary_vars) > 1:  # Au moins une variable dépendante et une indépendante
                    model = ARDL(df_diff[stationary_vars[0]].dropna(), lags=lags, exog=df_diff[stationary_vars[1:]].dropna())
                    results = model.fit()

                    # Afficher les résultats
                    st.write("Résumé du modèle ARDL :")
                    st.write(results.summary())
                else:
                    st.warning("Aucune variable indépendante stationnaire trouvée. Veuillez vérifier les variables sélectionnées.")

    except FileNotFoundError:
        st.error("Fichier non trouvé.")
    except Exception as e:
        st.error(f"Erreur : {e}")

if __name__ == '__main__':
    main()
