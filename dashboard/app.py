import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# CONFIG
# ============================================
st.set_page_config(
    page_title="Volve Field — Well QC Dashboard",
    page_icon="🛢️",
    layout="wide"
)

# Style CSS pro
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #E07B00;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 { color: #1a1a2e; }
    .stMetric { background: white; padding: 15px; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ============================================
# DONNÉES
# ============================================
@st.cache_data
def load_data():
    df = pd.read_csv('../data/volve_production_clean.csv',
                     parse_dates=['DATEPRD'])
    df['WATER_CUT'] = (
        df['BORE_WAT_VOL'] /
        (df['BORE_OIL_VOL'] + df['BORE_WAT_VOL'])
    ) * 100
    return df

df = load_data()

# ============================================
# HEADER
# ============================================
st.markdown("## Volve Field — Well Production QC Dashboard")
st.markdown("*Champ Volve, Mer du Nord (2008–2016) · Equinor Open Dataset · Portfolio TotalEnergies*")
st.divider()

# ============================================
# FILTRES SIDEBAR
# ============================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/TotalEnergies_logo.svg/320px-TotalEnergies_logo.svg.png", width=180)
st.sidebar.markdown("### 🔧 Filtres")

puits = st.sidebar.multiselect(
    "Sélectionner les puits",
    options=df['NPD_WELL_BORE_NAME'].unique(),
    default=df['NPD_WELL_BORE_NAME'].unique()
)

date_range = st.sidebar.date_input(
    "Période",
    value=[df['DATEPRD'].min(), df['DATEPRD'].max()]
)

df_filtered = df[
    (df['NPD_WELL_BORE_NAME'].isin(puits)) &
    (df['DATEPRD'] >= pd.Timestamp(date_range[0])) &
    (df['DATEPRD'] <= pd.Timestamp(date_range[1]))
]

# ============================================
# KPIs
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Huile totale",
            f"{df_filtered['BORE_OIL_VOL'].sum()/1e6:.1f}M Sm³")
col2.metric("Gaz total",
            f"{df_filtered['BORE_GAS_VOL'].sum()/1e6:.0f}M Sm³")
col3.metric("Eau totale",
            f"{df_filtered['BORE_WAT_VOL'].sum()/1e6:.1f}M Sm³")
col4.metric("🕳️ Puits actifs",
            df_filtered['NPD_WELL_BORE_NAME'].nunique())
col5.metric("Jours de prod.",
            df_filtered['DATEPRD'].nunique())

st.divider()

# ============================================
# GRAPHIQUES — Ligne 1
# ============================================
col1, col2 = st.columns(2)

with col1:
    oil_by_well = df_filtered.groupby('NPD_WELL_BORE_NAME')['BORE_OIL_VOL']\
                             .sum().reset_index()\
                             .sort_values('BORE_OIL_VOL', ascending=False)
    fig1 = px.bar(
        oil_by_well,
        x='NPD_WELL_BORE_NAME',
        y='BORE_OIL_VOL',
        title='Production totale par puits',
        labels={'NPD_WELL_BORE_NAME': 'Puits',
                'BORE_OIL_VOL': 'Volume huile (Sm³)'},
        color='BORE_OIL_VOL',
        color_continuous_scale='Oranges',
        text_auto='.2s'
    )
    fig1.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    wc = df_filtered.groupby('NPD_WELL_BORE_NAME')['WATER_CUT']\
                    .mean().reset_index()\
                    .sort_values('WATER_CUT', ascending=False)
    fig2 = px.bar(
        wc,
        x='NPD_WELL_BORE_NAME',
        y='WATER_CUT',
        title='Water Cut moyen par puits',
        labels={'NPD_WELL_BORE_NAME': 'Puits',
                'WATER_CUT': 'Water Cut (%)'},
        color='WATER_CUT',
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    fig2.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False,
        coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True)

# ============================================
# GRAPHIQUES — Ligne 2
# ============================================
oil_time = df_filtered.groupby('DATEPRD')['BORE_OIL_VOL']\
                      .sum().reset_index()
fig3 = px.line(
    oil_time,
    x='DATEPRD',
    y='BORE_OIL_VOL',
    title='Évolution de la production journalière',
    labels={'DATEPRD': 'Date',
            'BORE_OIL_VOL': 'Production huile (Sm³/jour)'},
    color_discrete_sequence=['#E07B00']
)
fig3.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white'
)
st.plotly_chart(fig3, use_container_width=True)

# ============================================
# GRAPHIQUES — Ligne 3
# ============================================
col1, col2 = st.columns(2)

with col1:
    fig4 = px.box(
        df_filtered,
        x='NPD_WELL_BORE_NAME',
        y='AVG_DOWNHOLE_PRESSURE',
        title='Distribution pression fond de puits',
        labels={'NPD_WELL_BORE_NAME': 'Puits',
                'AVG_DOWNHOLE_PRESSURE': 'Pression (bar)'},
        color='NPD_WELL_BORE_NAME',
        points='outliers'
    )
    fig4.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    prod_by_well = df_filtered.groupby(
        ['DATEPRD', 'NPD_WELL_BORE_NAME']
    )['BORE_OIL_VOL'].sum().reset_index()

    fig5 = px.line(
        prod_by_well,
        x='DATEPRD',
        y='BORE_OIL_VOL',
        color='NPD_WELL_BORE_NAME',
        title='Production par puits dans le temps',
        labels={'DATEPRD': 'Date',
                'BORE_OIL_VOL': 'Production (Sm³/jour)',
                'NPD_WELL_BORE_NAME': 'Puits'}
    )
    fig5.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    st.plotly_chart(fig5, use_container_width=True)

# ============================================
# FOOTER
# ============================================
st.divider()
st.markdown(
    "*Dashboard développé dans le cadre d'un portfolio Data Analyst — "
    "Données : Equinor Volve Open Dataset (CC License)*"
)
