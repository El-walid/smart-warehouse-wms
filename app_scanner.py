import streamlit as st
import sqlite3
from database import init_db, DB_NAME
from streamlit_qrcode_scanner import qrcode_scanner  # 👈 THE NEW IMPORT

# 1. Page Config
st.set_page_config(page_title="Scanner d'Entrepôt", page_icon="📱", layout="centered")

# Ensure DB is initialized
init_db()

# ---------------------------------------------------------
# 📱 THE USER INTERFACE
# ---------------------------------------------------------
st.title("📱 Scanner d'Entrepôt Mobile")
st.markdown("Scannez un produit pour voir ses détails ou mettre à jour son statut.")

# --- THE DUAL SCANNER SYSTEM ---
# We create two tabs: one for the Camera, one for the USB Scanner/Manual
tab1, tab2 = st.tabs(["📷 Scanner Caméra", "⌨️ Saisie Manuelle (Douchette)"])

scanned_code = None

with tab1:
    st.info("Autorisez l'accès à la caméra, puis placez le QR Code dans le cadre.")
    # This activates the webcam/phone camera
    camera_result = qrcode_scanner(key='camera_scanner')
    if camera_result:
        scanned_code = camera_result

with tab2:
    # This is your original manual input
    manual_result = st.text_input("🔍 Code Barre du Produit :", key="manual_scanner")
    if manual_result:
        scanned_code = manual_result

st.markdown("---")

# ---------------------------------------------------------
# ⚙️ THE SEARCH & UPDATE ENGINE
# ---------------------------------------------------------
# The rest of your code stays exactly the same!
if scanned_code:
    # 1. Open Vault
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 2. Search for the exact physical item
    cursor.execute("""
        SELECT sp.Code_Barre, cp.Designation, sp.SKU_Base, sp.Statut, sp.Date_Creation
        FROM Stock_Physique sp
        JOIN Catalogue_Produits cp ON sp.SKU_Base = cp.SKU_Base
        WHERE sp.Code_Barre = ?
    """, (scanned_code.strip(),))
    
    product = cursor.fetchone()
    
    if product:
        code, designation, sku, current_status, date_creation = product
        
        st.success("✅ Produit Identifié")
        
        with st.container(border=True):
            st.subheader(designation)
            st.write(f"**Code Unique:** {code}")
            st.write(f"**Modèle (SKU):** {sku}")
            st.write(f"**Date d'entrée:** {date_creation}")
            
            if current_status == "En Stock":
                st.info(f"📍 Statut Actuel : **{current_status}**")
            elif current_status == "Expédié":
                st.success(f"🚚 Statut Actuel : **{current_status}**")
            else:
                st.error(f"⚠️ Statut Actuel : **{current_status}**")

        st.write("### Actions Rapides")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚚 Expédier", use_container_width=True, disabled=(current_status == "Expédié")):
                cursor.execute("UPDATE Stock_Physique SET Statut = 'Expédié' WHERE Code_Barre = ?", (code,))
                conn.commit()
                st.rerun()
                
        with col2:
            if st.button("📦 Remettre en Stock", use_container_width=True, disabled=(current_status == "En Stock")):
                cursor.execute("UPDATE Stock_Physique SET Statut = 'En Stock' WHERE Code_Barre = ?", (code,))
                conn.commit()
                st.rerun()
                
        with col3:
            if st.button("🚨 Déclarer Perdu", use_container_width=True, disabled=(current_status == "Perdu")):
                cursor.execute("UPDATE Stock_Physique SET Statut = 'Perdu' WHERE Code_Barre = ?", (code,))
                conn.commit()
                st.rerun()
                
    else:
        st.error("❌ Produit introuvable. Ce code n'existe pas dans la base de données.")
        
    conn.close()