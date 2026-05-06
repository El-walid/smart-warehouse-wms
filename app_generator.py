import streamlit as st
import qrcode
from PIL import Image
import io

st.set_page_config(page_title="Générateur d'Étiquettes", page_icon="🖨️", layout="wide")

st.title("🖨️ Générateur d'Étiquettes Intelligentes")
st.markdown("Créez des étiquettes uniques avec QR Code et photo pour sécuriser votre entrepôt.")

# --- THE INPUT FORM ---
with st.form("label_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        product_name = st.text_input("Désignation du Produit", placeholder="ex: Moteur Électrique 1.5cv")
        base_ref = st.text_input("Référence de Base (SKU)", placeholder="ex: MOT-150")
        quantity = st.number_input("Quantité reçue (Nombre d'étiquettes à générer)", min_value=1, max_value=100, value=5)
        
    with col2:
        # The genius feature: Uploading the product picture
        uploaded_image = st.file_uploader("Photo du produit (Optionnel mais recommandé)", type=["jpg", "jpeg", "png"])
        
    submit_button = st.form_submit_button("Générer les Étiquettes", type="primary")

# --- THE GENERATION ENGINE ---
if submit_button and product_name and base_ref:
    st.markdown("---")
    st.subheader(f"✅ Lot généré : {quantity} x {product_name}")
    
    # Process the uploaded image if it exists
    product_img = None
    if uploaded_image:
        product_img = Image.open(uploaded_image)
        # Resize to make it small enough for a physical sticker
        product_img.thumbnail((150, 150))
    
    # Display the generated labels in a clean grid (4 columns wide)
    cols = st.columns(4)
    
    for i in range(quantity):
        # 1. Create the unique Serial ID (e.g., MOT-150-001)
        unique_id = f"{base_ref}-{i+1:03d}"
        
        # 2. Generate the QR Code for this specific ID
        qr = qrcode.QRCode(box_size=4, border=2)
        qr.add_data(unique_id)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # 3. Render the Label in the Streamlit UI
        col_index = i % 4
        with cols[col_index]:
            st.markdown(f"**{unique_id}**") # The unique code
            if product_img:
                st.image(product_img, use_container_width=False) # The idiot-proof picture
            st.image(qr_img.get_image(), width=120) # The scannable QR
            st.caption(product_name[:20]) # Shortened product name
            st.divider()

    # (Future feature: A button here to export all these to a single A4 PDF for the printer)
    st.success("Toutes les étiquettes sont prêtes à être imprimées et collées sur les produits physiques !")
elif submit_button:
    st.error("Veuillez remplir au moins la Désignation et la Référence.")