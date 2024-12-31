import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Assuming df is your DataFrame (replace with your actual data loading)
# ... (Your data loading code from the previous example) ...

url="https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/refs/heads/main/Base_F2.csv"

df = pd.read_csv(url,sep=";",decimal=",")

st.title("Visualisation des données")


# Sidebar for year range selection
st.sidebar.header("Sélection de la période")
min_year = int(df.index.min())
max_year = int(df.index.max())
start_year = st.sidebar.slider("Année de début", min_year, max_year, min_year)
end_year = st.sidebar.slider("Année de fin", min_year, max_year, max_year)

# Sidebar for variable selection
st.sidebar.header("Sélection des variables")
selected_columns = st.sidebar.multiselect("Sélectionnez les colonnes à afficher", df.columns, default=list(df.columns))
all_columns = st.sidebar.checkbox("Afficher toutes les colonnes", value=True)

# Determine columns to display
if all_columns:
    columns_to_plot = df.columns
else:
    columns_to_plot = selected_columns
def ncols(i):
  if  i in range(3):
    return 1
  elif i in range(3,8):
    return 2
  else:
    return 3
if not columns_to_plot:
    st.warning("Veuillez sélectionner au moins une colonne.")
else:
    # Plot based on the number of selected columns
    n_cols = ncols(len(columns_to_plot))
    n_rows = (len(columns_to_plot) + n_cols - 1) // n_cols

    cols = st.columns(n_cols)

    for i, col_name in enumerate(columns_to_plot):
        with cols[i % n_cols]:
            filtered_df = df[(df.index >= start_year) & (df.index <= end_year)]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=filtered_df.index, y=filtered_df[col_name], mode='lines+markers', name=col_name, line=dict(color=f'rgb({np.random.randint(0,256)},{np.random.randint(0,256)},{np.random.randint(0,256)})')))
            fig.update_layout(
                title=f"Graphique de {col_name}",
                xaxis_title="Année",
                yaxis_title=col_name,
                xaxis_rangeslider_visible=True,
            )
            st.plotly_chart(fig)
