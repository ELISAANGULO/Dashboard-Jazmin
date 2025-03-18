import streamlit as st
from streamlit import session_state as state
import re

def register():
    st.title("Página de Registro")
        # Function to validate email
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email)

    # Function to validate password
    def validate_password(password):
        password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})'
        return re.match(password_regex, password)

    # Function to check if email exists (dummy function for example)
    def email_exists(email):
        # Replace with actual email existence check
        return False

    # Function to create user (dummy function for example)
    def create_user(values):
        # Replace with actual user creation logic
        st.success("User created successfully!")

    # Initial form values
    initial_values = {
        "firstName": "",
        "lastName": "",
        "email": "",
        "password": "",
        "confirmPassword": ""
    }

    # Streamlit form
    st.title("REGÍSTRATE PARA ACCEDER A LA INFORMACION")

    with st.form("registration_form"):
        first_name = st.text_input("Nombre(s)", value=initial_values["firstName"])
        last_name = st.text_input("Apellidos(s)", value=initial_values["lastName"])
        email = st.text_input("Email", value=initial_values["email"])
        password = st.text_input("Contraseña", type="password", value=initial_values["password"])
        confirm_password = st.text_input("Confirmar Contraseña", type="password", value=initial_values["confirmPassword"])
        
        submit_button = st.form_submit_button(label="Registrar")

        if submit_button:
            if not first_name:
                st.error("El nombre es requerido.")
            elif not last_name:
                st.error("Los apellidos son requeridos.")
            elif not email:
                st.error("El email es requerido.")
            elif not validate_email(email):
                st.error("El email tiene un formato errado.")
            elif email_exists(email):
                st.error("El email ya está registrado.")
            elif not password:
                st.error("La contraseña es requerida.")
            elif not validate_password(password):
                st.error("Debe contener 8 caracteres, letras mayusculas y minisculas, y un caracter especial.")
            elif password != confirm_password:
                st.error("La confirmacion debe ser igual al password.")
            else:
                create_user({
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "password": password
                })



