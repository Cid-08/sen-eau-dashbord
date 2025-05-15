import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Tableau de Bord – SEN'EAU", layout="wide")

st.title("📊 Tableau de Bord – CUG Dakar")
st.markdown("L’Excellence pour le Sénégal, la Référence pour l’Afrique")

# === 1. Import du fichier ===
uploaded_file = st.file_uploader("📥 Téléverser le fichier Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # nettoyage

        # Vérification des colonnes
        expected_cols = {"Année", "Population", "Consommation_m3", "CUG (L/hab/j)"}
        if not expected_cols.issubset(df.columns):
            st.error("❌ Le fichier doit contenir les colonnes : Année, Population, Consommation_m3, CUG (L/hab/j)")
        else:
            # === 2. Sélection d’année ===
            st.markdown("### 📅 Sélectionnez une année")
            selected_year = st.selectbox("Année", sorted(df["Année"].unique()))

            selected_row = df[df["Année"] == selected_year].iloc[0]

            # Affichage des indicateurs
            col1, col2 = st.columns(2)
            col1.metric("Consommation Unitaire Globale (CUG)", f"{selected_row['CUG (L/hab/j)']:.2f} L/hab/j")
            col2.metric("Population", f"{selected_row['Population']:,.1f}")

            # === 3. Courbe Altair : CUG vs Population ===
            st.markdown("### 📉 Évolution de la CUG en fonction de la population à Dakar (1997–2035)")

            df_chart = df.rename(columns={"CUG (L/hab/j)": "CUG"})

            chart = alt.Chart(df_chart).mark_line(point=alt.OverlayMarkDef(color='blue')).encode(
                x=alt.X('Population:Q', title='Population'),
                y=alt.Y('CUG:Q', title='CUG (L/hab/j)'),
                tooltip=['Année', 'Population', 'CUG']
            ).properties(
                width=600,
                height=400,
                title='CUG en fonction de la Population'
            ).configure_axis(
                labelColor='black',
                titleColor='black'
            ).configure_title(
                color='black'
            ).interactive()

            left, center, right = st.columns([1, 6, 1])
            with center:
                st.altair_chart(chart, use_container_width=False)

    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
else:
    st.info("Veuillez importer un fichier Excel pour continuer.")
