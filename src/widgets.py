import streamlit as st

# Configuración de la página en modo ancho
st.set_page_config(layout="wide")

# Título de la aplicación
st.title('Recomendador de Películas')

# Simulación de algunas películas
peliculas = {
    'Acción': [('Acción Movie 1', 1994, '16+', 120), ('Acción Movie 2', 2003, '12+', 73)],
    'Comedia': [('Comedia Movie 1', 1992, '7+', 100), ('Comedia Movie 2', 2011, 'TP', 180)],
    'Drama': [('Drama Movie 1', 1988, '18+', 120), ('Drama Movie 2', 2000, '16+', 90)]
}

# Expander para información sobre la app
with st.expander('Acerca de esta app'):
    st.write("""
        Esta aplicación permite agregar y eliminar peliculas y las recomienda basadas en el género, el rango de años y duracion seleccionados por el usuario.
        Utiliza datos simulados y es solo un ejemplo de cómo puedes estructurar tu aplicación Streamlit.\n
        \nLa clasificación de edad se basa en:
        \nTP - Todo Público (Apto para todos los públicos)
        \n7+ - No recomendada para menores de 7 años
        \n12+ - No recomendada para menores de 12 años
        \n16+ - No recomendada para menores de 16 años
        \n18+ - No recomendada para menores de 18 años
        \nEl codigo de la pelicula es el numero en el listado al que esta asignado la vista de todas las peliculas
    """)
    st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)



# Entrada de datos en la barra lateral
st.sidebar.header('Agregar pelicula')
genero_pelicula = st.sidebar.selectbox('Elige el género de la película:', ['-', 'Acción', 'Comedia', 'Drama'])
nombre_pelicula = st.sidebar.text_input('ingrese el nombre de la pelicula:')
año_pelicula = st.sidebar.slider('Selecciona el año de la pelicula:', 1980, 2020, 2010)
clasificacion_pelicula = st.sidebar.selectbox('Elige la clasificacion de genero de la película:', ['-', 'TP', '7+', '12+', '16+', '18+'])
time = st.sidebar.slider('Selecciona la duracion de la pelicula:', 0, 200, 200)
if st.sidebar.button('Agregar pelicula'):
    tmp = (nombre_pelicula, año_pelicula, clasificacion_pelicula, time)
    peliculas[genero_pelicula].append(tmp)

st.sidebar.header('Eliminar pelicula')
geny = st.sidebar.selectbox('Elige el género de la película:', ['--', 'Acción', 'Comedia', 'Drama'])
cod = st.sidebar.number_input('ingrese el numero de la pelicula:', 0, 999)
if st.sidebar.button('eliminar pelicula'):
    del peliculas[geny][cod]

st.sidebar.header('Buscar pelicula')
nom= st.sidebar.text_input('Ingresa el nombre de la película:')
genero = st.sidebar.selectbox('Elige el género de la película:', ['', 'Acción', 'Comedia', 'Drama'])
año_inicio, año_fin = st.sidebar.slider('Selecciona el rango de años:', 1980, 2020, (1990, 2010))
edad = st.sidebar.slider('Selecciona la edad:', 0, 150, 0)
mins = st.sidebar.slider('Selecciona la duracion de la pelicula:', 0, 200, 0)


# Lógica para recomendar películas basada en la entrada
def obtener_recomendaciones(genero, año_inicio, año_fin, edad, nom, mins):
    recomendaciones = []

    for nombre, año, clas_edad, dur in peliculas[genero]:
        # Revisar si el año de la película está dentro del rango especificado
        if año >= año_inicio and año <= año_fin:
            if mins == dur:
                if nom.lower() in nombre.lower():
                    if clas_edad == 'TP':
                        recomendaciones.append((nombre, año, clas_edad, dur))
                    elif edad >= 18:
                        recomendaciones.append((nombre, año, clas_edad, dur))
                    elif edad >= 16 and clas_edad != '18+':
                        recomendaciones.append((nombre, año, clas_edad, dur))
                    elif edad >= 12 and clas_edad != '18+' and clas_edad != '16+':
                        recomendaciones.append((nombre, año, clas_edad, dur))
                    elif edad >= 7 and clas_edad != '18+' and clas_edad != '16+' and clas_edad != '12+':
                        recomendaciones.append((nombre, año, clas_edad, dur))
    return recomendaciones


with st.expander('ver todas las peliculas'):
    cont = 0
    st.header('Acción')
    for peli_A, anio_A, clas_e_A, dur_A in peliculas['Acción']:
        st.write(f"{cont}. **{peli_A}** ({anio_A}) - **{clas_e_A}** ({dur_A} mins)")
        cont += 1

    cont = 0
    st.header('Comedia')
    for peli_C, anio_C, clas_e_C, dur_C in peliculas['Comedia']:
        st.write(f"{cont}. **{peli_C}** ({anio_C}) - **{clas_e_C}** ({dur_C} mins)")
        cont += 1

    cont = 0
    st.header('Drama')
    for peli_D, anio_D, clas_e_D, dur_D in peliculas['Drama']:
        st.write(f"{cont}. **{peli_D}** ({anio_D}) - **{clas_e_D}** ({dur_D} mins)")
        cont += 1


# Output de recomendaciones
st.header('Recomendaciones de Películas')
if genero and año_inicio and año_fin and edad:
    recomendaciones = obtener_recomendaciones(genero, año_inicio, año_fin, edad, nom, mins)
    if recomendaciones:
        for pelicula, año, clas_edad, dur in recomendaciones:
            st.write(f"**{pelicula}** ({año}) - **{clas_edad}** ({dur} mins)")
    else:
        st.write("No se encontraron películas que coincidan con los criterios.")
else:
    st.write("Por favor, selecciona un género y ajusta el rango de años para obtener recomendaciones.")
