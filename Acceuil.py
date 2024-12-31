import streamlit as st

# Appliquer des styles avec HTML et CSS
st.markdown(
    """
    <style>
    body {
        background-image: url('https://via.placeholder.com/1920x1080'); /* Remplacez par l'URL de votre image */
        background-size: cover;
        background-attachment: fixed;
        color: white; /* Couleur du texte par défaut */
    }
    .title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
    }
    .subtitle {
        font-size: 1.5em;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 30px;
        font-style: italic;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    .content {
        background-color: rgba(0, 0, 0, 0.6); /* Couleur de fond semi-transparente */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        max-width: 800px;
        margin: auto;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Titre et sous-titre
st.markdown("<div class='title'>Bienvenue sur Mon Application</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Votre plateforme interactive</div>", unsafe_allow_html=True)

# Contenu principal avec mise en forme
st.markdown(
    """
    <div class='content'>
        <p>Bienvenue sur cette plateforme interactive, où vous pouvez explorer des données, visualiser des graphiques, 
        et interagir avec des outils d'analyse en temps réel.</p>
        <p>Utilisez le menu à gauche pour naviguer entre les différentes sections de l'application.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
