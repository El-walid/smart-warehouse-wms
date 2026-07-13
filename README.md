# 🏭 Smart Warehouse Management System (WMS)

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Mobile_UI-FF4B4B?style=for-the-badge&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Data_Analytics-150458?style=for-the-badge&logo=pandas)

## 📋 Executive Summary
A lightweight, mobile-first Warehouse Management System designed to bridge the gap between physical factory floors and executive financial dashboards. 

Industrial businesses lose thousands of dollars annually due to manual paper tracking, lost inventory, and blind spots in their asset valuation. This suite solves that by introducing **Financial Serialization**. Every physical item generated receives a unique QR code (DNA) and is tied to a specific financial value and category. The system tracks individual items in real-time on the warehouse floor while automatically aggregating financial KPIs for the executive team.

## 🏗️ System Architecture
This system is built on a serverless, zero-configuration architecture, making it perfect for rapid deployment in industrial environments without requiring heavy IT infrastructure.

### 1. 🗄️ The Vault (`database.py`)
A normalized, dual-table SQLite database:
* **Catalogue_Produits:** Stores the core product concepts (SKU, Name, Category, Unit Price).
* **Stock_Physique:** Tracks the exact physical location, timestamp, and status of *individual* items using unique Serial IDs (e.g., `LEAHTER-100-214821-002`).

### 2. 🖨️ The Creator (`app_generator.py`)
The intake engine for new inventory. 
* Managers input product details, financial categories, and quantities.
* The system injects the data into the SQL vault using intelligent UPSERT logic.
* It dynamically compiles a **Print-Ready A4 PDF** containing a perfectly formatted grid of unique QR code stickers for warehouse workers to apply to incoming pallets.

### 3. 📱 The Tracker (`app_scanner.py`)
A mobile-first application designed for the warehouse floor.
* **Dual Input:** Supports both smartphone camera scanning and traditional USB Laser Barcode Scanners.
* **Contextual Awareness:** Workers scan a physical box to instantly pull its unique database record, update its status (*En Stock* ➡️ *Expédié*), and simultaneously view the global remaining stock for that specific SKU.

### 4. 📊 The Executive Dashboard (`app_dashboard.py`)
The strategic control tower for factory owners and managers.
* **Real-Time KPIs:** Instantly calculates the total financial value of all active inventory in the warehouse.
* **Live Analytics:** Displays grouped stock availability, shipped item counts, and category breakdowns using Pandas dataframes.

---

## 🚀 How to Deploy Locally

### Prerequisites
* Python 3.10+
* A smartphone or webcam (for testing the scanner)

### Installation
1. Clone the repository:
   ```bash
   git clone (https://github.com/El-walid/smart-warehouse-wms.git)
   cd smart-warehouse-wms

2. Create and activate a virtual environment:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate

```


3. Install dependencies:
```bash
pip install -r requirements.txt

```

*(Note: Ensure your `requirements.txt` includes `streamlit`, `qrcode`, `Pillow`, `fpdf2`, `streamlit-qrcode-scanner`, and `pandas`)*

### Running the Suite

You can run the modules independently depending on the user's role:

**For the Office Manager (To generate labels & intake stock):**

```bash
streamlit run app_generator.py

```

**For the Warehouse Worker (To scan labels & update status):**

```bash
streamlit run app_scanner.py

```

**For the Executive (To view financial valuation & KPIs):**

```bash
streamlit run app_dashboard.py

```

---

## 👤 Author

**El Walid El Alaoui Fels**
