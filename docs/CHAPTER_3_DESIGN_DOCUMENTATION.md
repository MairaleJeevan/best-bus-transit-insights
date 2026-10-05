# Chapter 3: Methodology & Design Documentation

## Project: BEST Bus Transit Insights & Analytics System

---

## 3.1 Entity-Relationship (ER) Diagram

### Description
The Logical Entity-Relationship (ER) Diagram models the relational structure of the survey data repository and analytical dimensions. The schema organizes survey submissions across 5 distinct entities: **Commuters**, **Bus Routes**, **Bottleneck Locations**, **Payment Methods**, and **Survey Metrics**.

```mermaid
erDiagram
    COMMUTER_PROFILE ||--o{ SURVEY_RESPONSE : "submits"
    ROUTE ||--o{ SURVEY_RESPONSE : "is evaluated on"
    BOTTLENECK ||--o{ SURVEY_RESPONSE : "identifies"
    PAYMENT_METHOD ||--o{ SURVEY_RESPONSE : "uses"
    SURVEY_RESPONSE ||--|| SURVEY_METRIC : "contains"

    COMMUTER_PROFILE {
        string commuter_id PK "Unique identifier"
        string age_group "e.g., 18-25, 26-40, 41-60"
        string occupation "Student, Working Professional, Business"
        string frequent_user_status "Regular / Occasional"
        string travel_frequency "Daily, 3-4 times/week, Rare"
    }

    ROUTE {
        string route_number PK "e.g., 364, 383, 363, 501, 430, 663, 399, 367, A-21"
        string route_name "Corridor Description"
        string origin_terminus "e.g., Chembur Station"
        string destination_terminus "e.g., Kurla East / Nehru Nagar"
    }

    BOTTLENECK {
        string bottleneck_id PK "Unique Chokepoint ID"
        string location_name "SCLR, Chembur Stn, Diamond Garden"
        string corridor_segment "Nehru Nagar - Kurla Link"
        string severity_tier "High / Moderate / Low"
    }

    PAYMENT_METHOD {
        string payment_id PK "Unique Mode ID"
        string method_name "Chalo App, Smart Card, Cash, UPI"
        string category "Digital / Physical"
    }

    SURVEY_RESPONSE {
        string response_id PK "Unique Response UUID"
        datetime timestamp "Submission Time"
        string commuter_id FK "References COMMUTER_PROFILE"
        string route_number FK "References ROUTE"
        string bottleneck_location FK "References BOTTLENECK"
        string payment_method FK "References PAYMENT_METHOD"
    }

    SURVEY_METRIC {
        string metric_id PK "Unique Metric Record ID"
        string response_id FK "References SURVEY_RESPONSE"
        int bus_frequency_rating "Scale 1 to 5"
        int schedule_reliability "Punctuality Rating (1-5)"
        string overcrowding_level "Low, Moderate, High, Severe"
        int bus_condition_rating "Cleanliness & Comfort (1-5)"
        int avg_waiting_time_min "Estimated delay in minutes"
    }
```

---

## 3.2 Class Diagram

### Description
The Object-Oriented Class Diagram illustrates the backend architecture of the Python/Flask analytics microservice, showcasing data ingestion abstractions, data validation, filtering services, statistical aggregation, and REST API controllers.

```mermaid
classDiagram
    direction TB

    class AbstractDataLoader {
        <<abstract>>
        +load_data()* DataFrame
    }

    class CSVLoader {
        -string file_path
        +load_data() DataFrame
        -_validate_file_exists() bool
    }

    class GoogleSheetsLoader {
        -string sheet_id
        -string credentials_path
        +load_data() DataFrame
        -_authenticate() Object
    }

    class DataCleaner {
        -dict column_aliases
        -dict default_values
        +clean(DataFrame raw_df) Tuple[DataFrame, dict]
        -_normalize_route(string val) string
        -_normalize_boolean(string val) string
        -_normalize_age_group(string val) string
        -_normalize_occupation(string val) string
        -_normalize_payment(string val) string
        -_impute_missing_values(DataFrame df) DataFrame
    }

    class FilterService {
        +apply_filters(DataFrame df, dict filters) DataFrame
        -_filter_by_route(DataFrame df, string route) DataFrame
        -_filter_by_demographics(DataFrame df, dict demo_filters) DataFrame
    }

    class MetricsService {
        +get_summary_kpis(DataFrame df) dict
        +get_parameter_diagnostics(DataFrame df) list
        -_calculate_crowding_index(DataFrame df) float
        -_calculate_peak_delay_rate(DataFrame df) float
        -_calculate_digital_share(DataFrame df) float
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
        -datetime last_updated
        -DataCleaner cleaner
        +refresh(string source) dict
        +get_analytics(dict filters) dict
        +get_filter_options() dict
        +export_filtered_csv(dict filters) string
    }

    class FlaskAppController {
        +get_dashboard_analytics() JSON
        +refresh_dataset() JSON
        +export_csv() Response
        +health_check() JSON
    }

    AbstractDataLoader <|-- CSVLoader : implements
    AbstractDataLoader <|-- GoogleSheetsLoader : implements
    AnalyticsService *-- DataCleaner : contains
    AnalyticsService ..> AbstractDataLoader : uses
    AnalyticsService ..> FilterService : delegates filtering
    AnalyticsService ..> MetricsService : computes KPIs
    AnalyticsService ..> ChartDataService : transforms for UI
    FlaskAppController --> AnalyticsService : calls
```

---

## 3.3 Flow Chart (System Process Pipeline)

### Description
The Flow Chart outlines the sequential processing pipeline from commuter data acquisition to interactive visualization and reporting.

```mermaid
flowchart TD
    Start([Start System]) --> IngestionChoice{Data Ingestion Source}
    
    IngestionChoice -->|Cloud Live Stream| GForms[Google Forms Survey Collection]
    GForms --> GSheets[Google Sheets Cloud Database]
    GSheets --> GLoader[GoogleSheetsLoader via gspread API]
    
    IngestionChoice -->|Local/Offline| LocalCSV[Local Survey CSV File]
    LocalCSV --> CSVLoad[CSVLoader Ingestion]
    
    GLoader --> RawDF[(Raw Pandas DataFrame)]
    CSVLoad --> RawDF
    
    RawDF --> Cleaning[DataCleaner: Header Aliasing & Type Conversion]
    Cleaning --> Deduplicate[Deduplication & Missing Value Imputation]
    Deduplicate --> Norm[Value Normalization: Routes, Ratings, Demographics]
    Norm --> Cache[(In-Memory Validated Cache DataFrame)]
    
    Cache --> UserQuery[/User Loads Dashboard / Applies Filters/]
    UserQuery --> RouteHandler[Flask REST Controller: /api/analytics]
    RouteHandler --> FilterEngine[FilterService: Route, Age, Frequency Slicing]
    
    FilterEngine --> SlicedDF[(Filtered DataFrame Slice)]
    
    SlicedDF --> ParallelCalc1[MetricsService: Summary KPIs & Diagnostics]
    SlicedDF --> ParallelCalc2[ChartDataService: 8 Chart Transformations]
    
    ParallelCalc1 --> JSONBuilder[Assemble Unified JSON Analytics Payload]
    ParallelCalc2 --> JSONBuilder
    
    JSONBuilder --> APIResponse[HTTP 200 OK Response]
    APIResponse --> RenderUI[Frontend SPA: Render 8 Chart.js Visuals & KPI Cards]
    
    RenderUI --> InteractionCheck{User Action?}
    InteractionCheck -->|Change Filter| FilterEngine
    InteractionCheck -->|Export CSV| ExportEngine[Generate Filtered CSV Download]
    InteractionCheck -->|Refresh Data| IngestionChoice
    InteractionCheck -->|Idle / Inspect| EndNode([Dashboard Active])
```

---

## 3.4 Activity Diagram (UML Behavioral Flow)

### Description
The UML Activity Diagram details user interactions, system validations, parallel processing threads, and backend state transitions during dashboard operations.

```mermaid
stateDiagram-v2
    [*] --> InitializeDashboard : User opens Web Browser
    
    InitializeDashboard --> FetchInitialData : Dispatch GET /api/analytics
    
    state FetchInitialData {
        [*] --> CheckCache
        CheckCache --> ServeCache : Cache Valid & Warm
        CheckCache --> ReadDataSource : Cache Cold / Expired
        ReadDataSource --> CleanAndValidate : Load CSV or Sheets
        CleanAndValidate --> StoreCache : Update In-Memory Cache
        StoreCache --> ServeCache
        ServeCache --> [*]
    }
    
    FetchInitialData --> ApplyActiveFilters
    
    state ProcessAnalytics {
        [*] --> ParallelProcessing
        state ParallelProcessing {
            -->> ComputeKPIs : Calculate Delay, Crowding, Digital Share
            -->> ComputeCharts : Format 8 Datasets (Bar, Line, Radar, Donut)
            -->> ComputeDiagnostics : Evaluate Sentiment & Concern Tags
        }
        ParallelProcessing --> AggregateResponse
        AggregateResponse --> [*]
    }
    
    ApplyActiveFilters --> ProcessAnalytics
    ProcessAnalytics --> TransmitJSONPayload : HTTP 200 Response
    
    state UI_Rendering {
        [*] --> RenderCards : Update KPI Banner
        [*] --> RenderCharts : Update Chart.js Canvas
        [*] --> RenderMatrix : Populate Diagnostic Table
    }
    
    TransmitJSONPayload --> UI_Rendering
    
    UI_Rendering --> AwaitingUserInput : Dashboard Ready
    
    AwaitingUserInput --> SlicingData : User Adjusts Filter (Route / Age / Occupation)
    SlicingData --> ApplyActiveFilters
    
    AwaitingUserInput --> ManualRefresh : User clicks "Refresh Data"
    ManualRefresh --> ReadDataSource
    
    AwaitingUserInput --> DownloadCSV : User clicks "Export CSV"
    DownloadCSV --> GenerateFile : Stream CSV Buffer
    GenerateFile --> AwaitingUserInput
```

---

## 3.5 Sequence Diagram (System Interaction Timeline)

### Description
The UML Sequence Diagram captures the chronological message exchange between the commuter/analyst, Single Page Application frontend, Flask REST API layer, business logic services, and the data stores.

```mermaid
sequenceDiagram
    autonumber
    actor User as Commuter / Transport Analyst
    participant Browser as Browser Client (SPA)
    participant Flask as Flask REST API
    participant Service as AnalyticsService
    participant Loader as Data Loader (Sheets / CSV)
    participant Cleaner as DataCleaner
    participant Filter as FilterService
    participant Metrics as MetricsService & ChartDataService
    participant Charts as Chart.js UI Engine

    User->>Browser: Opens Dashboard URL / Selects Filter
    Browser->>Flask: GET /api/analytics?route=364&commuter=Regular
    activate Flask
    Flask->>Service: get_analytics(filters)
    activate Service

    alt In-Memory Cache Empty or Manual Refresh
        Service->>Loader: load_data()
        activate Loader
        Loader-->>Service: raw_data_frame
        deactivate Loader
        Service->>Cleaner: clean(raw_data_frame)
        activate Cleaner
        Cleaner-->>Service: (cleaned_df, validation_report)
        deactivate Cleaner
        Service->>Service: store in cached_df
    end

    Service->>Filter: apply_filters(cached_df, filters)
    activate Filter
    Filter-->>Service: filtered_df
    deactivate Filter

    par Compute Summary KPIs
        Service->>Metrics: get_summary_kpis(filtered_df)
        Metrics-->>Service: kpi_dict
    and Generate Visual Chart Data
        Service->>Metrics: generate_all_chart_data(filtered_df)
        Metrics-->>Service: charts_dict
    and Evaluate Diagnostic Indicators
        Service->>Metrics: get_parameter_diagnostics(filtered_df)
        Metrics-->>Service: diagnostics_list
    end

    Service-->>Flask: unified_analytics_payload
    deactivate Service
    Flask-->>Browser: 200 OK (JSON Payload)
    deactivate Flask

    Browser->>Charts: renderKPIs(summary)
    Browser->>Charts: updateCharts(charts_dict)
    Browser->>Browser: renderDiagnosticTable(diagnostics_list)
    Browser-->>User: Interactive Visual Dashboard Displayed
```
