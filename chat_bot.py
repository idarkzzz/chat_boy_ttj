import streamlit as st
import groq as gq


MODELOS = ['llama3-8b-8192','llama3-70b-8192']

# CONFIGURAR LA PAGINA
def configurar_pagina():
    st.set_page_config(page_title="MI PRIMERA PAGINA CON PYTHON" , page_icon="🫡") #cambia el nombre de la ventana del navegadore
    st.title("Bienvenidos a mi chatbot")
    
# MOSTRAR EL SIDEBAR CON LOS MODELOS
def mostrar_sidebar():
    st.sidebar.title("ELEJÍ TU MODELO DE IA FAVORITO")
    modelo = st.sidebar.selectbox("¿ Cuál elejís ?", MODELOS,index=0)
    st.write(f"ELEJISTE EL MODELO: {modelo}")
    return modelo
    
# UN CLIENTE GROQ
def crear_cliente_groq():
    groq_api_key = st.secrets["GROQ_API_KEY"] #almacenar la api key de groq
    return gq.Groq(api_key=groq_api_key)

#mensajes
def inicializacion_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state["mensajes"] = []
        
def mostrar_historial_chat():
    for mensaje in st.session_state["mensajes"]:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

            
def obtener_mensaje_usuario():
    return st.chat_input("Enviar mensaje")

def agregar_mensaje_de_usuario(role,content):
    st.session_state["mensajes"].append({"role": role, "content": content})


def mostrar_mensajes(role,content):
    with st.chat_message(role):
        st.markdown(content)
        

def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
    return respuesta.choices[0].message.content




#FLUJO DE LA APP
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_groq()
    inicializacion_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    mostrar_historial_chat()
    
    if mensaje_usuario :
        agregar_mensaje_de_usuario("user", mensaje_usuario)
        mostrar_mensajes("user", mensaje_usuario)
        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes)
        agregar_mensaje_de_usuario("assistant",mensaje_modelo)
        mostrar_mensajes("assistant",mensaje_modelo)

if __name__ == '__main__': # Si este archivo es el archivo principal , entonces EJECUTá
    ejecutar_app()



