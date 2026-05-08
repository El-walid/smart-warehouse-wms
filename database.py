import sqlite3

DB_NAME = "warehouse_tracking.db"

def init_db():
    """Creates the two-table architecture if it doesn't exist yet."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Table 1: The Concept (Catalogue) - NOW WITH QUANTITY
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Catalogue_Produits (
            SKU_Base TEXT PRIMARY KEY,
            Designation TEXT,
            Image_Path TEXT,
            Quantity INTEGER DEFAULT 0
        )
    """)
    
    # Table 2: The Physical Reality (Stock)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Stock_Physique (
            Code_Barre TEXT PRIMARY KEY,
            SKU_Base TEXT,
            Date_Creation TEXT,
            Statut TEXT,
            FOREIGN KEY(SKU_Base) REFERENCES Catalogue_Produits(SKU_Base)
        )
    """)
    conn.commit()
    conn.close()