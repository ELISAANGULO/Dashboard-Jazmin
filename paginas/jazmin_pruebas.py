import streamlit as st 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pathlib

def jazmin_pruebas():
    st.title("JAZMIN PRUEBAS")

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
    excel_file_JAZ_path = 'data/Seguimiento pruebas JAZMIN.xlsx'
    df_historico_jaz = load_excel_file(excel_file_JAZ_path, sheet_name='BD')

    # Convertir FECHA a datetime y luego al formato DD/MM/YYYY
    df_historico_jaz['FECHA'] = pd.to_datetime(df_historico_jaz['FECHA'], dayfirst=True)

    # Formatear los valores de VOLUMEN DE ACEITE para que tengan solo una cifra decimal
    df_historico_jaz['VOLUMEN DE ACEITE'] = df_historico_jaz['VOLUMEN DE ACEITE'].round(1)
    df_historico_jaz['VOLUMEN DE AGUA'] = df_historico_jaz['VOLUMEN DE AGUA'].round(1)
    df_historico_jaz['BSW'] = df_historico_jaz['BSW'].round(1)


    # Calcular la fecha de hace cuatro años
    ultimo_ano = df_historico_jaz['FECHA'].max() - pd.DateOffset(years=4)

    # Filtrar los datos de los últimos cuatro años
    df_historico_jaz = df_historico_jaz[df_historico_jaz['FECHA'] >= ultimo_ano]
    # Función para obtener los datos de un pozo específico
    def get_well_data(well_name):
        return df_historico_jaz[df_historico_jaz['SARTA'] == well_name]

    # Crear la aplicación Streamlit
    selected_well = st.selectbox(
        'Selecciona un pozo',
        df_historico_jaz['SARTA'].unique()
    )

    df_well = get_well_data(selected_well)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=pd.to_datetime(df_well['FECHA'], dayfirst=True), y=df_well['VOLUMEN DE ACEITE'], mode='lines+markers', name='VOLUMEN DE ACEITE', yaxis='y1', marker=dict(color='green')))
    fig.add_trace(go.Scatter(x=pd.to_datetime(df_well['FECHA'], dayfirst=True), y=df_well['VOLUMEN DE AGUA'], mode='lines+markers', name='VOLUMEN DE AGUA', yaxis='y2', marker=dict(color='blue')))
    fig.add_trace(go.Scatter(x=pd.to_datetime(df_well['FECHA'], dayfirst=True), y=df_well['BSW'], mode='lines+markers', name='BSW', yaxis='y1', marker=dict(color='red')))
    fig.update_layout(
        title=f'Datos del pozo {selected_well}',
        xaxis=dict(title='FECHA', tickformat='%d/%m/%Y'),
        yaxis=dict(title=dict(text='VOLUMEN DE ACEITE (BOPD)')),
        yaxis2=dict(
            title=dict(text='VOLUMEN DE AGUA (BWPD)'),
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

    st.divider()

    cc1, cc2 = st.columns(2)
    with cc1:

        # Paso 1: Obtener la fecha más reciente y la segunda más reciente para cada pozo
        df_historico_jaz_sorted = df_historico_jaz.sort_values(by=[ 'SARTA','FECHA'], ascending=[ True,False])
        latest_data = df_historico_jaz_sorted.groupby('SARTA').nth(0).reset_index()
        second_latest_data = df_historico_jaz_sorted.groupby('SARTA').nth(1).reset_index()
        
        # Renombrar las columnas para diferenciarlas
        latest_data = latest_data.rename(columns={
            'VOLUMEN DE ACEITE': 'VOLUMEN DE ACEITE_LATEST',
            'FECHA': 'FECHA_LATEST'
        })
        
        latest_data = latest_data[['SARTA', 'FECHA_LATEST', 'VOLUMEN DE ACEITE_LATEST']].copy()
        
        second_latest_data = second_latest_data.rename(columns={
            'VOLUMEN DE ACEITE': 'VOLUMEN DE ACEITE_PREVIOUS',
            'FECHA': 'FECHA_PREVIOUS'
        })
        
        second_latest_data = second_latest_data[['SARTA', 'FECHA_PREVIOUS', 'VOLUMEN DE ACEITE_PREVIOUS']].copy()
        
        # Integrar los dos datasets
        comparison_data = pd.merge(latest_data, second_latest_data, on='SARTA')
        
        # Calcular las diferencias
        comparison_data['DIF_VOL_ACEITE'] = comparison_data['VOLUMEN DE ACEITE_LATEST'] - comparison_data['VOLUMEN DE ACEITE_PREVIOUS']
        
        # Agregar un buscador para filtrar por pozo
        selected_pozos = st.multiselect('Selecciona los pozos que deseas ver', comparison_data['SARTA'].unique())
        if selected_pozos:
            comparison_data = comparison_data[comparison_data['SARTA'].isin(selected_pozos)]
        
        # Mostrar la tabla comparativa en Streamlit
        st.dataframe(comparison_data, hide_index=True)
        
    with cc2:    
        # Paso 3: Calcular el total de producción para la última prueba y la prueba anterior
        total_production_latest = latest_data['VOLUMEN DE ACEITE_LATEST'].sum()
        total_production_latest = total_production_latest.round(1)
        total_production_previous = second_latest_data['VOLUMEN DE ACEITE_PREVIOUS'].sum()
        total_production_previous = total_production_previous.round(1)
        dif_prod = (total_production_latest - total_production_previous).round(1)
        
        # Crear una gráfica de barras para comparar la producción total
        fig = go.Figure()
        fig.add_trace(go.Bar(y=[total_production_latest], name='Total Volumen de Aceite (Última Prueba)', marker_color='green', text=[total_production_latest], textposition='auto'))
        fig.add_trace(go.Bar(y=[total_production_previous], name='Total Volumen de Aceite (Prueba Anterior)', marker_color='blue', text=[total_production_previous], textposition='auto'))
        fig.add_trace(go.Bar(y=[dif_prod], name='Diferencia', marker_color='red', text=[dif_prod], textposition='auto'))
        
        fig.update_layout(
            title='Comparación de Producción Total entre pruebas',
            yaxis=dict(title='Volumen de Aceite'),
            barmode='group'
        )
        # Mostrar la gráfica en Streamlit
        st.plotly_chart(fig)

    st.divider()
    c1, c2, c3 = st.columns([2, 2, 3])

    with c1:
        pozos_mayor_dif = comparison_data[['SARTA', 'DIF_VOL_ACEITE']].sort_values(by='DIF_VOL_ACEITE', ascending=False).head(10)
        pozos_mayor_dif['DIF_VOL_ACEITE'] = pozos_mayor_dif['DIF_VOL_ACEITE'].round(1)

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(pozos_mayor_dif.columns),
                        fill_color='green',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[pozos_mayor_dif[col].tolist() for col in pozos_mayor_dif.columns],
                    align='left')
        )])

        fig.update_layout(
            title_text='MAYOR DIF ENTRE PRUEBAS',
            title_font_size=15,
            title_x=0.03,
            margin=dict(t=30)
        )

        st.plotly_chart(fig)

    with c2:
        pozos_mayor_dif = comparison_data[['SARTA', 'DIF_VOL_ACEITE']].sort_values(by='DIF_VOL_ACEITE', ascending=True).head(10)
        pozos_mayor_dif['DIF_VOL_ACEITE'] = pozos_mayor_dif['DIF_VOL_ACEITE'].round(1)

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(pozos_mayor_dif.columns),
                        fill_color='green',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[pozos_mayor_dif[col].tolist() for col in pozos_mayor_dif.columns],
                    align='left')
        )])

        fig.update_layout(
            title_text='MENOR DIF ENTRE PRUEBAS',
            title_font_size=15,
            title_x=0.03,
            margin=dict(t=30)
        )

        st.plotly_chart(fig)

    with c3:
        latest_dates = df_historico_jaz.groupby('SARTA')['FECHA'].max().reset_index()
        latest_data = pd.merge(latest_dates, df_historico_jaz, on=['SARTA', 'FECHA'])
        top_10_wells = latest_data.sort_values(by='VOLUMEN DE ACEITE', ascending=False).head(10)
        top_10_wells = top_10_wells[['SARTA', 'FECHA', 'VOLUMEN DE ACEITE']].copy()

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(top_10_wells.columns),
                        fill_color='green',
                        font=dict(color='white', size=12),
                        align='left'),
            cells=dict(values=[top_10_wells[col].tolist() for col in top_10_wells.columns],
                    align='left')
        )])

        fig.update_layout(
            title_text='10 Pozos con Mayor Producción en GIRASOL',
            title_font_size=15,
            title_x=0.1,
            margin=dict(t=40)
        )

        st.plotly_chart(fig)