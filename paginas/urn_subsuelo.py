import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pathlib
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib.pyplot as plt

def urn_subsuelo():
    st.title("JAZMIN SUBSUELO")

    @st.cache_data
    def load_excel_file(file_path, sheet_name=None):
        return pd.read_excel(file_path, sheet_name=sheet_name)

    # LOAD CSS
    def load_css(file_css):
        if file_css.exists():
            with open(file_css) as css:
                st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)
        else:
            st.error("CSS file not found.")

    css_path = pathlib.Path("style.css")
    load_css(css_path)

    # Load Excel files
    excel_file_JAZ_path = 'data/INTERVENCIONES JAZMIN.xlsx'
    df_historico_jaz = load_excel_file(excel_file_JAZ_path, sheet_name='BD')

    # Convertir FECHA a datetime y luego al formato DD/MM/YYYY
    df_historico_jaz['FECHA'] = pd.to_datetime(df_historico_jaz['FECHA'], errors='coerce', dayfirst=True)

    # Filtrar fechas inválidas
    df_historico_jaz = df_historico_jaz.dropna(subset=['FECHA'])

    # Filtrar registros donde CAMPO sea igual a 'JAZMIN'
    df_historico_jaz = df_historico_jaz[df_historico_jaz['CAMPO'].str.upper() == 'UNDERRIVER']

    st.dataframe(df_historico_jaz)

    def get_filtered_data(well_planning, sarta):
        df_filtered = df_historico_jaz
        if well_planning:
            df_filtered = df_filtered[df_filtered['WELL PLANNING'].isin(well_planning)]
        if sarta:
            df_filtered = df_filtered[df_filtered['SARTA'] == sarta]
        return df_filtered

    # Crear la aplicación Streamlit
    selected_well_planning = st.multiselect('Selecciona un well planning', list(df_historico_jaz['WELL PLANNING'].unique()))
    selected_pozo = st.selectbox('Selecciona un pozo', [''] + list(df_historico_jaz['SARTA'].unique()))

    df_filtered = get_filtered_data(selected_well_planning, selected_pozo)

    if not df_filtered.empty:
        # Contar el número de intervenciones por fecha y tipo de intervención
        df_filtered['COUNT'] = df_filtered.groupby(['FECHA', 'INTERVENCION'])['INTERVENCION'].transform('count')
        
        fig = px.bar(df_filtered, x='FECHA', y='COUNT', color='INTERVENCION', title='Cantidad de intervenciones por fecha y tipo de intervención')

        fig.update_layout(
            xaxis=dict(title='FECHA', tickformat='%d/%m/%Y'),
            yaxis=dict(title='# de SERVICIOS'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='black')
        )

        st.plotly_chart(fig)
        
        # Crear tabla resumen por pozo y año
        df_filtered['AÑO'] = df_filtered['FECHA'].dt.year
        resumen_por_pozo = df_filtered.groupby(['SARTA', 'AÑO']).size().reset_index(name='SERVICIOS')
        
        st.subheader("Resumen por Pozo y Año")
        st.dataframe(resumen_por_pozo, hide_index=True)
        
    else:
        st.warning("No hay datos para los filtros seleccionados.")

    st.divider()