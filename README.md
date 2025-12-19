# Global Power Plant Visualization Dashboard

An interactive **multi-tab Dash application** that visualizes the global distribution, composition, and capacity of power plants using the **Global Power Plant Database (World Resources Institute)**.  

This project provides a detailed exploration of global energy infrastructure, renewable vs non-renewable trends, and country-level fuel mixes — powered by `Plotly`, `Dash`, and `Pandas`.

---

## 🚀 Features

- **Multi-Tab Interactive Dashboard**
  - **Tab 1** – Global Renewable vs Non-Renewable Capacity  
  - **Tab 2** – Capacity Trends & Commissioning Year Analysis  
  - **Tab 3** – Global Power Plant Map with Animated Year Slider  
  - **Tab 4** – Regional Fuel Mix Comparison (Bar + Histogram + Treemap)
- **Data Cleaning & Aggregation:**
  - Duplicate and null removal  
  - Standardized fuel and country names  
  - Renewable vs Non-Renewable labeling  
  - Capacity outlier filtering
- **Dynamic Filters:**
  - By fuel type, year range, energy category, and country
- **Responsive Visuals:**
  - Bubble plots, deviations, boxplots, area trends, and global treemaps  

---

## Project Structure

```plaintext
global-power-plant-visualization/
│
├── data/                         # Dataset and loader script
│   └── global_power_plant_database.csv
│
├── src/                          # Preprocessing, visualization, and dashboard code
│   ├── data_loader.py            # Reads CSV and returns raw DataFrame
│   ├── preprocess.py             # Cleans and prepares data for analysis
│   ├── visualizations.py         # Plotly functions for Tabs 1–4
│   └── dashboard.py              # Main Dash app (entry point)
│
├── docs/                         # Proposal, mockups, and markdown project notes
│   ├── Visualization_Mockup.pdf
│   ├── GPP_Dataset_Proposal.docx
│   └── project_notes.md          # Takeaways and markdown explanations
│
├── results/                      # Generated figures or HTML exports (optional)
│
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
└── LICENSE                       # License file
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/global-power-plant-visualization.git
cd global-power-plant-visualization
```

### 2. Create and Activate a Virtual Environment

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Dashboard

Once dependencies are installed, run the Dash application:

```bash
python src/dashboard.py
```

Then open your browser and visit:

```
http://127.0.0.1:8050/
```

💡 **Tip:**  
Use `CTRL+C` in the terminal to stop the server.  
You can also deploy this app using `gunicorn`, `Render`, or `Heroku`.

---

## Dashboard Overview

### **Tab 1 – Global Renewable vs Non-Renewable Capacity**
Explores 2017 global installed capacity and energy generation across fuels.  
Includes bubble plots, deviation charts, boxplots, and renewable share comparisons.

**Key Insight:**  
Non-renewables (especially Gas and Coal) dominate global capacity, while Hydro remains the only large-scale renewable counterpart.

---

### **Tab 2 – Capacity Trends & Commissioning Year Analysis**
Tracks installed capacity growth from 1950–2016.  
Visualizes energy transition over time using area charts and plant-level scatterplots.

**Key Insight:**  
Global capacity surged post-2000 due to Gas and Coal — but renewables (Wind & Solar) now drive growth, signaling a global energy shift.

---

### **Tab 3 – Global Power Plant Map**
Interactive geo-visualization of global power plants by fuel type, year, and energy category.  
Includes an animated year slider (1950–2016).

**Key Insight:**  
Non-renewable plants are concentrated in North America, Europe, and Asia — while renewables (especially Hydro, Wind, Solar) show rapid global spread in recent years.

---

### **Tab 4 – Regional Fuel Mix Comparison**
Country-level exploration of installed capacity, plant size distribution, and treemap analysis by energy category.

**Key Insight:**  
Energy portfolios vary widely:
- USA → Gas & Coal dominated  
- Canada → Hydro majority  
- Brazil → Balanced renewables  
- China → Coal-heavy with growing Solar/Wind share

---

## Dataset Information

- **Source:** Global Power Plant Database (World Resources Institute)  
- **Coverage:** 34,000+ plants worldwide (2017 snapshot)  
- **Fields:**  
  - Country, name, latitude/longitude  
  - Capacity (MW), primary fuel, commissioning year  
  - Estimated annual generation (GWh, 2017)
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)

---

## Dependencies

```txt
dash>=3.0.0
plotly>=5.15.0
pandas>=2.0.0
numpy>=1.25.0
gunicorn>=21.2.0
```

---

## Project Notes

All markdown “Takeaway” and analytical explanations are stored in:
```
/docs/project_notes.md
```

These describe the rationale and insights behind each visualization tab.

---

##  Author

**Sandeep Kang**  
IUPUI – Global Power Plant Visualization Project  
Course: [Visualization Design, Analysis, & Evaluation INFO-H 517 (22685), Fall 2025]

---

## 📄 License

This project is licensed under the **MIT License**.  
See the `LICENSE` file for details.

---

## 💡 Acknowledgments

- **World Resources Institute (WRI)** for the *Global Power Plant Database*  
- **Plotly Dash** for the web visualization framework  
- **Pandas & NumPy** for data manipulation and analysis  
- **IUPUI Faculty Advisors** for project guidance and review

## References

- World Resources Institute (WRI).  
  *Global Power Plant Database, Version 1.3.0.*  
  Available at: [https://datasets.wri.org/dataset/globalpowerplantdatabase](https://datasets.wri.org/dataset/globalpowerplantdatabase)  
  License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
