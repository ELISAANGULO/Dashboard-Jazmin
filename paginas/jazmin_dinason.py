import streamlit as st 
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pathlib
from streamlit_extras.metric_cards import style_metric_cards

def jazmin_dinason():
    st.title("JAZMIN DINASON")

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
    excel_file_JAZ_path = 'data/DINASON JAZMIN.xlsx'
    excel_file_CARGADOR_JAZ_path = 'data/Cargador Diferidas Jazmín.xlsx'

    df_historico_jaz = load_excel_file(excel_file_JAZ_path, sheet_name='DINASON JAZMIN')


    # Verificar si la columna 'SPM' existe en el DataFrame
    if 'SPM' in df_historico_jaz.columns:
        df_historico_jaz = df_historico_jaz[['SARTA', 'FECHA', 'SPM', 'LLENADO DE BOMBA', 'SUMERGENCIA EFECTIVA','TEMPERATURA']].copy()
    else:
        df_historico_jaz = df_historico_jaz[['SARTA', 'FECHA', 'LLENADO DE BOMBA', 'SUMERGENCIA EFECTIVA','TEMPERATURA']].copy()

    df_jaz = load_excel_file(excel_file_JAZ_path, sheet_name='DIF DINASON JAZ')
    df_cargadores_Jaz = load_excel_file(excel_file_CARGADOR_JAZ_path, sheet_name='Trabajo Previo')
    df_cargadores_Jaz.columns = df_cargadores_Jaz.iloc[0]
    df_cargadores_Jaz = df_cargadores_Jaz[1:].reset_index(drop=True)

    # Process df_cargadores_Jaz
    estado_pozos_jaz = df_cargadores_Jaz[['NOMBRE  SARTA']].copy()
    estado_pozos_jaz.rename(columns={'NOMBRE  SARTA': 'SARTA'}, inplace=True)

    # Filter df_jaz
    df_jaz = df_jaz[~df_jaz['SARTA'].isin(estado_pozos_jaz['SARTA'])]

    # Sumergencia alta JAZ
    df_sumergencia_ALTA_JAZ = df_jaz[(df_jaz['SUMERGENCIA EFECTIVA ACTUAL'] > 200) & 
                                    (df_jaz['LLENADO BOMBA\n'] < 50) & 
                                    (df_jaz['SPM'] != 'OFF') & 
                                    (df_jaz['SPM'] != 'INACT')]

    # Ordenar el DataFrame por 'SUMERGENCIA EFECTIVA ACTUAL' de mayor a menor
    df_sumergencia_ALTA_JAZ = df_sumergencia_ALTA_JAZ.sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=False)

    # Sumergencia baja JAZ
    df_sumergencia_BAJA_JAZ = df_jaz[(df_jaz['SUMERGENCIA EFECTIVA ACTUAL'] < 30) & 
                                    (df_jaz['LLENADO BOMBA\n'] < 30) & 
                                    (df_jaz['SPM'] != 'OFF') & 
                                    (df_jaz['SPM'] != 'INACT')]

    # Ordenar el DataFrame por 'SUMERGENCIA EFECTIVA ACTUAL' de menor a mayor
    df_sumergencia_BAJA_JAZ = df_sumergencia_BAJA_JAZ.sort_values(by='SUMERGENCIA EFECTIVA ACTUAL', ascending=True)

    # Grafica sumergencia y nivel por pozos
    df_historico_jaz = pd.DataFrame(df_historico_jaz)

    # Convertir FECHA a datetime
    df_historico_jaz['FECHA'] = pd.to_datetime(df_historico_jaz['FECHA'])

    # Filtrar datos del último año
    ultimo_ano = df_historico_jaz['FECHA'].max() - pd.DateOffset(years=1)
    df_historico_jaz = df_historico_jaz[df_historico_jaz['FECHA'] >= ultimo_ano]

    # Función para obtener los datos de un pozo específico
    def get_well_data(well_name):
        return df_historico_jaz[df_historico_jaz['SARTA'] == well_name]

    # Crear la aplicación Streamlit
    #st.title('Dashboard de Pozos')

    selected_well = st.selectbox(
        'Selecciona un pozo',
        df_historico_jaz['SARTA'].unique()
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
        if 'SPM' in latest_data:
            st.metric("SPM", latest_data['SPM'])
        else:
            st.metric("SPM", "N/A")
    st.divider()

    if st.button("REVISAR DATA GENERAL",key="data"):
    # Display data
        st.subheader("POZOS DE JAZMIN CON SUMERGENCIA MAYOR A 200 Y LLENADO DE BOMBA MENOR A 50")
        df_sumergencia_JAZ_copy = df_sumergencia_ALTA_JAZ[['WELL','FECHA ACTUAL','SPM','LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_JAZ_copy)

        st.subheader("POZOS DE JAZMIN CON SUMERGENCIA MENOR A 30 FT Y LLENADO DE BOMBA MENOR A 30")
        df_sumergencia_JAZ_BAJA_copy = df_sumergencia_BAJA_JAZ[['WELL','FECHA ACTUAL','SPM','LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
        st.dataframe(df_sumergencia_JAZ_BAJA_copy)