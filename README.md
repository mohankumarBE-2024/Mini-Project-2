# Mini-Project-2
Bird Species Observation Analysis
# Overview
This project focuses on analyzing bird observation data collected from two different habitats: Grassland and Forest. The data is stored in a PostgreSQL database, and insights are extracted using SQL queries and visualized using Streamlit, Pandas, Matplotlib, and Seaborn.

The goal is to uncover trends in species diversity, observation patterns, environmental correlations, and conservation priorities through interactive visual dashboards.

## Technologies Used

- **PostgreSQL**: Stores bird observation data in structured tables.

- **psycopg2**: For PostgreSQL database connection and query execution.

- **SQLAlchemy**: For creating database engines and integrating with Pandas.

- **Pandas**: For handling SQL results and preparing data for visualization.

- **Matplotlib & Seaborn**: For building clear and insightful data visualizations.

- **Streamlit**: For building an interactive web-based dashboard.

## Steps Involved

### 1. Data Preprocessing
- Cleaned and standardized raw bird observation data using Pandas.
- Converted time-related fields (`Start_Time`, `End_Time`) to `datetime.time`.
- Ensured data types for columns like `Date`, `Temperature`, `Humidity`, `Sex`, etc., were consistent.
- Handled missing values:
  - `ID_Method`
  - `Distance`
  - `Sex`

### 2. PostgreSQL Table Creation & Data Insertion
- Established a connection to PostgreSQL using `psycopg2`.
- Created two main tables: `grassland` and `forest`, each with well-defined column types (`TEXT`, `INTEGER`, `BOOLEAN`, etc.).
- Inserted the cleaned DataFrames into the database using `pandas.to_sql()` or `executemany()` with SQLAlchemy engine.

### 3. SQL-Based Analysis
- Wrote optimized SQL queries for:
  - Seasonal and yearly observation trends
  - Sex ratio and species diversity across locations
  - Observer behavior and visit patterns
  - Environmental factors (Temperature, Humidity, Sky, Wind) affecting bird activity
  - Species with conservation priority using `PIF_Watchlist_Status` and `Regional_Stewardship_Status`

### 4. Streamlit Dashboard Development
- Built an interactive web dashboard using Streamlit.
- Added sidebar navigation for selecting different analytical views.
- Each selection:
  - Runs SQL queries using SQLAlchemy
  - Loads data into Pandas
  - Generates visualizations using Seaborn/Matplotlib
- Visual formats used:
  - Bar charts (vertical & horizontal)
  - Line plots
  - Count plots
  - Heatmaps for weather correlations
