import streamlit as st
import qrcode
from PIL import Image
import sqlite3
import tempfile
from datetime import datetime
from database import init_db, DB_NAME
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="Générateur d'Étiquettes", page_icon="🖨️", layout="wide")

# 2. Initialize the database
init_db()

# ---------------------------------------------------------
# 🎨 THE USER INTERFACE
# ---------------------------------------------------------
st.title("🖨️ Générateur d'Étiquettes Intelligentes")
st.markdown("Créez des étiquettes uniques avec QR Code et exportez-les en PDF pour l'impression.")

with st.form("label_form"):
    col1, col2 = st.columns(2)
    with col1:
        product_name = st.text_input("Désignation du Produit", placeholder="ex: Moteur Électrique 1.5cv")
        base_ref = st.text_input("Référence de Base (SKU)", placeholder="ex: MOT-150").strip().upper()
        quantity = st.number_input("Quantité reçue", min_value=1, max_value=100, value=6)
    with col2:
        uploaded_image = st.file_uploader("Photo du produit (Optionnel)", type=["jpg", "jpeg", "png"])
        
    submit_button = st.form_submit_button("Générer & Sauvegarder", type="primary")

# ---------------------------------------------------------
# ⚙️ THE GENERATION, DB INSERTION, AND PDF ENGINE
# ---------------------------------------------------------
if submit_button and product_name and base_ref:
    st.markdown("---")
    st.subheader(f"✅ Lot généré : {quantity} x {product_name}")
    
    # Open Vault
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Save to Catalogue
    cursor.execute("""
        INSERT INTO Catalogue_Produits (SKU_Base, Designation, Image_Path, Quantity)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(SKU_Base) DO UPDATE SET Quantity = Quantity + excluded.Quantity
    """, (base_ref, product_name, "uploaded_image", quantity))
    
    cols = st.columns(4)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # We will collect the data here to build the PDF afterward
    labels_for_pdf = []
    
    for i in range(quantity):
        unique_timestamp = datetime.now().strftime("%H%M%S")
        unique_id = f"{base_ref}-{unique_timestamp}-{i+1:03d}"
        
        # Save to Stock
        cursor.execute("""
            INSERT INTO Stock_Physique (Code_Barre, SKU_Base, Date_Creation, Statut)
            VALUES (?, ?, ?, ?)
        """, (unique_id, base_ref, today_str, "En Stock"))
        
        # Create QR
        qr = qrcode.QRCode(box_size=4, border=1)
        qr.add_data(unique_id)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white").get_image()
        
        # Store for PDF
        labels_for_pdf.append({"id": unique_id, "name": product_name, "qr": qr_img})
        
        # Render on Streamlit Screen
        with cols[i % 4]:
            st.markdown(f"**{unique_id}**")
            st.image(qr_img, width=120)
            st.caption(product_name[:20])
            st.divider()

    conn.commit()
    conn.close()
    
    # ---------------------------------------------------------
    # 🖨️ THE PDF BUILDER (A4 Grid Engine)
    # ---------------------------------------------------------
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 10)
    
    # Grid Settings for an A4 Page
    x_start, y_start = 15, 15
    label_w, label_h = 55, 65
    x_space, y_space = 5, 5
    x, y = x_start, y_start

    for i, label in enumerate(labels_for_pdf):
        # Move to next row if 3 columns are filled
        if i > 0 and i % 3 == 0:
            x = x_start
            y += label_h + y_space
        
        # Create a new page if we run out of vertical space
        if y + label_h > 280:
            pdf.add_page()
            x, y = x_start, y_start

        # Draw the sticker border
        pdf.rect(x, y, label_w, label_h)
        
        # Write the ID at the top
        pdf.set_xy(x, y + 3)
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(label_w, 5, label["id"], align="C")
        
        # Insert the QR Code (Using a safe temporary file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            label["qr"].save(tmp.name)
            pdf.image(tmp.name, x=x+10, y=y+10, w=35)
            
        # Write the Product Name at the bottom
        pdf.set_xy(x, y + 50)
        pdf.set_font("helvetica", "", 8)
        pdf.cell(label_w, 5, label["name"][:25], align="C")
        
        # Move X to the right for the next label
        x += label_w + x_space

    # Convert the PDF bytearray into strict bytes for Streamlit
    pdf_bytes = bytes(pdf.output())
    
    st.success("✅ Étiquettes sauvegardées en base de données et prêtes pour l'impression !")
    
    # 3. The Physical Export Button
    st.download_button(
        label="🖨️ Télécharger la Planche PDF",
        data=pdf_bytes,
        file_name=f"Etiquettes_{base_ref}_{today_str[:10]}.pdf",
        mime="application/pdf",
        type="primary"
    )

elif submit_button:
    st.error("⚠️ Veuillez remplir la Désignation et la Référence.")