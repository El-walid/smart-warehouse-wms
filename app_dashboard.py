import streamlit as st
import sqlite3
import pandas as pd
from database import DB_NAME

st.set_page_config(page_title="Tableau de Bord WMS", page_icon="📊", layout="wide")

st.title("📊 Tableau de Bord Stratégique")
st.markdown("Vue globale de l'inventaire et des mouvements d'entrepôt.")

# Connect to Vault
conn = sqlite3.connect(DB_NAME)

# 1. TOP LEVEL METRICS (The KPI Row)
st.subheader("Indicateurs Clés (KPIs)")
col1, col2, col3, col4 = st.columns(4)

# Query active stock
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM Stock_Physique WHERE Statut = 'En Stock'")
total_active_items = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM Stock_Physique WHERE Statut = 'Expédié'")
total_shipped = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT SKU_Base) FROM Catalogue_Produits")
total_skus = cursor.fetchone()[0]

cursor.execute("""
    SELECT SUM(cp.Prix_Unitaire) 
    FROM Stock_Physique sp 
    JOIN Catalogue_Produits cp ON sp.SKU_Base = cp.SKU_Base 
    WHERE sp.Statut = 'En Stock'
""")
total_value = cursor.fetchone()[0] or 0.0

col1.metric("📦 Articles en Stock (Total)", total_active_items)
col2.metric("🚚 Articles Expédiés", total_shipped)
col3.metric("🏷️ Modèles Uniques (SKU)", total_skus)
col4.metric("💰 Valeur du Stock", f"{total_value:,.2f} MAD")

st.markdown("---")

# 2. INVENTORY BREAKDOWN TABLE
st.subheader("Stock Disponible par Modèle")

# We write a SQL query to count individual serialized items and group them by SKU
query = """
SELECT 
    cp.Designation AS 'Produit',
    cp.SKU_Base AS 'SKU',
    cp.Categorie AS 'Catégorie',
    COUNT(sp.Code_Barre) AS 'Quantité Physique en Stock',
    cp.Prix_Unitaire AS 'Prix Unitaire (MAD)',
    (COUNT(sp.Code_Barre) * cp.Prix_Unitaire) AS 'Valeur Totale (MAD)'
FROM Catalogue_Produits cp
LEFT JOIN Stock_Physique sp ON cp.SKU_Base = sp.SKU_Base AND sp.Statut = 'En Stock'
GROUP BY cp.SKU_Base
ORDER BY 'Quantité Physique en Stock' DESC
"""
df_stock = pd.read_sql_query(query, conn)
st.dataframe(df_stock, use_container_width=True, hide_index=True)

conn.close()