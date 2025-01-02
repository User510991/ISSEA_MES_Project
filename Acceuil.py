import streamlit as st
col1, col2,col3 = st.columns(3)
with col2:
    st.image("https://raw.githubusercontent.com/Ndobo1997/Projet-MES/main/Logo_ISSEA.jpeg", use_container_width=True)
    st.markdown('<p class="caption">ISSEA</p>', unsafe_allow_html=True)
# Appliquer des styles avec HTML et CSS

def set_background(image_url, opacity=0.5, color="#000000"):
    """Définit l'image de fond de l'application."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({image_url});
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
            color: white !important;
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
        </style>
        """,
        unsafe_allow_html=True,
    )
set_background('https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/main/Back_ground2.jpg', opacity=0.5, color="#000000")
st.markdown(
    """
    <style>
    body {
        background-image: url('https://raw.githubusercontent.com/User510991/ISSEA_MES_Project/main/Back_ground2.jpg'); /* Remplacez par l'URL de votre image */
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
st.markdown("<div class='title'>Application de simulation</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Projet de cours de Modèle à équation simultané</div>", unsafe_allow_html=True)

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
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        """
        <div class='content'>
            <p>Réalisé par les élèves Ingénieurs Statisticiens Economistes:</p>
            <ul>
                <li><strong>DOMETI Kwassi Raphaël</strong></li>
                <li><strong>JOUBAIDA ALI</strong></li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        """
        <div class='content'>
            <p>Sous la supervision de:</p>
            <ul>
                <li><strong>M. CHASSEM Narcisse</strong>    
                <br><em>Ingénieur Statisticien Economiste, ...</em>.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
