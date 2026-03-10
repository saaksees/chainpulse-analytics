# ⚡ ChainPulse Analytics

### Feel the pulse of your supply chain

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-0.775_AUC-FF6600?style=flat)
![Prophet](https://img.shields.io/badge/Prophet-90_Day_Forecast-4285F4?style=flat)
![SQLite](https://img.shields.io/badge/SQLite-Version_Control-003B57?style=flat)
![Status](https://img.shields.io/badge/Status-Active_Development-10b981?style=flat)

---

## What Is ChainPulse?

ChainPulse is an end-to-end supply chain
analytics platform built on 180,000 real
orders from the DataCo Supply Chain dataset.
It predicts delivery failures before they
happen, forecasts demand 90 days ahead,
segments customers for targeted action,
and finds cross-sell opportunities using
NLP — all in a live Flask web application
with role-based access control and full
dataset version history.

---

## Key Results

| Metric | Value |
|--------|-------|
| Dataset | 180,519 orders · 3 years |
| Total Revenue Analyzed | $36,784,735 |
| Late Delivery Rate | 57.3% |
| XGBoost ROC-AUC | 0.775 |
| Revenue at Risk | $2,494,632 |
| Customers Segmented | 14,282 |
| Forecast Horizon | 90 days · 5 categories |
| Products NLP Analyzed | 118 |

---

## Features

### Analytics Pages
- **EDA Explorer** — Revenue trends,
regional breakdown, late rate analysis
- **Risk Analyzer** — Live XGBoost
inference with What-If simulator
- **Demand Forecast** — Prophet 90-day
forecast with confidence intervals
- **Customer Intel** — RFM segmentation
+ KMeans clustering, 7 segments
- **NLP Insights** — LDA topic modeling,
bigram analysis, cross-sell detection

### What-If Simulator
Change shipping mode, region, category
and instantly see new risk prediction,
probability comparison, and dollar
savings per order.

### Smart Data Upload
- Drag and drop CSV upload
- Fuzzy column name matching
- Data validator with feedback
- AutoML: auto-selects best model
for any uploaded dataset

### Version Control
- Every upload = permanent SQLite snapshot
- Switch between versions instantly
- Side-by-side version comparison

### Authentication + RBAC

| Role | Access |
|------|--------|
| Admin | Full + user management |
| Analyst | Upload + view + reports |
| Viewer | Dashboards + reports |

### PDF Reports
One-click branded PDF download
on every analytics page.

### Automation
- Nightly pipeline with APScheduler
- MD5 change detection
- Email alerts on KPI breaches

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web Framework | Flask + Jinja2 |
| ML Classification | XGBoost |
| Forecasting | Facebook Prophet |
| Clustering | KMeans + RFM |
| NLP | NLTK + Gensim LDA |
| Database | SQLite |
| Auth | Flask-Login + Bcrypt |
| Scheduling | APScheduler |
| PDF | ReportLab |
| Charts | Chart.js + Matplotlib |

---

## Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/saaksees/chainpulse-analytics.git
cd chainpulse-analytics
```

### 2. Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Download the dataset
Download DataCo Supply Chain Dataset
from Kaggle and place it at: 
data/raw/DataCoSupplyChainDataset.csv

📊 Kaggle link:
https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

### 5. Create users config
```bash
cp config/users.json.example config/users.json
```
Then run the app once — it will
auto-create default users.

### 6. Run the pipeline
```bash
python run_pipeline.py
```
This runs all 6 analysis scripts.
Takes approximately 9 minutes.

### 7. Start the app
```bash
python run_app.py
```

### 8. Open in browser
http://localhost:5000

### Default credentials

| Username | Password | Role |
|----------|----------|------|
| admin | chainpulse123 | Admin |
| analyst | analyst123 | Analyst |
| viewer | viewer123 | Viewer |

---

## Project Structure

```
chainpulse-analytics/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── upload_routes.py
│   ├── auth.py
│   ├── auth_routes.py
│   ├── validator.py
│   ├── column_mapper.py
│   ├── ml_predictor.py
│   ├── database.py
│   ├── version_manager.py
│   ├── scheduler.py
│   ├── alerting.py
│   ├── auto_model_selector.py
│   └── report_generator.py
├── scripts/
│   ├── 01_eda.py
│   ├── 02_demand_forecasting.py
│   ├── 03_delivery_risk_model.py
│   ├── 04_rfm_segmentation.py
│   ├── 05_nlp_analysis.py
│   └── 06_export_powerbi_tables.py
├── templates/
├── static/
│   ├── css/
│   └── js/
├── data/
│   ├── raw/
│   ├── processed/
│   └── powerbi/
├── models/
├── config/
├── run_app.py
├── run_pipeline.py
└── requirements.txt
```

---

## Model Performance

### XGBoost Risk Model
- Accuracy: 72%
- ROC-AUC: 0.775
- SMOTE for class imbalance
- 3 risk levels: High / Medium / Low

### Prophet Forecast

| Category | MAE | 90-Day Total |
|----------|-----|-------------|
| Fishing | $1,357 | $637,294 |
| Cleats | $777 | $391,198 |
| Camping | $885 | $372,519 |
| Cardio | $988 | $336,147 |
| Apparel | $613 | $274,058 |

### RFM Segmentation
- Champions: 10.8% customers → 20% revenue
- At Risk: $602,573 recoverable revenue
- 7 segments with action playbooks

---

## Roadmap

- [x] Core 6-step analytics pipeline
- [x] Flask web application
- [x] XGBoost risk model
- [x] Prophet demand forecasting
- [x] RFM + KMeans segmentation
- [x] NLP analysis
- [x] Auth + RBAC
- [x] SQLite version control
- [x] What-If simulator
- [x] PDF reports
- [x] AutoML pipeline
- [x] Smart column mapping
- [ ] Dynamic multi-dataset support
- [ ] AI insight generator
- [ ] Power BI dashboard
- [ ] Cloud deployment

---

## Author

**Saakshi Jaiswal**

---

## License

MIT