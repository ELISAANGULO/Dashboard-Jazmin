import streamlit as st

def footer_page():
    footer_page = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #393f81;
            z-index: 1000; /* Asegura que el pie de página esté siempre encima del contenido */
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
        <footer class="site-footer style-1 bg-img-fix footer-action d-flex" id="footer">
            <div class="footer-bottom text-center">
                <div class="d-flex justify-content-center">
                    <span class="copyright-text">
                        <img src='https://companieslogo.com/img/orig/EC-5b71716b.png?download=true' alt='Logo' style='width: 50px; height: auto;'>
                        Copyright © 2025. Desarrollado por Elisa Maria Angulo
                    </span>
                </div>
            </div>
        </footer>
    </div>
    """

    st.markdown(footer_page, unsafe_allow_html=True)

footer_page()