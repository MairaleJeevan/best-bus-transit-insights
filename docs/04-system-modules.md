# Chapter 4: System Modules & Functional Architecture

## 4.1 Basic System Modules

### 4.1.1 Home Dashboard Module (`frontend/index.html`, `dashboard.js`)
- **Brand Identity & Header**: Displays project title, corridor focus, live data source status badge, auto-refresh interval dropdown, manual refresh button, dataset upload button, and CSV export trigger.
- **Top Analytical Filter Bar**: Allows multi-criteria filtering across Route Focus, Commuter Segment, Age Group, Occupation, and Travel Frequency.
- **Dynamic KPI Cards Grid**: 8 responsive metric cards displaying real-time calculations for:
  1. *Active Survey Base* (Total respondents)
  2. *Peak Delay Exposure* (% delayed at bottlenecks)
  3. *Overcrowding Index* (% reporting severe/high rush load)
  4. *Digital Payment Share* (% Chalo / Smart Card / UPI)
  5. *Frequent BEST Users* (% regular daily commuters)
  6. *Average Waiting Time* (Minutes spent waiting)
  7. *Most Used Route* (Highest volume corridor)
  8. *Top Bottleneck* (Primary traffic choke point)

### 4.1.2 Interactive Visualizations Module (`charts.js`)
Contains 8 Chart.js canvas components:
1. **Route Usage Distribution**: Vertical bar chart highlighting demand on routes 364, 383, 363, A-21, etc.
2. **Peak-Hour Frequency & Reliability**: Grouped bar chart comparing bus frequency vs arrival punctuality ratings (1-5 scale).
3. **Operational Bottlenecks Intensity**: Horizontal bar chart identifying delay rates at SCLR, Chembur Station, Diamond Garden, etc.
4. **Hourly Overcrowding vs Bus Frequency Trend**: Line chart analyzing density curves across the day (handles honest availability check).
5. **Transit Health Profile**: Multidimensional radar chart scoring Frequency, Timeliness, Capacity, Cleanliness, and Digital Adoption (0-100 scale).
6. **Payment Method Adoption**: Donut chart detailing Chalo App, Smart Card, and Cash shares.
7. **Commuter Demographics**: Bar chart breakdown of age brackets and professions.
8. **Bus Physical Condition**: Bar chart evaluating fleet cleanliness, seating, and ventilation.

### 4.1.3 Detailed Parameter Diagnostic Module (`metrics.py`, `dashboard.js`)
- Searchable, filterable diagnostic matrix comparing positive vs negative sentiment across core transit indicators.
- Automated health classification tags: `High Adoption`, `Acceptable`, `Operational Concern`, `Critical Deficit`.
- Actionable operational recommendation rules for BEST depot management and municipal planners.

## 4.2 Data Processing Modules

### 4.2.1 Data Loader (`data_loader.py`, `google_sheets.py`)
- Reads raw survey rows from Google Sheets via Google Service Account authentication or local CSV file.
- Automatic fallback mechanism ensuring high availability if Google Sheets API quota is reached or credentials are unconfigured.

### 4.2.2 Data Cleaner (`data_cleaner.py`)
- Standardizes column headers using alias dictionary.
- Validates and deduplicates records by `Response_ID`.
- Imputes missing rating and text fields using conservative median/modal values.
- Normalizes route codes (e.g. "Route 364" -> "364", "A21" -> "A-21").
- Normalizes boolean indicators ("Yes", "No").
- Generates data pipeline validation summary report.

### 4.2.3 Analytics Engine & Filter Service (`metrics.py`, `filters.py`, `chart_data.py`)
- Slices cached DataFrames before calculations.
- Computes aggregations, proportions, and Chart.js data structures.
