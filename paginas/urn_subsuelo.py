import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px


def urn_subsuelo():

    st.title("URN DINASON")

    # Load Excel files
    excel_file = pd.ExcelFile('data/DINASON URN.xlsx')
    st.write("Sheets in DINASON URN.xlsx:", excel_file.sheet_names)

    excel_file_CARGADOR_URN = pd.ExcelFile('data/Cargador Diferidas Underriver Norte.xlsx')
    st.write("Sheets in Cargador Diferidas Underriver Norte.xlsx:", excel_file_CARGADOR_URN.sheet_names)

    # Read data from Excel files
    df_urn = pd.read_excel(excel_file, sheet_name='DIF DINASON URN')
    df_cargadores_URN = pd.read_excel(excel_file_CARGADOR_URN, sheet_name='Trabajo Previo')
    df_cargadores_URN.columns = df_cargadores_URN.iloc[0]
    df_cargadores_URN = df_cargadores_URN[1:].reset_index(drop=True)

    # Display first 5 rows of df_urn
    st.write("First 5 rows of df_urn:")
    st.dataframe(df_urn.head(5))

    # Process df_cargadores_URN
    estado_pozos_urn = df_cargadores_URN[['NOMBRE  SARTA']].copy()
    estado_pozos_urn.rename(columns={'NOMBRE  SARTA': 'SARTA'}, inplace=True)
    st.write("First 3 rows of estado_pozos_urn:")
    st.dataframe(estado_pozos_urn.head(3))

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

    # Display data
    st.subheader("POZOS DE URN CON SUMERGENCIA MAYOR A 200 Y LLENADO DE BOMBA MENOR A 50")
    df_sumergencia_URN_ALTA_copy = df_sumergencia_ALTA_URN[['WELL','FECHA ACTUAL','SPM','LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
    st.dataframe(df_sumergencia_URN_ALTA_copy)

    st.subheader("POZOS DE URN CON SUMERGENCIA MENOR A 30 FT Y LLENADO DE BOMBA MENOR A 30")
    df_sumergencia_URN_BAJA_copy = df_sumergencia_BAJA_URN[['WELL','FECHA ACTUAL','SPM','LLENADO BOMBA\n', 'SUMERGENCIA EFECTIVA ACTUAL']].copy()
    st.dataframe(df_sumergencia_URN_BAJA_copy)