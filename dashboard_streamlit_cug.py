import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="SEN'EAU – CUG Dashboard", layout="wide")

# === Style général ===
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

st.title("📊 Tableau de Bord – CUG Dakar")
st.markdown("**L’Excellence pour le Sénégal, la Référence pour l’Afrique**")

# === Mise en page à deux colonnes ===
col_gauche, col_droite = st.columns([2, 5])

with col_gauche:
    st.markdown('<div class="bloc">', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("📥 Téléverser le fichier Excel", type=["xlsx"])

    if uploaded_file:
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

# === Colonne droite : graphique ===
with col_droite:
    if uploaded_file:
        df_chart = df.rename(columns={"CUG (L/hab/j)": "CUG"})

        chart = alt.Chart(df_chart).mark_line(point=alt.OverlayMarkDef(color='blue')).encode(
            x=alt.X('Population:Q', title='Population'),
            y=alt.Y('CUG:Q', title='CUG (L/hab/j)'),
            tooltip=['Année', 'Population', 'CUG']
        ).properties(
            width=600,
            height=400,
            title='📈 CUG en fonction de la population'
        ).configure_axis(
            labelColor='black',
            titleColor='black'
        ).configure_title(
            color='black'
        ).interactive()

        st.altair_chart(chart, use_container_width=False)
