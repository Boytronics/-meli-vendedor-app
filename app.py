import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

st.set_page_config(page_title="Perfil de Vendedor - Mercado Libre")
st.title("🔍 Buscar perfil del vendedor en Mercado Libre")
st.write("Pega la URL del producto y abre el perfil del vendedor.")

url_producto = st.text_input("URL del producto de Mercado Libre")

def extraer_vendedor_de_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    seller_id = query.get("seller_id", [None])[0]
    return seller_id

def obtener_vendedor(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # A: Buscar href con /perfil/
        vendedor_tag = soup.find("a", href=lambda h: h and "/perfil/" in h)
        if vendedor_tag:
            return vendedor_tag['href'].split("/perfil/")[-1]

        # B: Buscar por clase CSS usada normalmente
        vendedor_por_clase = soup.find("a", class_="ui-pdp-seller__link-trigger")
        if vendedor_por_clase and "/perfil/" in vendedor_por_clase.get("href", ""):
            return vendedor_por_clase.get("href").split("/perfil/")[-1]

        # C: Buscar dentro del div seller-info
        vendedor_info = soup.find("div", {"id": "seller-info"})
        if vendedor_info:
            link = vendedor_info.find("a")
            if link and "/perfil/" in link.get("href", ""):
                return link.get("href").split("/perfil/")[-1]

        # D: Extraer desde la URL si todo falla
        return extraer_vendedor_de_url(url)

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

