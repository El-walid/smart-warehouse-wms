# 🏭 Smart Warehouse Management System (WMS)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Mobile_UI-FF4B4B?style=for-the-badge&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![QR Code](https://img.shields.io/badge/QR_Code-Serialization-black?style=for-the-badge)

## 📋 Executive Summary
A lightweight, mobile-first Warehouse Management System designed to bridge the gap between physical factory floors and digital databases. 

Many industrial businesses lose thousands of dollars annually due to manual paper tracking, lost inventory, and data entry delays. This suite solves that by introducing **Digital Twins & Unique Serialization**. Every physical item generated receives a unique QR code (DNA), which is printed, attached to the physical object, and tracked in real-time via smartphone scanners.

## 🏗️ System Architecture
This system is built on a serverless, zero-configuration architecture, making it perfect for rapid deployment in industrial environments without requiring heavy IT infrastructure.

### 1. 🗄️ The Vault (`database.py`)
A normalized, dual-table SQLite database:
* **Catalogue_Produits:** Stores the core product concepts (SKU, Name, Total Quantity).
* **Stock_Physique:** Tracks the exact physical location and status of *individual* items using unique Serial IDs (e.g., `MOT-150-142533-001`).

### 2. 🖨️ The Creator (`app_generator.py`)
The intake engine for new inventory. 
* Managers input product details and quantities.
* The system injects the data into the SQL vault.
* It dynamically compiles a **Print-Ready A4 PDF** containing a perfectly formatted grid of unique QR code stickers for the warehouse workers to apply to the pallets.

### 3. 📱 The Tracker (`app_scanner.py`)
A mobile-first application designed for the warehouse floor.
* **Dual Input:** Supports both smartphone camera scanning and traditional USB Laser Barcode Scanners.
* **Real-Time CRUD:** Workers scan a physical box to instantly pull its database record and update its status (e.g., *En Stock* ➡️ *Expédié* or *Perdu*) with a single tap.

---

## 🚀 How to Deploy Locally

### Prerequisites
* Python 3.10+
* A smartphone or webcam (for testing the scanner)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/smart-warehouse-wms.git](https://github.com/YOUR-USERNAME/smart-warehouse-wms.git)
   cd smart-warehouse-wms

```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. Install dependencies:
```bash
pip install -r requirements.txt

```



*(Note: Ensure your `requirements.txt` includes `streamlit`, `qrcode`, `Pillow`, `fpdf2`, and `streamlit-qrcode-scanner`)*

### Running the Suite

You can run the modules independently depending on the user's role:

**For the Office Manager (To generate labels):**

```bash
streamlit run app_generator.py

```

**For the Warehouse Worker (To scan labels):**

```bash
streamlit run app_scanner.py

```

---

## 👤 Author

**El Walid El Alaoui Fels**

* **Role:** Consultant in Data Engineering & Automation
* **Focus:** Cloud Data Platforms, ETL Pipelines, and Business Process Automation
