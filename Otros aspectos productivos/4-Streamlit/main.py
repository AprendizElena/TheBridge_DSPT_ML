"""
Una aplicación sencilla, de ejemplo
"""
from PIL import Image
import pandas as pd

import streamlit as st
import streamlit.components.v1 as c

# Configuración de página
st.set_page_config(page_title="Cargadores eléctricos",
                   page_icon=":electric_plug:")

# Introducimos un selector
seleccion = st.sidebar.selectbox("Selecciona menu", ["Home", "EDA", "Filtros"])

# Y en base a lo que diga el selector
if seleccion == "Home":

    # Indicamos título
    st.title("Cargadores Madrid")

    with st.expander("¿Qué es esta aplicación?"):
        st.write("""
                 Es una primera aproximación para solucionar la búsqueda 
                 de cargadores eléctricos para facilitar la transición a 
                 otras fuentes de energía
                 """)

    img = Image.open("data/puntos-recarga-madrid.jpg")
    st.image(img)

# Si hemos seleccionado EDA
elif seleccion == "EDA":

    st.write("Análisis exploratorio de datos")

    df = pd.read_csv("data/red_recarga_acceso_publico.csv", sep=";")
    st.write(df.head())

    file = open("data/heatmap.html", "r")

    c.html(file.read(), height=300)

# Si hemos seleccionado filtros
elif seleccion == "Filtros":

    st.write("Filtros aplicados a la selección")

    df = pd.read_csv("data/red_recarga_acceso_publico.csv", sep=";")
    df.rename(columns={"latitud":"lat",
                       "longitud":"lon"}, 
                       inplace=True)

    barrio = st.sidebar.selectbox("Selecciona el barrio", ["TODOS"] + list(df['DISTRITO'].unique()))
    f_cargadores = st.sidebar.radio("Selecciona nº de cargadores",
                                    sorted(df['Nº CARGADORES'].unique()))

    cargadores_bool = st.sidebar.checkbox("Aplicar filtro cargadores")

    if barrio == "TODOS":
        st.write("Conteo de cargadores:" + " " + str(df['Nº CARGADORES'].sum()))
        st.write(df)
        st.map(df)
    elif cargadores_bool :
        suma = df[df['DISTRITO'] == barrio]['Nº CARGADORES'].sum()
        st.write("Conteo de cargadores:" + " " + str(suma))
        st.write(df[(df['DISTRITO'] == barrio) & (df['Nº CARGADORES'] == f_cargadores)] )
        st.map(df[(df['DISTRITO'] == barrio) & (df['Nº CARGADORES'] == f_cargadores)])
    else:
        suma = df[df['DISTRITO'] == barrio]['Nº CARGADORES'].sum()
        st.write("Conteo de cargadores:" + " " + str(suma))
        st.write(df[(df['DISTRITO'] == barrio)])
        st.map(df[(df['DISTRITO'] == barrio)])

    valor = st.sidebar.slider("Valor mínimo", min_value=0, max_value=100, value=0)
    texto = st.sidebar.text_input("Buscar")

    st.sidebar.multiselect("Selecciona opciones", ["1","2","3"])
    st.sidebar.date_input("Fecha inicio")