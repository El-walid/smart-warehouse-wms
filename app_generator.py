import streamlit as st
import qrcode
from PIL import Image
import sqlite3
from datetime import datetime
from database import init_db, DB_NAME

# 1. Page Config MUST be the first Streamlit command
st.set_page_config(page_title="Générateur d'Étiquettes", page_icon="🖨️", layout="wide")

# 2. Initialize the database (Creates tables if they don't exist)
init_db()

# ---------------------------------------------------------
# 🎨 THE USER INTERFACE
# ---------------------------------------------------------
st.title("🖨️ Générateur d'Étiquettes Intelligentes")
st.markdown("Créez des étiquettes uniques avec QR Code et photo pour sécuriser votre entrepôt.")

# --- THE INPUT FORM ---
with st.form("label_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Désignation du Produit", placeholder="ex: Moteur Électrique 1.5cv")
        base_ref = st.text_input("Référence de Base (SKU)", placeholder="ex: MOT-150").strip().upper()
        quantity = st.number_input("Quantité reçue (Nombre d'étiquettes à générer)", min_value=1, max_value=100, value=5)
        
    with col2:
        uploaded_image = st.file_uploader("Photo du produit (Optionnel mais recommandé)", type=["jpg", "jpeg", "png"])
        
    submit_button = st.form_submit_button("Générer & Sauvegarder", type="primary")

# ---------------------------------------------------------
# ⚙️ THE GENERATION & INSERTION ENGINE
# ---------------------------------------------------------
if submit_button and product_name and base_ref:
    st.markdown("---")
    st.subheader(f"✅ Lot généré et sauvegardé : {quantity} x {product_name}")
    
    # Process the uploaded image if it exists
    product_img = None
    if uploaded_image:
        product_img = Image.open(uploaded_image)
        product_img.thumbnail((150, 150))
    
    # Open the vault to save the data
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Save the Product Concept to the Catalogue
    cursor.execute("""
        INSERT OR IGNORE INTO Catalogue_Produits (SKU_Base, Designation, Image_Path, Quantity)
        VALUES (?, ?, ?)
    """, (base_ref, product_name, "uploaded_image",quantity))
    
    # Display the generated labels in a clean grid (4 columns wide)
    cols = st.columns(4)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for i in range(quantity):
        # 1. Create the unique Serial ID with a timestamp to prevent duplicates
        unique_timestamp = datetime.now().strftime("%H%M%S")
        unique_id = f"{base_ref}-{unique_timestamp}-{i+1:03d}"
        
        # 2. SAVE to the Physical Stock Database
        cursor.execute("""
            INSERT INTO Stock_Physique (Code_Barre, SKU_Base, Date_Creation, Statut)
            VALUES (?, ?, ?, ?)
        """, (unique_id, base_ref, today_str, "En Stock"))
        
        # 3. Generate the QR Code visual
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(unique_id)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # 4. Render the Label in the Streamlit UI
        col_index = i % 4
        with cols[col_index]:
            st.markdown(f"**{unique_id}**")
            if product_img:
                st.image(product_img, use_container_width=False)
            st.image(qr_img.get_image(), width=120)
            st.caption(product_name[:20])
            st.divider()

    # Commit the saves and close the vault
    conn.commit()
    conn.close()

    st.success("✅ Toutes les étiquettes sont générées ET enregistrées dans la base de données locale !")
    
elif submit_button:
    st.error("⚠️ Veuillez remplir au moins la Désignation et la Référence.")