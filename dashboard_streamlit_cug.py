import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="SEN'EAU – CUG Dashboard", layout="wide")

# === STYLE GLOBAL HARMONISÉ AUX COULEURS SEN'EAU ===
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

    h1, h2, h3, label, .st-emotion-cache-1c7y2kd {
        color: #003366 !important;
    }

    .stMetricLabel {
        color: #8DC63F !important; /* vert SEN’EAU */
        font-weight: bold;
    }

    .stMetricValue {
        color: #003366 !important; /* bleu foncé SEN’EAU */
        font-weight: bold;
        font-size: 1.6rem;
    }

    .st-emotion-cache-1avcm0n {
        color: #003366 !important;
    }

    .stSelectbox > div {
        color: #003366 !important;
    }

    .st-emotion-cache-1c7y2kd:hover {
        color: #8DC63F !important;
    }
    </style>
""", unsafe_allow_html=True)

# === TITRE PRINCIPAL ===
st.title("📊 Tableau de Bord – CUG Dakar")
st.markdown("**L’Excellence pour le Sénégal, la Référence pour l’Afrique**")

# === COLONNES : GAUCHE (import, KPIs) / DROITE (graphique) ===
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
            title="Évolution de la CUG en fonction de la population à Dakar (1997–2035)",
            labels={
                "Population": "Population",
                "CUG (L/hab/j)": "CUG (L/hab/j)"
            }
        )

        fig.update_traces(line_color="#8DC63F", line_width=3)

        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(
                color="#003366",
                size=14
            ),
            title_font=dict(
                color="#003366",
                size=18
            ),
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
