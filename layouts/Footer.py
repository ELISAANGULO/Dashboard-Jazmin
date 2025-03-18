import streamlit as st
from paginas.register import register

def footer_login():
    footer_login = """
    <style>
        .footer {
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #393f81;
        }
        .footer a {
            color: #17a2b8;
            text-decoration: none;
        }
        .footer a:hover {
            color: #0056b3;
        }
        .footer .footer-bottom {
            margin-top: 20px;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }
    </style>

    <div class="footer">
        <p class="mb-1 pb-lg-2" style="color: #393f81;">
            No tienes cuenta? <a href="#" class="small text-info" onclick="window.location.href='?page=register'">Registrarse aquí</a>
        </p>
        <div class="d-flex text-center items-center justify-content-center">
            <a href="#!" class="small text-info me-1">Términos de uso.</a>
            <a href="#!" class="small text-info">Política de privacidad</a>
        </div>
        <footer class="site-footer style-1 bg-img-fix footer-action d-flex justify-content-center" id="footer">
            <div class="footer-bottom text-center">
                <div class="d-flex justify-content-center">
                    <span class="copyright-text">
                        Copyright © 2025. Desarrollado por Elisa Angulo. Todos los derechos reservados
                    </span>
                </div>
            </div>
        </footer>
    </div>
    """
    st.markdown(footer_login, unsafe_allow_html=True)

# Llamada a la función para mostrar el footer
footer_login()