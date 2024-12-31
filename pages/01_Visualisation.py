import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Assuming df is your DataFrame (replace with your actual data loading)
# ... (Your data loading code from the previous example) ...
url="https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F2.csv"

df = pd.read_csv(url,sep=";",decimal=",")
df = df.set_index('Annee')
def plot_df_column(df, column, start_year=None, end_year=None, title=None):
    """
    Génère un graphique de ligne de la colonne spécifiée du DataFrame.

    Args:
        df: Le DataFrame pandas.
        column: Le nom de la colonne à tracer.
        start_year: L'année de début de la plage (facultatif).
        end_year: L'année de fin de la plage (facultatif).
        title: Le titre du graphique (facultatif).
    """

    if start_year is not None and end_year is not None:
      df = df[(df.index >= start_year) & (df.index <= end_year)]
    elif start_year is not None:
      df = df[df.index >= start_year]
    elif end_year is not None:
      df = df[df.index <= end_year]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines+markers', name=column, line=dict(color=f'rgb({np.random.randint(0,256)},{np.random.randint(0,256)},{np.random.randint(0,256)})')))

    fig.update_layout(
        title=title if title is not None else f"Graphique de {column}",
        xaxis_title="Année",
        yaxis_title=column,
        xaxis_rangeslider_visible=True,
    )
    return fig

st.title("Visualisation des données")


# Sidebar for year range selection
#st.sidebar.header("Sélection de la période")
st.title("Sélection de la période")
min_year = int(df.index.min())
max_year = int(df.index.max())
#start_year = st.sidebar.slider("Année de début", min_year, max_year, min_year)
#end_year = st.sidebar.slider("Année de fin", min_year, max_year, max_year)
# Création du slider
start_year, end_year = st.slider(
    "Choisissez la plage d'année",
    min_value=min_year,  # Valeur minimale possible
    max_value=max_year,  # Valeur maximale possible
    value=(min_year, max_year),  # Plage par défaut sélectionnée
    step=1,  # Pas entre les valeurs
)
# Affichage des résultats
st.write(f"Année de départ sélectionnée : {start_year}")
st.write(f"Année finale sélectionnée : {end_year}")
# Sidebar for variable selection
st.sidebar.header("Sélection des variables")
selected_columns_raws = st.sidebar.multiselect("Sélectionnez les variables à afficher", df.columns, default=list(df.columns))
all_columns = st.sidebar.checkbox("Afficher toutes les colonnes", value=True)
reverse_selected_tables =st.sidebar.checkbox("Toutes les variables sauf celles sélectionnées",value=True)
if len(selected_columns_raws):
  if reverse_selected_tables:
    selected_columns =[col for col in df.columns if col not in selected_columns_raws]
  else:
    selected_columns=selected_columns_raws

# Determine columns to display
if all_columns:
    columns_to_plot = df.columns
elif len(selected_columns_raws):
    columns_to_plot = selected_columns
else:
    columns_to_plot = selected_columns_raws
def ncols(i):
  if  i in range(4):
    return 1
  #elif i in range(3,8):
    #return 2
  else:
    return 2#3
if len(columns_to_plot):
    # Plot based on the number of selected columns
    n_cols = ncols(len(columns_to_plot))
    n_rows = (len(columns_to_plot) + n_cols - 1) // n_cols

    cols = st.columns(n_cols)

    for i, col_name in enumerate(columns_to_plot):
        with cols[i % n_cols]:
            st.subheader(col_name)
            fig = plot_df_column(df, col_name, start_year, end_year)
            st.plotly_chart(fig, use_container_width=True)
else:
  st.warning("Veuillez sélectionner au moins une colonne.")
