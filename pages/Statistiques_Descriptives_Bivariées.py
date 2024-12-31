import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import streamlit as st

# Streamlit app starts here
st.title("Statistiques Descriptives Bivariées")


st.write("Aperçu des données :")
st.dataframe(df.head())

# Variable selection
variables = st.multiselect("Sélectionner les variables :", df.columns)

if variables:
  # Descriptive statistics
  st.subheader("Statistiques descriptives :")
  st.write(df[variables].describe())

  # Pairplot
  st.subheader("Nuage de points (pairplot) :")
  fig_pairplot = px.scatter_matrix(df[variables])
  st.plotly_chart(fig_pairplot)


  # Correlation matrix (optional)
  st.subheader("Matrice de corrélation :")
  correlation_matrix = df[variables].corr()
  st.write(correlation_matrix)


  # Other bivariate plots (example: scatter plot)
  x_var = st.selectbox("Variable X :", variables)
  y_var = st.selectbox("Variable Y :", variables, index=1 if len(variables)>1 else 0 ) #avoid the same variable for x and y

  if x_var != y_var:
    st.subheader(f"Nuage de points : {y_var} en fonction de {x_var}")
    fig_scatter = px.scatter(df, x=x_var, y=y_var)
    st.plotly_chart(fig_scatter)

else:
    st.warning("Veuillez sélectionner au moins une variable.")
