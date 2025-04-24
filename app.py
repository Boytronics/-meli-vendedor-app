import streamlit as st
import requests
import re

st.set_page_config(page_title="Perfil de Vendedor - Mercado Libre")
st.title("🔍 Buscar perfil del vendedor en Mercado Libre")
st.write("Pega la URL del producto y abre el perfil del vendedor.")

url_producto = st.text_input("URL del producto de Mercado Libre")

def obtener_seller_id_desde_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        
        # Paso 1: seguir redirección a la URL final
        r = requests.get(url, headers=headers, allow_redirects=True)
        r.raise_for_status()
        final_url = r.url

        # Paso 2: extraer ID tipo MLM123456789
        match = re.search(r"/MLM(\d+)", final_url)
        if not match:
            return None

        real_id = f"MLM{match.group(1)}"

        # Paso 3: consultar API de Mercado Libre
        api_url = f"https://api.mercadolibre.com/items/{real_id}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        return data.get("seller_id", None)

    except Exception as e:
        st.error(f"Error accediendo a la API o resolviendo redirección: {e}")
        return None

# Ejecutar búsqueda
if url_producto:
    seller_id = obtener_seller_id_desde_url(url_producto)
    if seller_id:
        perfil_url = f"https://www.mercadolibre.com.mx/perfil/{seller_id}"
        st.success(f"Vendedor encontrado: **{seller_id}**")
        st.markdown(f"[🔗 Ver perfil del vendedor]({perfil_url})", unsafe_allow_html=True)
    else:
        st.warning("No se encontró el vendedor.")
