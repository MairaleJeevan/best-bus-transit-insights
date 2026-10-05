# BEST Bus Transit Insights

> **Academic Project**: Public Transport Usage and Optimization Analysis  
> **Study Corridor**: Chembur, Kurla East, Nehru Nagar (Mumbai, Maharashtra)  
> **Target Population**: 100 Surveyed Commuters  
> **Primary Technology Stack**: Google Forms, Google Sheets, Python, Pandas, NumPy, Flask, HTML5, CSS3, JavaScript, Chart.js

---

## 🚌 Executive Summary

**BEST Bus Transit Insights** is an interactive, survey-driven data engineering and visual analytics platform designed to analyze public bus commuter patterns, route congestion, peak-hour reliability, bottlenecks (SCLR, Chembur Station, Diamond Garden), overcrowding, and digital payment adoption along the high-density Chembur–Kurla transit corridor in Mumbai.

The platform implements an end-to-end data processing pipeline where raw survey responses collected via Google Forms are synchronized with Google Sheets, ingested and cleaned using Pandas/NumPy, served via a lightweight Flask REST API, and visualized through a rich, dark-themed Single Page Application powered by Chart.js.

---

## 🏗️ Architecture & Pipeline

```
Google Form (Survey Collection)
      ↓
Google Sheet (Central Data Store) / Local CSV
      ↓
Python Data Loader (Fallback & In-Memory Cache)
      ↓
Data Cleaner (Deduplication, Imputation, Route Normalization)
      ↓
Filter Service (Multi-Criteria Slicing BEFORE Calculation)
      ↓
Metrics & Chart Data Engine (NumPy & Pandas Vectorized Aggregations)
      ↓
Flask REST API (/api/analytics, /api/summary, /api/refresh, /api/export-csv)
      ↓
HTML5 / CSS3 / JavaScript (Modular SPA)
      ↓
Chart.js Visualizations & Diagnostic Operational Matrix
```

---

## 🌟 Key Features

1. **Dynamic Top-Level KPI Cards**:
   - *Active Survey Base* (Total validated respondents)
   - *Peak Delay Exposure* (% delayed at bottlenecks)
   - *Overcrowding Index* (% reporting severe/high crowding)
   - *Digital Payment Share* (% Chalo App, Smart Card, UPI/QR)
   - *Frequent BEST Users* (% regular riders)
   - *Average Waiting Time* (Calculated peak interval delay)
   - *Most Used Route* (Highest volume corridor)
   - *Top Bottleneck* (Primary congestion choke point)

2. **8 Interactive Visualizations (Chart.js)**:
   - **Route Usage Distribution**: Vertical bar chart highlighting routes 363, 364, 367, 383, 399, 430, 501, 663, and A-21.
   - **Peak-Hour Frequency & Reliability**: Grouped bar chart comparing bus frequency vs arrival punctuality ratings (1–5 scale).
   - **Operational Bottlenecks Intensity**: Horizontal bar chart detailing delay rates at SCLR, Chembur Station, Diamond Garden, etc.
   - **Hourly Overcrowding vs Bus Frequency Trend**: Line chart analyzing density curves across the day.
   - **Transit Health Profile**: 5-dimensional radar chart (Frequency, Timeliness, Capacity, Cleanliness, Digital Adoption).
   - **Payment Method Adoption**: Donut chart detailing Chalo App, Smart Card, Cash, and UPI shares.
   - **Commuter Demographics**: Age bracket and occupational profile breakdown.
   - **Bus Physical Condition**: Ratings across cleanliness, seating comfort, and ventilation.

3. **Detailed Operational Parameter Diagnostic Table**:
   - Searchable, status-filtered diagnostic table comparing positive vs negative sentiment across core indicators with automated classification tags (`High Adoption`, `Acceptable`, `Operational Concern`, `Critical Deficit`) and actionable recommendations.

4. **Multi-Parameter Pre-Analytics Filtering**:
   - Filter by Route Focus (363, 364, 367, 383, 399, 430, 501, 663, or A-21), Commuter Segment, Age Group, Occupation, and Travel Frequency. Slices DataFrame before computing KPIs and charts.

5. **Data Management & Export**:
   - Near-real-time data refresh (manual button + configurable auto-refresh intervals).
   - Export currently filtered survey records as timestamped CSV files.
   - Drag-and-drop CSV dataset upload with schema validation.

---

## 🛠️ Technology Stack & Viva Justifications

| Component | Technology | Why It Was Used (Viva Defense) |
| :--- | :--- | :--- |
| **Data Ingestion** | Google Forms | Frictionless, mobile-friendly survey collection directly accessible to commuters. |
| **Data Storage** | Google Sheets | Cloud-native collaborative spreadsheet serving as central survey database without heavy RDBMS overhead. |
| **Language** | Python 3.x | Standard language for data engineering, rapid web services, and analytics. |
| **Data Cleaning** | Pandas | Vectorized table manipulation, missing value imputation, and robust deduplication. |
| **Calculations** | NumPy | High-performance numerical computations and statistical aggregations. |
| **API Layer** | Python Flask | Minimalist, fast WSGI microservice serving REST endpoints with CORS and structured error handling. |
| **Frontend UI** | HTML5 / CSS3 | Modern CSS custom properties, responsive CSS Grid and Flexbox with transit dark theme and glassmorphism. |
| **Interactivity** | Vanilla JavaScript | Modular ES6+ client architecture without bulky framework dependencies. |
| **Visualizations**| Chart.js (v4.x) | HTML5 Canvas-based rendering engine supporting animations and responsive charts. |
| **Data Export** | Microsoft Excel / CSV | Standard portable formats for offline reporting and data sharing. |

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.9+ installed on your system.
- Git (optional).

### 2. Setup Virtual Environment & Install Dependencies

```powershell
# Navigate to project root
cd c:\Clg_Project

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Run the Backend Server

```powershell
python backend/app.py
```

Open your browser and navigate to:  
👉 **`http://127.0.0.1:5000`**

---

## 📊 Configuration (.env)

Create a `.env` file based on `.env.example`:

```env
# Server Settings
FLASK_ENV=development
PORT=5000
DEBUG=True

# Data Source: "csv" or "google_sheets"
DATA_SOURCE=csv
CSV_DATA_PATH=data/sample_data.csv

# Google Sheets Configuration (Required if DATA_SOURCE=google_sheets)
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
```

### Setting Up Google Sheets API
1. Enable **Google Sheets API** & **Google Drive API** in Google Cloud Console.
2. Create a **Service Account** and download its JSON key file as `service_account.json`.
3. Share your survey response Google Sheet with the Service Account client email address with **Viewer** role.
4. Set `DATA_SOURCE=google_sheets` and `GOOGLE_SHEET_ID` in `.env`.

---

## 🧪 Automated Testing

Run the full automated test suite (30 unit and integration tests):

```powershell
.\venv\Scripts\pytest -v
```

Tests cover:
- CSV Loading & Google Sheets fallback
- Deduplication and missing value imputation
- Route and boolean normalization
- Dynamic KPI and metric calculations
- Multi-criteria DataFrame filtering
- Chart data transformations and radar scoring
- Full REST API endpoints and CSV export

---

## 📂 Project Structure

```
best-bus-analytics/
├── backend/
│   ├── app.py                      # Flask Application Server & Entry Point
│   ├── config.py                   # Configuration & Environment Handler
│   ├── requirements.txt            # Python Dependencies
│   ├── routes/
│   │   ├── analytics_routes.py     # Analytics & Export REST Endpoints
│   │   └── data_routes.py          # Health, Refresh & Upload Endpoints
│   ├── services/
│   │   ├── analytics_service.py    # Ingestion, Caching & Orchestration
│   │   ├── google_sheets.py        # Google Sheets API Service
│   │   └── refresh_service.py      # Cache Synchronization Handler
│   ├── analytics/
│   │   ├── data_loader.py          # Abstract, CSV & Sheets Data Loaders
│   │   ├── data_cleaner.py         # Imputation, Deduplication & Normalization
│   │   ├── filters.py              # Pre-Analytics Filter Service
│   │   ├── metrics.py              # Dynamic KPIs & Parameter Diagnostics
│   │   └── chart_data.py           # Chart.js Visual Transformations
│   └── utils/
│       ├── logger.py               # Structured Logging Utility
│       └── validation.py           # Schema & File Validation Rules
├── frontend/
│   ├── index.html                  # Single Page Application Dashboard Shell
│   ├── css/
│   │   ├── styles.css              # Dark Theme & Modern Design System
│   │   └── responsive.css          # Desktop, Tablet, Mobile Breakpoints
│   └── js/
│       ├── app.js                  # Main Application Orchestrator
│       ├── api.js                  # REST API Client Service
│       ├── charts.js               # Chart.js Visualizations Manager
│       ├── filters.js              # Analytical Filters Manager
│       ├── dashboard.js            # KPI, Parameter Table & DOM Controller
│       └── utils.js                # Toasts & Formatting Helpers
├── data/
│   └── sample_data.csv             # 100-Commuter Demo/Reference Survey Dataset
├── notebooks/
│   └── analysis.ipynb              # Exploratory Data Analysis & Prototyping
├── docs/                           # Academic Project Documentation
│   ├── 01-introduction.md          # Problem Statement, Existing/Proposed Systems, Photo Proof
│   ├── 02-literature-review.md     # Technology Survey, Questionnaire & Collection Plan
│   ├── 03-methodology.md           # Methodology & Full UML Models
│   ├── 04-system-modules.md        # System Modules Breakdown
│   ├── 05-data-design.md           # Schema, Constraints & Google Sheets Guide
│   ├── 06-ui-design.md             # UI Design System & Hierarchy
│   ├── 07-conclusion.md            # Findings, Operational Recommendations & Scope
│   ├── 08-references.md            # Academic & Industry References
│   └── diagrams/                   # Mermaid UML Source Files
│       ├── er-diagram.md
│       ├── class-diagram.md
│       ├── flowchart.md
│       ├── activity-diagram.md
│       ├── sequence-diagram.md
│       └── architecture.md
├── tests/                          # Automated Pytest Test Suite
│   ├── test_phase1.py
│   ├── test_data_loader.py
│   ├── test_data_cleaner.py
│   ├── test_filters.py
│   ├── test_metrics.py
│   ├── test_chart_data.py
│   └── test_api_endpoints.py
├── .env.example
├── .gitignore
└── README.md
```

---

## 🎓 Viva & Presentation Talking Points

1. **Why not a SQL Database?**
   - Survey datasets (100–10,000 records) are analytical (OLAP) rather than transactional (OLTP). Storing data in Google Sheets connected directly to Pandas in-memory DataFrames eliminates database server maintenance, reduces latency, and allows non-technical surveyors to view and edit responses in real time.
2. **How is real-time synchronization achieved?**
   - When new responses arrive via Google Forms into Google Sheets, clicking `[Refresh Data]` or triggering auto-refresh invokes the `AnalyticsService` to pull new rows, re-clean data, invalidate the in-memory cache, and re-render the dashboard in sub-seconds.
3. **How does filtering work?**
   - Filters are passed as HTTP query parameters to the Flask API. The backend `FilterService` slices the Pandas DataFrame **before** executing KPI aggregations, radar dimensions, and chart distributions, ensuring 100% mathematical integrity across all visual components.
