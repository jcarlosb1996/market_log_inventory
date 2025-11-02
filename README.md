# MarketLog Inventory System

A Django web application that lets users manage their online sales inventory — track items, record sales across platforms (Facebook, eBay)
and view real-time summaries of stock and performance.

## 🔧 Features

### ➕ Add Products
Easily add new inventory items with title, price, and image.
<img width="1432" height="810" alt="Screenshot 2025-11-02 at 12 37 15 PM" src="https://github.com/user-attachments/assets/72b72dee-a7e2-47a1-8267-a7869b447c0e" />

### 🏷️ Track Sales
Record sales across multiple channels (Facebook, eBay).
<img width="754" height="573" alt="Screenshot 2025-11-02 at 12 44 46 PM" src="https://github.com/user-attachments/assets/ebf4745d-cc16-427f-8b23-a03cc106d6aa" />

### 📦 Inventory Overview
Real-time dashboard with total items, sold-out count, and platform breakdown.
<img width="1434" height="814" alt="Screenshot 2025-11-02 at 12 36 35 PM" src="https://github.com/user-attachments/assets/9565d643-dd97-49bb-8775-0883618d005f" />

### 💰 Profit Tracking
Automatic fee deduction and net profit calculation for each sale.
<img width="1434" height="802" alt="Screenshot 2025-11-02 at 12 37 37 PM" src="https://github.com/user-attachments/assets/028b0a28-9567-4c38-89a7-789c1b1d3c38" />
<img width="1440" height="900" alt="Screenshot 2025-11-02 at 12 47 34 PM" src="https://github.com/user-attachments/assets/e684b5ef-98db-42cc-938e-f595821a1a22" />


## 🧠 Tech Stack
- Django (Python)
- SQLite (local dev)
- Bootstrap 5
- HTML & CSS templates

## ⚙️ Setup Instructions
```bash
git clone https://github.com/jcarlosb1996/market_log_inventory.git
cd market_log_inventory
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
