# Chapter 2: Literature Review & Technology Survey

## 2.1 Survey of Technology (Viva Justifications)

Each technology in the **BEST Bus Transit Insights** architecture was deliberately chosen for specific technical advantages in survey data pipelines:

| Technology | Role in Project | Technical Justification for Viva |
| :--- | :--- | :--- |
| **Python 3.x** | Core Language | Robust data engineering ecosystem, clean syntax, type hinting, and rapid prototyping capabilities. |
| **Pandas** | Data Processing | Vectorized DataFrame operations, flexible missing value handling, column renaming, filtering, and aggregation. |
| **NumPy** | Numerical Math | High-performance numerical computations, array operations, and statistics calculation. |
| **Google Forms** | Data Ingestion | Ubiquitous, mobile-responsive survey tool enabling effortless field data collection among commuters without app installation. |
| **Google Sheets** | Primary Storage | Cloud-native collaborative spreadsheet serving as real-time survey database with automated Google Forms syncing. |
| **Flask** | REST API Layer | Lightweight, un-opinionated Python web micro-framework delivering sub-millisecond REST API responses with minimal overhead. |
| **Vanilla JavaScript (ES6+)** | Frontend Interactivity | Modular, dependency-free client scripting ensuring maximum speed, zero build-step overhead, and direct DOM control. |
| **Chart.js (v4.x)** | Data Visualization | HTML5 Canvas-based rendering engine supporting interactive animations, responsive resizing, radar charts, and dark themes. |
| **HTML5 & CSS3** | UI Structure & Styling | Modern CSS custom properties (variables), glassmorphism, responsive CSS Grid and Flexbox layouts. |
| **Microsoft Excel** | Data Inspection / Export | Industry-standard tabular inspection and offline backup format for analytical datasets. |
| **Tableau** | Reference Visualization | Enterprise BI reference for validating chart types and interactive storytelling benchmarks. |

## 2.2 Survey Questionnaire & Interview Questions
The survey questionnaire captures key commuter dimensions:
1. **Demographics**: Age Group, Occupation, Daily Travel Frequency.
2. **Transit Choices**: Primary BEST Route Number (e.g. 364, 383, 363, A-21).
3. **Operational Ratings (1 to 5 Likert Scale)**:
   - Peak-Hour Bus Frequency Adequacy
   - Schedule Arrival Reliability / Punctuality
   - Cabin Overcrowding Severity (Severe, High, Moderate, Low)
   - Bus Fleet Physical Condition (Cleanliness, Seating Comfort, Ventilation)
4. **Traffic & Infrastructure**: Bottleneck Delay Exposure and Primary Bottleneck Location (SCLR, Chembur Station, Diamond Garden).
5. **Digital Transition**: Preferred Payment & Ticketing Method (Chalo App, Smart Card, Cash, UPI).

## 2.3 Data Collection Plan
- **Corridor Focus**: Chembur – Kurla East – Nehru Nagar.
- **Target Sample Size**: 100 verified local commuters.
- **Sampling Method**: Stratified random sampling across students, private employees, government staff, and self-employed commuters at peak morning (8:00 AM - 11:00 AM) and evening (5:30 PM - 8:30 PM) intervals.
