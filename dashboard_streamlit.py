import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# === Configuration de la page ===
st.set_page_config(
    page_title="CUG Dakar – SEN'EAU",
    page_icon="💧",
    layout="wide"
)

# === Style personnalisé ===
st.markdown("""
    <style>
    body {
        background-color: #e6f7ff;
    }
    h1, h2, h3 {
        color: #007acc;
    }
    .stMetric {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# === En-tête ===
col_logo, col_titre, col_hackathon = st.columns([1, 2, 1])
with col_logo:
    st.image("logo seneau.jpg", width=150)
with col_titre:
    st.title("📊 Tableau de Bord – CUG Dakar")
    st.markdown("#### L’Excellence pour le Sénégal, la Référence pour l’Afrique")
with col_hackathon:
    st.image("Photo Hackathon .jpg", width=180)

# === Chargement des données Excel ===
file_path = "consommation_avec_CUG.xlsx"
try:
    df = pd.read_excel(file_path)
except:
    st.error("Erreur de lecture du fichier Excel.")

# Vérification des colonnes requises
# Vérification des colonnes requises
if {"Année", "Population", "CUG (L/hab/j)"}.issubset(df.columns):
    # Menu déroulant pour choisir l'année
    selected_year = st.selectbox("📅 Sélectionnez une année", df["Année"].unique())
    selected_row = df[df["Année"] == selected_year].iloc[0]

    col1, col2 = st.columns(2)
    col1.metric("Consommation Unitaire Globale (CUG)", f"{selected_row['CUG (L/hab/j)']:.2f} L/hab/j")
    col2.metric("Population", f"{selected_row['Population']:,}")

    # === Courbe interactive : CUG en fonction de la population ===
    st.markdown("### 📉 Évolution de la CUG en fonction de la population à Dakar (1997–2035)")

    chart = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(color='blue')).encode(
        x=alt.X('Population:Q', title='Population'),
        y=alt.Y('Q("CUG (L/hab/j)"):Q', title='CUG (L/hab/j)'),
        tooltip=['Année', 'Population', 'CUG (L/hab/j)']
    ).properties(
        width=900,
        height=400,
        title='CUG en fonction de la Population'
    ).configure_axis(
        labelColor='black',
        titleColor='black'
    ).configure_title(
        color='black'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)