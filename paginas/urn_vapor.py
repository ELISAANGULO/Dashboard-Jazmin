import streamlit as st


def urn_vapor():

    st.title("Pagina 2")

    if "id" in st.session_state:
        st.write("El id es: ",st.session_state.id)
    else:
        st.write("No hay Id")