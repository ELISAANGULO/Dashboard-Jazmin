import streamlit as st
from datetime import datetime
from paginas.jazmin_dinason import jazmin_dinason
from layouts.Footer2 import footer_page
import pyrebase
from paginas.jazmin_pruebas import jazmin_pruebas
from paginas.jazmin_subsuelo import jazmin_subsuelo
from paginas.jazmin_vapor import jazmin_vapor
from paginas.girasol_dinason import girasol_dinason
from paginas.girasol_pruebas import girasol_pruebas
from paginas.girasol_subsuelo import girasol_subsuelo
from paginas.girasol_vapor import girasol_vapor
from paginas.urn_dinason import urn_dinason
from paginas.urn_pruebas import urn_pruebas
from paginas.urn_subsuelo import urn_subsuelo
from paginas.urn_vapor import urn_vapor
import re

# Configuración inicial de la página
st.set_page_config(page_title="DAHSBOARD JAZ-GIR-URN", page_icon='imagenes/plataforma-petrolera.png', layout="wide")

# Estilo CSS para personalizar encabezado
header_style = """
<style>
    .header {
        background-color: #008000; /* Verde */
        color: white;
        padding: 15px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header h1 {
        margin: 0;
        padding-left: 10px;
        color: white;
    }
    .header img {
        vertical-align: middle;
        margin-right: 10px;
        width: 60px;
        height: 60px;
    }
</style>
"""
st.markdown(header_style, unsafe_allow_html=True)

# Encabezado principal
st.markdown('''
<div class="header">
    <img src="https://companieslogo.com/img/orig/EC-5b71716b.png?download=true" alt="Logo">
    <h1>DAHSBOARD JAZ/GIR/URN</h1>
</div>
''', unsafe_allow_html=True)

# Configuración base de datos
firebaseConfig = {
    'apiKey': "AIzaSyDdPwku1Hb9NwKB-S66OC7idIjjxYVl50U",
    'authDomain': "dahboard-6285c.firebaseapp.com",
    'projectId': "dahboard-6285c",
    'databaseURL': "https://dashboardjazmin-default-rtdb.europe-west1.firebasedatabase.app/",
    'storageBucket': "dahboard-6285c.firebasestorage.app",
    'messagingSenderId': "34105296621",
    'appId': "1:34105296621:web:4a7d09f557ea4a78d92ee4",
    'measurementId': "G-XXS04M3VP4"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
# Autenticación
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def validate_email(email):
    if not email:
        return "El correo electrónico es obligatorio."
    if not re.match(r"[^@]+@ecopetrol\.com\.co", email):
        return "El correo electrónico debe ser válido y pertenecer a @ecopetrol.com.co."
    return None

def validate_password(password):
    if not password:
        return "La contraseña es obligatoria."
    if len(password) < 6:
        return "La contraseña debe tener al menos 6 caracteres."
    return None

if st.session_state['logged_in']:
    st.sidebar.success(f'Bienvenid@ *{st.session_state["name"]}*')
    if st.sidebar.button("🔒Cerrar sesión"):
        st.session_state['logged_in'] = False
        st.rerun()
else:
    choice = st.selectbox('Login/Signup', ['Login', 'Sign up'])

    # Obtener datos del usuario
    email = st.text_input('Please enter your email address')
    password = st.text_input('Please enter your password', type='password')

    # Registro de usuario
    if choice == 'Sign up':
        handle = st.text_input('Please input your app user name')
        submit = st.button('🔓Create account')

        if submit:
            email_error = validate_email(email)
            password_error = validate_password(password)
            if email_error:
                st.error(email_error)
            elif password_error:
                st.error(password_error)
            else:
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success('Your account is created successfully!')
                    st.balloons()
                    user = auth.sign_in_with_email_and_password(email, password)
                    db.child(user['localId']).child("Handle").set(handle)
                    db.child(user['localId']).child("ID").set(user['localId'])
                    st.session_state['logged_in'] = True
                    st.session_state['name'] = handle
                    st.rerun()
                except Exception as e:
                    st.error(f"Error en la creación de la cuenta: {e}")

    # Inicio de sesión
    if choice == 'Login':
        login = st.button('🔑Login')
        if login:
            email_error = validate_email(email)
            password_error = validate_password(password)
            if email_error:
                st.error(email_error)
            elif password_error:
                st.error(password_error)
            else:
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.session_state['logged_in'] = True
                    st.session_state['name'] = db.child(user['localId']).child("Handle").get().val()
                    st.rerun()
                except Exception as e:
                    st.error(f"Error en el inicio de sesión: {e}")


if st.session_state['logged_in']:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    pages = {
        "JAZMIN": [
            {"func": jazmin_dinason, "title": "🛢️Dinason", "icon": "🛢️"},
            {"func": jazmin_subsuelo, "title": "🏔️Subsuelo", "icon": "🌋"},
            {"func": jazmin_pruebas, "title": "🧪Pruebas", "icon": "🧪"},
            {"func": jazmin_vapor, "title": "💨Vapor", "icon": "💨"}
        ],
        "GIRASOL": [
            {"func": girasol_dinason, "title": "🛢️Dinason", "icon": "⚙️"},
            {"func": girasol_subsuelo, "title": "🏔️Subsuelo", "icon": "🏔️"},
            {"func": girasol_pruebas, "title": "🧪Pruebas", "icon": "🧫"},
            {"func": girasol_vapor, "title": "💨Vapor", "icon": "💨"}
        ],
        "URN": [
            {"func": urn_dinason, "title": "🛢️Dinason", "icon": "🛢️"},
            {"func": urn_subsuelo, "title": "🏔️Subsuelo", "icon": "🌋"},
            {"func": urn_pruebas, "title": "🧪Pruebas", "icon": "🧪"},
            {"func": urn_vapor, "title": "💨Vapor", "icon": "💨"}
        ],
    }

    selected_page = st.sidebar.selectbox(
        "Seleccione una categoría", list(pages.keys())
    )

    selected_subpage = st.sidebar.selectbox(
        "Seleccione una página", [page["title"] for page in pages[selected_page]]
    )

    # Página de configuración
    if selected_page == "JAZMIN" and selected_subpage == "🛢️Dinason":
        footer_page()
        jazmin_dinason()
    elif selected_page == "JAZMIN" and selected_subpage == "🏔️Subsuelo":
        footer_page()
        jazmin_subsuelo()
    elif selected_page == "JAZMIN" and selected_subpage == "🧪Pruebas":
        footer_page()
        jazmin_pruebas()
    elif selected_page == "JAZMIN" and selected_subpage == "💨Vapor":
        footer_page()
        jazmin_vapor()
    elif selected_page == "GIRASOL" and selected_subpage == "🏔️Subsuelo":
        footer_page()
        girasol_subsuelo()
    elif selected_page == "GIRASOL" and selected_subpage == "🧪Pruebas":
        footer_page()
        girasol_pruebas()
    elif selected_page == "GIRASOL" and selected_subpage == "💨Vapor":
        footer_page()
        girasol_vapor()
    elif selected_page == "GIRASOL" and selected_subpage == "🛢️Dinason":
        footer_page()
        girasol_dinason()
    elif selected_page == "URN" and selected_subpage == "🧪Pruebas":
        footer_page()
        urn_pruebas()
    elif selected_page == "URN" and selected_subpage == "💨Vapor":
        footer_page()
        urn_vapor()
    elif selected_page == "URN" and selected_subpage == "🏔️Subsuelo":
        footer_page()
        urn_subsuelo()
    elif selected_page == "URN" and selected_subpage == "🛢️Dinason":
        footer_page()
        urn_dinason()
    else:
        pass