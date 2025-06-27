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
-*Cleaned and standardized raw bird observation data using Pandas.

-*Converted time-related fields (Start_Time, End_Time) to datetime.time.

-Ensured data types for columns like Date, Temperature, Humidity, Sex, etc., were consistent.

-Handled missing values, (e.g., ID_Method, Distance, Sex).

### 2. PostgreSQL Table Creation & Data Insertion
  -Established a connection to PostgreSQL using psycopg2.
  -Created two main tables: grassland and forest, each with properly defined column types (TEXT, INTEGER, BOOLEAN, etc.).
  -Inserted the cleaned DataFrames into these tables using Pandas with SQLAlchemy and bulk insert queries.

### 3. SQL-Based Analysis
Wrote optimized SQL queries for insights like:
-Seasonal and yearly observation patterns
-Sex ratio, distance analysis, observer-wise trends
-Species affected by environmental variables like temperature, humidity, and wind
-Identification of conservation-priority species using PIF Watchlist and Stewardship flags

### 4. Streamlit Dashboard Development
-Built an interactive web dashboard using Streamlit.
-Sidebar navigation allows users to select specific analysis themes.
-Each section executes SQL queries dynamically, loads the data into Pandas, and visualizes results using Matplotlib and Seaborn.
-Used intuitive charts (barplots, line plots, heatmaps, horizontal bar charts) for maximum clarity.
