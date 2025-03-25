import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pathlib
from streamlit_extras.metric_cards import style_metric_cards

def girasol_dinason():
    # LOAD CSS
    def load_css(file_css):
        with open(file_css) as css:
            st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

    css_path = pathlib.Path("style.css")
    load_css(css_path)

    @st.cache_data
    def load_excel_file(file_path, sheet_name=None):
        return pd.read_excel(file_path, sheet_name=sheet_name)


    @st.cache_data
    def filter_data(df, estado_pozos_gir):
        df_gir = df[~df['SARTA'].isin(estado_pozos_gir['SARTA'])]
        df_sumergencia_ALTA_GIR = df_gir[(df_gir['SUMERGENCIA EFECTIVA ACTUAL'] > 200) & 
                                        (df_gir['LLENADO BOMBA\n'] < 50) & 
                                        (df_gir['SPM'] != 'OFF') & 
                                        (df_gir['SPM'] != 'INACT')].sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=False)
        df_sumergencia_BAJA_GIR = df_gir[(df_gir['SUMERGENCIA EFECTIVA ACTUAL'] < 30) & 
                                        (df_gir['LLENADO BOMBA\n'] < 30) & 
                                        (df_gir['SPM'] != 'OFF') & 
                                        (df_gir['SPM'] != 'INACT')].sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=True)
        return df_sumergencia_ALTA_GIR, df_sumergencia_BAJA_GIR


    st.title("GIRASOL DINASON")

    # Load Excel files
    excel_file_GIR_path = 'data/DINASON GIRASOL.xlsx'
    excel_file_CARGADOR_GIR_path = 'data/Cargador Diferidas Girasol.xlsx'

    df_historico_gir = load_excel_file(excel_file_GIR_path, sheet_name='DINASON GIRASOL')
    df_gir = load_excel_file(excel_file_GIR_path, sheet_name='DIF DINASON GIR')
    df_cargadores_GIR = load_excel_file(excel_file_CARGADOR_GIR_path, sheet_name='Trabajo Previo')
    df_cargadores_GIR.columns = df_cargadores_GIR.iloc[0]
    df_cargadores_GIR = df_cargadores_GIR[1:].reset_index(drop=True)

    estado_pozos_gir = df_cargadores_GIR[['NOMBRE  SARTA']].copy()
    estado_pozos_gir.rename(columns={'NOMBRE  SARTA': 'SARTA'}, inplace=True)

    df_sumergencia_ALTA_GIR, df_sumergencia_BAJA_GIR = filter_data(df_gir, estado_pozos_gir)

    # Verificar si la columna 'SPM' existe en el DataFrame
    if 'SPM' in df_historico_gir.columns:
        df_historico_gir = df_historico_gir[['SARTA', 'FECHA', 'SPM', 'LLENADO DE BOMBA', 'SUMERGENCIA EFECTIVA','TEMPERATURA']].copy()
    else:
        df_historico_gir = df_historico_gir[['SARTA', 'FECHA', 'LLENADO DE BOMBA', 'SUMERGENCIA EFECTIVA','TEMPERATURA']].copy()

    # Convertir FECHA a datetime
    df_historico_gir['FECHA'] = pd.to_datetime(df_historico_gir['FECHA'])

    # Filtrar datos del último año
    ultimo_ano = df_historico_gir['FECHA'].max() - pd.DateOffset(years=1)
    df_historico_gir = df_historico_gir[df_historico_gir['FECHA'] >= ultimo_ano]

    # Función para obtener los datos de un pozo específico
    def get_well_data(well_name):
        return df_historico_gir[df_historico_gir['SARTA'] == well_name]

    selected_well = st.selectbox(
        'Selecciona un pozo',
        df_historico_gir['SARTA'].unique()
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

    if st.button("REVISAR DATA GENERAL", key="data"):
        st.subheader("POZOS DE GIRASOL CON SUMERGENCIA MAYOR A 200 Y LLENADO DE BOMBA MENOR A 50")
        df_sumergencia_GIR_copy = df_sumergencia_ALTA_GIR[['WELL', 'FECHA ACTUAL', 'SPM', 'LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_GIR_copy)

        st.subheader("POZOS DE GIRASOL CON SUMERGENCIA MENOR A 30 FT Y LLENADO DE BOMBA MENOR A 30")
        df_sumergencia_GIR_copy = df_sumergencia_BAJA_GIR[['WELL', 'FECHA ACTUAL', 'SPM', 'LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_GIR_copy)