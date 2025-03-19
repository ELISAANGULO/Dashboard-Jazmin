import streamlit as st 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pathlib
from streamlit_extras.metric_cards import style_metric_cards


def urn_dinason():
    st.title("URN DINASON")

    @st.cache_data
    def load_excel_file(file_path, sheet_name=None):
        return pd.read_excel(file_path, sheet_name=sheet_name)

    # LOAD CSS
    def load_css(file_css):
        with open(file_css) as css:
            st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    css_path = pathlib.Path("style.css")
    load_css(css_path)

    # Load Excel files
    excel_file_path = 'data/DINASON URN.xlsx'
    excel_file_CARGADOR_URN_path = 'data/Cargador Diferidas Underriver Norte.xlsx'

    df_historico_urn = load_excel_file(excel_file_path, sheet_name='DINASON URN')
    df_historico_urn = df_historico_urn[['SARTA', 'FECHA','SPM', 'LLENADO DE BOMBA', 'SUMERGENCIA EFECTIVA','TEMPERATURA']].copy()
    df_urn = load_excel_file(excel_file_path, sheet_name='DIF DINASON URN')
    df_cargadores_URN = load_excel_file(excel_file_CARGADOR_URN_path, sheet_name='Trabajo Previo')

    df_cargadores_URN.columns = df_cargadores_URN.iloc[0]
    df_cargadores_URN = df_cargadores_URN[1:].reset_index(drop=True)

    # Process df_cargadores_URN
    estado_pozos_urn = df_cargadores_URN[['NOMBRE  SARTA']].copy()
    estado_pozos_urn.rename(columns={'NOMBRE  SARTA': 'SARTA'}, inplace=True)

    # Sumergencia alta URN
    df_sumergencia_ALTA_URN = df_urn[(df_urn['SUMERGENCIA EFECTIVA ACTUAL'] > 200) & 
                                    (df_urn['LLENADO BOMBA\n'] < 50) & 
                                    (df_urn['SPM'] != 'OFF')]

    # Ordenar el DataFrame por 'SUMERGENCIA EFECTIVA ACTUAL' de mayor a menor
    df_sumergencia_ALTA_URN = df_sumergencia_ALTA_URN.sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=False)

    # Sumergencia baja URN
    df_sumergencia_BAJA_URN = df_urn[(df_urn['SUMERGENCIA EFECTIVA ACTUAL'] < 30) & 
                                    (df_urn['LLENADO BOMBA\n'] < 30) & 
                                    (df_urn['SPM'] != 'OFF')]

    # Ordenar el DataFrame por 'SUMERGENCIA EFECTIVA ACTUAL' de menor a mayor
    df_sumergencia_BAJA_URN = df_sumergencia_BAJA_URN.sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=True)

    # Convertir FECHA a datetime
    df_historico_urn['FECHA'] = pd.to_datetime(df_historico_urn['FECHA'])

    # Filtrar datos del último año
    ultimo_ano = df_historico_urn['FECHA'].max() - pd.DateOffset(years=1)
    df_historico_urn = df_historico_urn[df_historico_urn['FECHA'] >= ultimo_ano]

    # Función para obtener los datos de un pozo específico
    def get_well_data(well_name):
        return df_historico_urn[df_historico_urn['SARTA'] == well_name]

    # Crear la aplicación Streamlit
    #st.title('Dashboard de Pozos')

    selected_well = st.selectbox(
        'Selecciona un pozo',
        df_historico_urn['SARTA'].unique()
    )

    df_well = get_well_data(selected_well)


    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_well['FECHA'], y=df_well['LLENADO DE BOMBA'], mode='markers', name='LLENADO DE BOMBA', yaxis='y1', marker=dict(color='green')))
    fig.add_trace(go.Scatter(x=df_well['FECHA'], y=df_well['SUMERGENCIA EFECTIVA'], mode='lines+markers', name='SUMERGENCIA EFECTIVA', yaxis='y2', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df_well['FECHA'], y=df_well['TEMPERATURA'], mode='markers', name='TEMPERATURA', yaxis='y1', marker=dict(color='red',symbol='square')))
    fig.add_trace(go.Scatter(x=df_well['FECHA'], y=df_well['SPM'], mode='markers', name='SPM', yaxis='y1', marker=dict(color='Purple',symbol='triangle-up')))

    fig.update_layout(
        title=f'Datos del pozo {selected_well}',
        xaxis=dict(title='FECHA', tickformat='%b %Y'),
        yaxis=dict(title='LLENADO DE BOMBA/ TEMPERATURA / SPM'),
        yaxis2=dict(
            title='SUMERGENCIA EFECTIVA',
            tickfont=dict(color='black'),
            anchor='x',
            overlaying='y',
            side='right',
            position=1
        ),
        legend=dict(x=0, y=1.1, orientation='h'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )

    st.plotly_chart(fig)
    # Obtener los datos más recientes del pozo seleccionado
    latest_data = df_well.sort_values(by='FECHA', ascending=False).iloc[0]

    # Mostrar tarjetas con los datos seleccionados
    style_metric_cards(border_left_color="green", border_size_px=0)

    st.subheader(f'Datos del pozo {selected_well}')
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Fecha del último nivel", latest_data['FECHA'].strftime('%Y-%m-%d'))
        st.metric("Sumergencia Efectiva", latest_data['SUMERGENCIA EFECTIVA'])
    with col2:
        st.metric("Llenado de Bomba", latest_data['LLENADO DE BOMBA'])
        st.metric("SPM", latest_data['SPM'])

    st.divider()

    if st.button("REVISAR DATA GENERAL",key="data"):
        st.subheader("POZOS DE URN CON SUMERGENCIA MAYOR A 200 Y LLENADO DE BOMBA MENOR A 50")
        df_sumergencia_URN_ALTA_copy = df_sumergencia_ALTA_URN[['WELL', 'FECHA ACTUAL', 'SPM', 'LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_URN_ALTA_copy)

        st.subheader("POZOS DE URN CON SUMERGENCIA MENOR A 30 FT Y LLENADO DE BOMBA MENOR A 30")
        df_sumergencia_URN_BAJA_copy = df_sumergencia_BAJA_URN[['WELL', 'FECHA ACTUAL', 'SPM', 'LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_URN_BAJA_copy)