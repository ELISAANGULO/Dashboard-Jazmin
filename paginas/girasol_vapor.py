import streamlit as st 
import pandas as pd 

def girasol_vapor():
    df = pd.read_csv("course_materials_learnstreamlit\LearnStreamlit\Module01\iris.csv")


    # Method 1
    st.write("DATAFRAME")
    # st.dataframe(df)
    # Adding a color style from dataframe

    st.dataframe(df.style.highlight_max(axis=0))


    # Method 2: Static Table
    st.write("STATIC TABLE")
    st.table(df)

    # Method 3: Using superfuncion st.write

    st.write(df.head())

    # Display Json

    st.json({'data':'name'})

    # Display Code

    mycode = """

    def say hello ()
    print("Hello streamlit lovers")

    """

    st.code(mycode)