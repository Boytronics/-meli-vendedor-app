import streamlit as st
import requests
import re
from bs4 import BeautifulSoup

st.set_page_config(page_title="Perfil de Vendedor - Mercado Libre")
st.title("🔍 Buscar perfil del vendedor en Mercado Libre")
st.write("Pega la URL del producto y obtén el perfil y datos del vendedor.")

url_producto = st.text_input("URL del producto de Mercado Libre")

def obtener_seller_id(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, allow_redirects=True)
        r.raise_for_status()
        final_url = r.url
        match = re.search(r"/MLM(\d+)", final_url)
        real_id = f"MLM{match.group(1)}" if match else None

        if real_id:
            api_url = f"https://api.mercadolibre.com/items/{real_id}"
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return data.get("seller_id", None)

        soup = BeautifulSoup(r.text, "html.parser")
        vendedor_tag = soup.find("a", href=lambda h: h and "/perfil/" in h)
        if vendedor_tag:
            return vendedor_tag['href'].split("/perfil/")[-1]

        return None
    except Exception as e:
        st.error(f"Error accediendo a la URL: {e}")
        return None

def obtener_datos_vendedor(seller_id):
    try:
        url = f"https://api.mercadolibre.com/users/{seller_id}"
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except:
        return {}

def obtener_top_productos(seller_id, limit=5):
    try:
        url = f"https://api.mercadolibre.com/sites/MLM/search?seller_id={seller_id}&sort=sold_quantity_desc&limit={limit}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        total = data['paging']['total']
        productos = [{
            'title': item['title'],
            'sold': item.get('sold_quantity', 0),
            'link': item['permalink']
        } for item in data['results']]
        return total, productos
    except:
        return 0, []

# Ejecución principal
if url_producto:
    seller_id = obtener_seller_id(url_producto)
    if seller_id:
        vendedor = obtener_datos_vendedor(seller_id)
        total_publicaciones, top_productos = obtener_top_productos(seller_id)

        nickname = vendedor.get("nickname", seller_id)
        reputation = vendedor.get("seller_reputation", {})
        transactions = reputation.get("transactions", {})
        ratings = transactions.get("ratings", {})

        perfil_url = f"https://www.mercadolibre.com.mx/perfil/{nickname}"

        st.success(f"Vendedor encontrado: **{nickname}**")
        st.markdown(f"🔗 [Ver perfil del vendedor]({perfil_url})")

        st.markdown(f"""
        ### 📊 Información del vendedor
        - **ID:** {seller_id}
        - **País:** {vendedor.get("country_id", "N/A")}
        - **Nivel:** {reputation.get("level_id", "Desconocido")}
        - **Power Seller:** {reputation.get("power_seller_status", "No")}
        - **Ventas completadas:** {transactions.get("completed", 0)}
        - **Canceladas:** {transactions.get("canceled", 0)}
        - **👍 Positivas:** {ratings.get("positive", 0.0) * 100:.1f}%
        """)

        st.markdown(f"""
        ### 🛒 Publicaciones
        - **Total activas:** {total_publicaciones}
        """)

        if top_productos:
            st.markdown("### 🥇 Top productos más vendidos")
            for i, producto in enumerate(top_productos, start=1):
                st.markdown(f"{i}. [{producto['title']}]({producto['link']}) — Vendidos: {producto['sold']}")
        else:
            st.info("No se encontraron productos destacados.")
    else:
        st.warning("No se encontró el vendedor.")

