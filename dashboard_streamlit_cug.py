import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SEN'EAU – CUG Dashboard", layout="wide")

# === Style fond + encadré gauche ===
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
    </style>
""", unsafe_allow_html=True)

# === Titre principal ===
st.title("📊 Tableau de Bord – CUG Dakar")
st.markdown("**L’Excellence pour le Sénégal, la Référence pour l’Afrique**")

# === Colonnes : zone gauche (import, KPIs) et droite (graphique) ===
col_gauche, col_droite = st.columns([2, 5])

with col_gauche:
    st.markdown('<div class="bloc">', unsafe_allow_html=True)

    # Téléversement du fichier
    uploaded_file = st.file_uploader("📥 Téléverser le fichier Excel", type=["xlsx"])

    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df.columns = df.columns.str.strip()

            expected = {"Année", "Population", "Consommation_m3", "CUG (L/hab/j)"}
            if not expected.issubset(df.columns):
                st.error("❌ Le fichier doit contenir : Année, Population, Consommation_m3, CUG (L/hab/j)")
            else:
                # Sélection d'année
                selected_year = st.selectbox("📅 Sélectionnez une année :", sorted(df["Année"].unique()))
                selected = df[df["Année"] == selected_year].iloc[0]

                # Affichage des métriques
                st.metric("💧 CUG (L/hab/j)", f"{selected['CUG (L/hab/j)']:.2f}")
                st.metric("👥 Population", f"{selected['Population']:,.0f}")

        except Exception as e:
            st.error(f"Erreur de lecture : {e}")
    else:
        st.info("📂 Importez un fichier .xlsx pour commencer.")

    st.markdown('</div>', unsafe_allow_html=True)

# === Colonne droite : graphique Matplotlib ===
with col_droite:
    if uploaded_file and expected.issubset(df.columns):
        st.markdown("### 📈 Évolution de la CUG en fonction de la population à Dakar (1997–2035)")

        df_sorted = df.sort_values("Année")
        x = df_sorted["Population"]
        y = df_sorted["CUG (L/hab/j)"]

        fig, ax = plt.subplots(figsize=(8, 4))  # taille du graphique
        ax.plot(x, y, marker='o', color='orange', label='CUG en fonction de la population')

        ax.set_xlabel("Population")
        ax.set_ylabel("CUG (L/hab/j)")
        ax.set_title("Évolution de la CUG en fonction de la population à Dakar (1997–2035)")
        ax.legend()
        ax.grid(True)

        st.pyplot(fig)
