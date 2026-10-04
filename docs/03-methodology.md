# Chapter 3: Methodology & Architectural Modeling

## 3.1 Logical ER Model
In accordance with modern analytical data engineering (OLAP/survey analysis), the logical schema organizes survey observations into analytical entities without needing an RDBMS:

```mermaid
erDiagram
    SURVEY_RESPONSE {
        string response_id PK
        datetime timestamp
        string route_number FK
        string commuter_id FK
        string payment_method FK
        string bottleneck_location FK
    }
    COMMUTER_PROFILE {
        string commuter_id PK
        string age_group
        string occupation
        string frequent_user_status
        string travel_frequency
    }
    ROUTE {
        string route_number PK
        string route_name
        string origin_terminus
        string destination_terminus
    }
    BOTTLENECK {
        string bottleneck_id PK
        string location_name
        string corridor_segment
        string severity_tier
    }
    PAYMENT_METHOD {
        string payment_id PK
        string method_name
        string category
    }
    SURVEY_METRIC {
        string metric_id PK
        string response_id FK
        int bus_frequency_rating
        int schedule_reliability
        string overcrowding_level
        int bus_condition_rating
        int avg_waiting_time_min
    }

    SURVEY_RESPONSE ||--|| COMMUTER_PROFILE : "characterizes"
    SURVEY_RESPONSE }|--|| ROUTE : "travels on"
    SURVEY_RESPONSE }|--|| BOTTLENECK : "encounters"
    SURVEY_RESPONSE }|--|| PAYMENT_METHOD : "pays via"
    SURVEY_RESPONSE ||--|| SURVEY_METRIC : "measures"
```

## 3.2 Class Diagram
The object-oriented design of the Python analytics engine:

```mermaid
classDiagram
    class AbstractDataLoader {
        <<abstract>>
        +load_data() DataFrame*
    }
    class CSVLoader {
        -string file_path
        +load_data() DataFrame
    }
    class GoogleSheetsLoader {
        -string sheet_id
        -string credentials_path
        +load_data() DataFrame
    }
    class DataCleaner {
        -dict column_aliases
        +clean(DataFrame raw_df) Tuple[DataFrame, dict]
        -_normalize_route(val) string
        -_normalize_boolean(val) string
        -_normalize_age_group(val) string
        -_normalize_occupation(val) string
        -_normalize_payment(val) string
    }
    class FilterService {
        +apply_filters(DataFrame df, dict filters) DataFrame
    }
    class MetricsService {
        +get_summary_kpis(DataFrame df) dict
        +get_parameter_diagnostics(DataFrame df) list
    }
    class ChartDataService {
        +get_route_distribution(DataFrame df) dict
        +get_peak_reliability_distribution(DataFrame df) dict
        +get_bottleneck_analysis(DataFrame df) dict
        +get_hourly_analysis(DataFrame df) dict
        +get_transit_health_profile(DataFrame df) dict
        +get_payment_distribution(DataFrame df) dict
        +get_demographics_distribution(DataFrame df) dict
        +get_bus_condition_breakdown(DataFrame df) dict
    }
    class AnalyticsService {
        -DataFrame cached_df
        -dict cached_validation
        -DataCleaner cleaner
        +refresh(string source) dict
        +get_analytics(dict filters) dict
        +get_filter_options() dict
        +export_filtered_csv(dict filters) string
    }

    AbstractDataLoader <|-- CSVLoader
    AbstractDataLoader <|-- GoogleSheetsLoader
    AnalyticsService o-- DataCleaner
    AnalyticsService ..> FilterService
    AnalyticsService ..> MetricsService
    AnalyticsService ..> ChartDataService
```

## 3.3 System Flowchart
```mermaid
flowchart TD
    A[Google Form / Commuter Survey] -->|Auto-Sync| B[Google Sheets Database]
    B -->|Fetch via gspread| C[Python Data Loader]
    D[Local CSV Fallback] -->|File Read| C
    C --> E[Data Cleaner & Deduplicator]
    E --> F[Validation & Normalization Report]
    E --> G[Cleaned DataFrame In-Memory Cache]
    H[Frontend Filter Bar] -->|HTTP Query Params| I[Flask API Layer]
    I --> J[FilterService - Pre-Analytics Slice]
    G --> J
    J --> K[MetricsService - KPI Calculations]
    J --> L[ChartDataService - Visual Transformations]
    K --> M[JSON Analytics Response Payload]
    L --> M
    M --> N[Chart.js & Dashboard UI Render]
```

## 3.4 Activity Diagram
```mermaid
stateDiagram-v2
    [*] --> LoadDashboard
    LoadDashboard --> RequestAPI : GET /api/analytics
    RequestAPI --> LoadDataset : Check In-Memory Cache
    LoadDataset --> CleanNormalize : Validate Columns & Deduplicate
    CleanNormalize --> ApplyFilters : Apply Active Filter Slices
    ApplyFilters --> CalculateKPIs : NumPy / Pandas Aggregations
    CalculateKPIs --> GenerateChartData : Prepare Chart.js Formats
    GenerateChartData --> ReturnJSON : 200 OK Response
    ReturnJSON --> RenderDashboard : Update KPI Cards, 8 Charts, Matrix Table
    RenderDashboard --> UserInteraction : User Slices Filter or Clicks Refresh
    UserInteraction --> ApplyFilters : User Changes Filter
    UserInteraction --> LoadDataset : User Clicks [Refresh Data]
```

## 3.5 Sequence Diagram
```mermaid
sequenceDiagram
    autonumber
    actor User as Commuter / Analyst
    participant UI as Browser (SPA)
    participant Flask as Flask REST API
    participant Analytics as AnalyticsService
    participant Loader as DataLoader / Sheets API
    participant Cleaner as DataCleaner
    participant Charts as Chart.js Engine

    User->>UI: Opens Dashboard or Applies Filter
    UI->>Flask: GET /api/analytics?route=364&age_group=18-25
    Flask->>Analytics: get_analytics(filters)
    opt Cache Expired or Manual Refresh
        Analytics->>Loader: load_data()
        Loader-->>Analytics: Raw DataFrame
        Analytics->>Cleaner: clean(raw_df)
        Cleaner-->>Analytics: Cleaned DataFrame & Validation
    end
    Analytics->>Analytics: FilterService.apply_filters(df, filters)
    Analytics->>Analytics: MetricsService.get_summary_kpis(filtered_df)
    Analytics->>Analytics: ChartDataService.generate_all(filtered_df)
    Analytics-->>Flask: JSON Analytics Payload
    Flask-->>UI: 200 OK (Summary, Charts, Parameters, Validation)
    UI->>Charts: Charts.renderAll(chartsData)
    UI->>UI: Dashboard.updateKPIs & Table
    UI-->>User: Interactive Visual Dashboard Displayed
```
