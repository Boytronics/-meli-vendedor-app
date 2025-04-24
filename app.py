import streamlit as st
import requests
from urllib.parse import urlparse
import re

st.set_page_config(page_title="Perfil de Vendedor - Mercado Libre")
st.title("🔍 Buscar perfil del vendedor en Mercado Libre")
st.write("Pega la URL del producto y abre el perfil del vendedor.")

url_producto = st.text_input("URL del producto de Mercado Libre")

def extraer_id_producto(url):
    # Extrae el ID como MLM-123456789 o directamente en la URL
    match = re.search(r"(MLM-\d+)", url)
    if match:
        return match.group(1)
    match = re.search(r"/MLM(\d+)", url)
    if match:
        return f"MLM{match.group(1)}"
    return None

def obtener_seller_id(id_producto):
    try:
        api_url = f"https://api.mercadolibre.com/items/{id_producto}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        return data.get("seller_id", None)
    except Exception as e:
        st.error(f"Error accediendo a la API: {e}")
        return None

if url_producto:
    id_producto = extraer_id_producto(url_producto)
    if id_producto:
        seller_id = obtener_seller_id(id_producto)
        if seller_id:
            perfil_url = f"https://www.mercadolibre.com.mx/perfil/{seller_id}"
            st.success(f"Vendedor encontrado: **{seller_id}**")
            st.markdown(f"[🔗 Ver perfil del vendedor]({perfil_url})", unsafe_allow_html=True)
        else:
            st.warning("No se encontró el vendedor.")
    else:
        st.error("No se pudo extraer el ID del producto.")

