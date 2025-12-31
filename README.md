## 📊 Sales Analytics Dashboard (Python)

A desktop-based **Sales Analytics Dashboard** built using Python that allows users to upload sales data, automatically clean it, generate meaningful **Key Performance Indicators (KPIs)**, and visualize **sales trends** through an interactive GUI.

This project is developed in **phases** to demonstrate real-world data analysis workflow — from raw data handling to visualization and dashboard design.

---

## 🚀 Project Phases

### **Phase 1 – Data Analysis & KPIs**
- Data loading and preprocessing
- Column normalization and validation
- Handling missing and invalid values
- KPI calculations
- Basic visualizations

### **Phase 2 – Enhanced Analytics & Trends**
- Improved data cleaning logic
- Feature engineering (Total Sales, Month, Year)
- Sales trend analysis:
  - Overall sales trend
  - Monthly sales trend
  - Yearly sales trend
- Product, category, and region-wise analysis

### **Phase 3 – GUI Dashboard**
- Interactive desktop application using **Tkinter**
- Sidebar-based navigation
- CSV upload via GUI
- KPI cards display
- Embedded Matplotlib charts
- User-friendly error handling

---

## ✨ Features

### 🔧 Data Processing
- Automatic data cleaning & preprocessing
- Column mapping & validation
- Missing value handling
- Feature engineering

### 📌 Key Performance Indicators (KPIs)
- 💰 Total Revenue
- 🛒 Total Orders
- 📊 Average Order Value
- 🏆 Highest & Lowest Revenue Products
- 🔥 Most & Least Demanded Products
- 🏅 Best Performing Category
- 🌍 Best Performing Region

### 📈 Data Visualizations
- Sales trend over time
- Monthly sales trend
- Yearly sales trend
- Product-wise sales
- Category contribution
- Region-wise sales

### 🖥 GUI Dashboard
- Built using Tkinter
- Sidebar navigation
- CSV file upload
- KPI cards
- Graph selection dropdown
- Error handling for missing or invalid data

---

## 🛠 Technologies Used
- **Python**
- **Pandas**
- **Matplotlib**
- **Tkinter**
- **Pillow (PIL)**

---

## 📁 Project Structure

```
Sales-Analytics-Dashboard/
│
├── sales_analysis.py      # Data cleaning, KPIs & plots
├── gui.py                 # Tkinter GUI application
├── images/
│   ├── icon.ico
│   └── notfound.png
├── sample_data.csv
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

1. Clone the repository

```bash
git clone  https://github.com/bariraa/business-sales-analysis.git
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the GUI

```bash
python gui.py
```

---

## 🔮 Future Scope

- Data filtering options (by date, product, category, region)
- Enhanced GUI styling
- Export reports (PDF / CSV)
- Advanced analytics & forecasting

---

## 📌 Author

**Barira**
Software Engineering Student
NED University of Engineering & Technology

---
