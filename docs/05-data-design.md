# Chapter 5: Data Design & Integrity

## 5.1 Analytical Data Schema

| Field Name | Canonical Type | Nullable | Allowed / Normalization Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `Response_ID` | String | No | Unique (e.g. `RESP001`, `GEN_0001`) | Primary survey response key |
| `Timestamp` | DateTime | Yes | ISO Format (`YYYY-MM-DD HH:MM:SS`) | Timestamp of survey submission |
| `Age_Group` | String | No | `18-25`, `26-35`, `36-50`, `50+` | Commuter age category |
| `Occupation` | String | No | `Student`, `Employed`, `Government`, `Business/Self-Employed`, `Retired`, `Other` | Commuter occupational group |
| `Frequent_User_Status` | String (Bool) | No | `Yes`, `No` | Regular commuter indicator |
| `Primary_Route_Number` | String | No | `363`, `364`, `367`, `383`, `399`, `430`, `501`, `663`, `A-21`, `Other` | Primary BEST route used |
| `Travel_Frequency` | String | No | `Daily`, `5-6 days/week`, `3-4 days/week`, `Occasionally` | Commute frequency |
| `Peak_Hour_Frequency_Rating` | Integer | No | `1` to `5` | Frequency adequacy rating |
| `Schedule_Arrival_Reliability` | Integer | No | `1` to `5` | Punctuality rating |
| `Bottleneck_Delay_Exposure` | String (Bool) | No | `Yes`, `No` | Traffic delay experience |
| `Primary_Bottleneck_Location`| String | No | `SCLR`, `Chembur Station`, `Diamond Garden`, `Nehru Nagar`, `Kurla Signal`, `None` | Congestion node |
| `Overcrowding_Level` | String | No | `Severe`, `High`, `Moderate`, `Low` | Passenger density perception |
| `Bus_Condition_Rating` | Integer | No | `1` to `5` | Overall fleet quality rating |
| `Cleanliness_Rating` | Integer | No | `1` to `5` | Cabin cleanliness score |
| `Seating_Comfort_Rating` | Integer | No | `1` to `5` | Seating ergonomics score |
| `Ventilation_Rating` | Integer | No | `1` to `5` | Airflow / AC comfort score |
| `Preferred_Payment_Method` | String | No | `Chalo App`, `Smart Card`, `Cash`, `UPI/QR`, `Other` | Ticketing method |
| `Avg_Waiting_Time_Min` | Integer | No | `1` to `120` (Minutes) | Estimated waiting time at bus stop |

## 5.2 Data Integrity and Constraints
1. **Primary Key Uniqueness**: `Response_ID` values are strictly deduplicated during the cleaning step.
2. **Type Safety & Bounds**: Numerical ratings are clipped to range `[1, 5]`; waiting time is bounded between `[1, 120]` minutes.
3. **Missing Value Imputation**: Null text fields are imputed with modal category; null ratings default to median `3`.
4. **Security & Upload Validation**: CSV file uploads are checked for valid `.csv` extension, file size `< 16MB`, and UTF-8 encoding. Executable content is rejected.

## 5.3 Google Sheets API Setup Guide
To connect a live Google Sheet:
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com).
2. Create a project named `BEST-Bus-Analytics`.
3. Enable the **Google Sheets API** and **Google Drive API**.
4. Create a **Service Account** under *IAM & Admin* > *Service Accounts*.
5. Create and download a new JSON key, saving it in the project root as `service_account.json`.
6. Open your Google Sheet containing the survey responses, click **Share**, and paste the Service Account client email address with **Viewer** role.
7. Set the environment variables in `.env`:
   ```bash
   DATA_SOURCE=google_sheets
   GOOGLE_SHEET_ID=1_YourGoogleSheetIdHere_XYZ
   GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
   ```
