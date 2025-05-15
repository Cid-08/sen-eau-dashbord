# === IMPORTS ===
import streamlit as st
import pandas as pd
import plotly.express as px

# === CONFIG PAGE ===
st.set_page_config(page_title="SEN'EAU – CUG Dashboard", layout="wide")

# === STYLES GÉNÉRAUX (SEN'EAU) ===
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #e6f7ff;
}
.bloc {
    background-color: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 0 8px rgba(0,0,0,0.1);
}
/* Titre, sous-titres */
h1, h2, h3, label {
    color: #003366 !important;
}
/* KPI Labels */
div[data-testid="stMetricLabel"] > div {
    color: #8DC63F !important;
    font-weight: bold;
}
/* KPI Valeurs */
div[data-testid="stMetricValue"] > div {
    color: #003366 !important;
    font-weight: bold;
    font-size: 1.6rem;
}
/* Upload */
section[data-testid="stFileUploader"] label {
    color: #8DC63F !important;
    font-weight: bold;
}
section[data-testid="stFileUploader"] > div {
    background-color: #003366 !important;
    color: white !important;
    border-radius: 6px;
    padding: 1rem;
}
section[data-testid="stFileUploader"] * {
    color: white !important;
}
/* Selectbox */
div[data-baseweb="select"] {
    background-color: #003366 !important;
    border-radius: 5px;
}
div[data-baseweb="select"] * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# === EN-TÊTE À 3 COLONNES ===
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("logo_hackathon.jpg", width=140)
    st.markdown("""
    <div style='color:#8DC63F; font-size:14px; font-weight:bold; text-align:center;'>
    Équipe : Deepthinkers_2025
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; font-size: 32px; font-weight: bold; color: #003366; padding-top: 10px;'>
    📊 Tableau de Bord – CUG Dakar
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.image("logo_seneau.jpg", width=140)
    st.markdown("""
    <div style='color:#8DC63F; font-size:14px; font-weight:bold; text-align:right;'>
    L’Excellence pour le Sénégal, la Référence pour l’Afrique
    </div>
    """, unsafe_allow_html=True)

# === COLONNES PRINCIPALES ===
col_gauche, col_droite = st.columns([2, 5])

with col_gauche:
    st.markdown('<div class="bloc">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📥 Téléverser le fichier Excel", type=["xlsx"])

    if uploaded_file:
        st.markdown(
            f"<div style='color:#003366; font-weight:600;'>📄 {uploaded_file.name}</div>",
            unsafe_allow_html=True
        )

        try:
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.strip()

            expected = {"Année", "Population", "Consommation_m3", "CUG (L/hab/j)"}
            if not expected.issubset(df.columns):
                st.error("❌ Le fichier doit contenir : Année, Population, Consommation_m3, CUG (L/hab/j)")
            else:
                selected_year = st.selectbox("📅 Sélectionnez une année :", sorted(df["Année"].unique()))
                selected = df[df["Année"] == selected_year].iloc[0]

                st.metric("💧 CUG (L/hab/j)", f"{selected['CUG (L/hab/j)']:.2f}")
                st.metric("👥 Population", f"{selected['Population']:,.0f}")

        except Exception as e:
            st.error(f"Erreur de lecture : {e}")
    else:
        st.info("📂 Importez un fichier .xlsx pour commencer.")

    st.markdown('</div>', unsafe_allow_html=True)

# === GRAPHIQUE PLOTLY INTERACTIF ===
with col_droite:
    if uploaded_file and expected.issubset(df.columns):
        st.markdown("### 📈 Évolution de la CUG en fonction de la population à Dakar (1997–2035)")

        df_sorted = df.sort_values("Année")
        fig = px.line(
            df_sorted,
            x="Population",
            y="CUG (L/hab/j)",
            markers=True,
            labels={
                "Population": "Population",
                "CUG (L/hab/j)": "CUG (L/hab/j)"
            }
        )

        fig.update_traces(line_color="#8DC63F", line_width=3)

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#003366", size=14),
            title_font=dict(color="#003366", size=18),
            xaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                title_font=dict(color="#003366", size=16),
                tickfont=dict(color="#003366")
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray",
                title_font=dict(color="#003366", size=16),
                tickfont=dict(color="#003366")
            ),
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)
