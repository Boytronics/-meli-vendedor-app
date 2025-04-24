import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Perfil de Vendedor - Mercado Libre")

st.title("🔍 Buscar perfil del vendedor en Mercado Libre")
st.write("Pega la URL del producto y abre el perfil del vendedor.")

url_producto = st.text_input("URL del producto de Mercado Libre")

def obtener_vendedor(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        vendedor_tag = soup.find("a", href=lambda h: h and "/perfil/" in h)
        if vendedor_tag:
            href = vendedor_tag['href']
            vendedor = href.split("/perfil/")[-1]
            return vendedor
        else:
            return None
    except Exception as e:
        st.error(f"Error al procesar la URL: {e}")
        return None

if url_producto:
    vendedor = obtener_vendedor(url_producto)
    if vendedor:
        perfil_url = f"https://www.mercadolibre.com.mx/perfil/{vendedor}"
        st.success(f"Vendedor encontrado: **{vendedor}**")
        st.markdown(f"[🔗 Ver perfil del vendedor]({perfil_url})", unsafe_allow_html=True)
    else:
        st.warning("No se encontró el vendedor en la página.")
