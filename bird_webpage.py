import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
from sqlalchemy import create_engine

# PostgreSQL connection settings
host = "localhost"
port = "5432"
database = "Bird_Species"
username = "postgres"
password = "password"

# Create the engine
engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Title
st.title("Bird's Observation Dashboard")

# Sidebar options
section = st.sidebar.selectbox("Choose an Insight", [
    "Seasonal Trends",
    "Observation Time",
    "Location Insights",
    "Plot-Level Analysis",
    "Diversity Metrics",
    'Activity Patterns',
    "Sex Ratio",
    "Weather Correlation",
    "Disturbance Effect",
    "Distance Analysis",
    "Observer Bias",
    "Visit Patterns",
    "Watchlist Trends",
    'AOU Code Patterns'

])


if section == "Seasonal Trends":
    # Query for grassland sightings
    grassland_query = """
    SELECT 
        'Grassland' AS habitat,
        CASE 
            WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM date) IN (9, 10, 11) THEN 'Autumn'
        END AS season,
        year,
        COUNT(*) AS sightings
    FROM grassland
    GROUP BY habitat, season, year
    ORDER BY year, season;
    """

    # Query for forest sightings
    forest_query = """
    SELECT 
        'Forest' AS habitat,
        CASE 
            WHEN EXTRACT(MONTH FROM date) IN (12, 1, 2) THEN 'Winter'
            WHEN EXTRACT(MONTH FROM date) IN (3, 4, 5) THEN 'Spring'
            WHEN EXTRACT(MONTH FROM date) IN (6, 7, 8) THEN 'Summer'
            WHEN EXTRACT(MONTH FROM date) IN (9, 10, 11) THEN 'Autumn'
        END AS season,
        year,
        COUNT(*) AS sightings
    FROM forest
    GROUP BY habitat, season, year
    ORDER BY year, season;
    """

    # Fetch both results into DataFrames
    grassland_df = pd.read_sql_query(grassland_query, engine)
    forest_df = pd.read_sql_query(forest_query, engine)

    # Combine into a single DataFrame
    combined_df = pd.concat([grassland_df, forest_df])

    # Create a new column that combines year and season for x-axis
    combined_df['year_season'] = combined_df['year'].astype(str) + ' ' + combined_df['season']

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=combined_df, x="year_season", y="sightings", hue="habitat", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Seasonal Bird Sightings by Habitat")
    st.pyplot(fig)

elif section == "Observation Time":
    query = """
    SELECT 
        CASE 
            WHEN start_time BETWEEN '04:00' AND '06:59' THEN 'Early Morning'
            WHEN start_time BETWEEN '07:00' AND '09:59' THEN 'Morning'
            WHEN start_time BETWEEN '10:00' AND '12:59' THEN 'Late Morning'
            WHEN start_time BETWEEN '13:00' AND '15:59' THEN 'Afternoon'
            WHEN start_time BETWEEN '16:00' AND '18:59' THEN 'Evening'
            ELSE 'Night'
        END AS time_window,
        COUNT(*) AS bird_sightings
    FROM grassland
    GROUP BY time_window
    ORDER BY bird_sightings DESC;
    """

    # Read into DataFrame
    time_df = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(10, 6))
    sns.barplot(x='time_window', y='bird_sightings', palette='viridis', data=time_df, hue='time_window', legend=True)
    plt.title("Bird Sightings by Time Window")
    plt.xlabel("Time of Day")
    plt.ylabel("Number of Sightings")
    st.pyplot(fig)

elif section == "Location Insights":
    query = """
    SELECT 
        location_type,
        COUNT(DISTINCT scientific_name) AS unique_species_count
    FROM (
        SELECT location_type, scientific_name FROM grassland
        UNION ALL
        SELECT location_type, scientific_name FROM forest
    )
    GROUP BY location_type
    ORDER BY unique_species_count DESC;
    """

    biodiversity_df = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(8, 5))
    sns.barplot(x='location_type', y='unique_species_count', data=biodiversity_df, palette='viridis',
                hue='location_type', legend=True)
    plt.title('Unique Bird Species Count in Forest & Grassland')
    plt.xlabel('Location Type')
    plt.ylabel('Unique Species Count')
    st.pyplot(fig)

elif section == "Plot-Level Analysis":
    habitat_choice = st.radio("Choose Habitat", ["Grassland", "Forest"])

    def disaply(plot_df, choice):
        top_n = plot_df.head(10)
        fig = plt.figure(figsize=(10, 6))
        sns.barplot(y='plot_name', x='unique_species_count', data=top_n, palette='mako', hue='plot_name', legend=True)
        plt.title(f'Top 10 Plots by Unique Bird Species in {choice}')
        plt.xlabel('Unique Species Count')
        plt.ylabel('Plot Name')
        st.pyplot(fig)

    if habitat_choice == "Grassland":
        query = """
        SELECT 
            plot_name,
            COUNT(DISTINCT scientific_name) AS unique_species_count
        FROM grassland
        GROUP BY plot_name
        ORDER BY unique_species_count DESC;
        """

        plot_df = pd.read_sql_query(query, engine)
        disaply(plot_df, habitat_choice)


    elif habitat_choice == "Forest":
        query = """
        SELECT 
            plot_name,
            COUNT(DISTINCT scientific_name) AS unique_species_count
        FROM forest
        GROUP BY plot_name
        ORDER BY unique_species_count DESC;
        """

        plot_df = pd.read_sql_query(query, engine)
        disaply(plot_df, habitat_choice)

elif section == "Diversity Metrics":
    query = """
    SELECT 
        location_type,
        COUNT(DISTINCT scientific_name) AS unique_species_count
    FROM (
        SELECT location_type, scientific_name FROM grassland
        UNION ALL
        SELECT location_type, scientific_name FROM forest
    ) AS all_data
    GROUP BY location_type
    ORDER BY unique_species_count DESC;
    """

    diversity_df = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(8, 5))
    sns.barplot(y='location_type', x='unique_species_count', data=diversity_df, hue='location_type', legend=True)
    plt.title('Unique Bird Species by Location Type')
    plt.xlabel('Location Type')
    plt.ylabel('Unique Species Count')
    st.pyplot(fig)

elif section == 'Activity Patterns':
    query = """
    SELECT 
        id_method,
        interval_length,
        COUNT(*) AS observations
    FROM (
        SELECT id_method, interval_length FROM grassland
        UNION ALL
        SELECT id_method, interval_length FROM forest
    ) AS all_data
    GROUP BY id_method, interval_length
    ORDER BY observations DESC;
    """

    activity_df = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(12, 6))
    sns.barplot(
        x='interval_length',
        y='observations',
        hue='id_method',
        data=activity_df,
        palette='Set2'
    )
    plt.title('Bird Observation Methods by Interval Length')
    plt.xlabel('Interval Length')
    plt.ylabel('Number of Observations')
    plt.xticks(rotation=45)
    plt.legend(title='ID Method')
    st.pyplot(fig)

elif section == "Disturbance Effect":
    query = """
    SELECT
        Disturbance,
        COUNT(*) AS total_sightings,
        COUNT(DISTINCT Scientific_Name) AS unique_species
    FROM
        grassland
    GROUP BY
        Disturbance
    ORDER BY
        total_sightings DESC;
    """

    disturbance_effect = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=disturbance_effect, y="total_sightings", x="disturbance", palette="coolwarm", hue='disturbance',
                legend=True)
    plt.title("Impact of Disturbance on Bird Sightings")
    plt.xlabel("Total Bird Sightings")
    plt.xticks(rotation=45)
    plt.ylabel("Disturbance Type")
    st.pyplot(fig)

elif section == "Distance Analysis":
    query_grassland = """
    SELECT
        Distance,
        Scientific_Name,
        COUNT(*) AS Sightings,
        'Grassland' AS Habitat
    FROM grassland
    GROUP BY Distance, Scientific_Name
    """

    # Step 3: Query forest table
    query_forest = """
    SELECT
        Distance,
        Scientific_Name,
        COUNT(*) AS Sightings,
        'Forest' AS Habitat
    FROM forest
    GROUP BY Distance, Scientific_Name
    """

    # Step 4: Read both into DataFrames
    df_grassland = pd.read_sql_query(query_grassland, engine)
    df_forest = pd.read_sql_query(query_forest, engine)

    # Step 5: Combine both
    combined_df = pd.concat([df_grassland, df_forest], ignore_index=True)


    def categorize_distance(d):
        if d in ['<= 50 Meters', '50 - 100 Meters']:
            return 'Observed Closer'
        elif d == 'Flyover':
            return 'Observed Farther'
        else:
            return 'other'


    combined_df["distance_category"] = combined_df["distance"].apply(categorize_distance)

    # Step 6: Get top 5 species per Distance per Habitat
    top_species = (
        combined_df.groupby(["habitat", "distance_category"], group_keys=False)
        .apply(lambda x: x.sort_values("sightings", ascending=False).head(5))
    )
    # For example, filter only one habitat
    habitat_choice = st.radio("Choose Habitat", ["Grassland", "Forest"])

    filtered_df = top_species[top_species["habitat"] == habitat_choice]

    fig = plt.figure(figsize=(12, 6))
    sns.barplot(
        data=filtered_df,
        x="sightings",
        y="scientific_name",
        hue="distance_category",
        dodge=True
    )
    plt.title(f"Top 5 Bird Species by Distance Category - {habitat_choice}")
    plt.xlabel("Number of Sightings")
    plt.ylabel("Scientific Name")
    plt.legend(title="Distance Category", bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig)

elif section == "Observer Bias":
    from sqlalchemy import create_engine, text

    query = """
    SELECT
        observer,
        COUNT(*) AS total_sightings,
        COUNT(DISTINCT scientific_name) AS unique_species
    FROM (
        SELECT observer, scientific_name FROM grassland
        UNION ALL
        SELECT observer, scientific_name FROM forest
    ) AS combined
    GROUP BY observer
    ORDER BY total_sightings DESC;
    """

    df = pd.read_sql_query(query, engine)

    observers = df['observer']
    x = np.arange(len(observers))  # X locations
    width = 0.35  # Width of bars

    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - width / 2, df['total_sightings'], width, label='Total Sightings', color='skyblue')
    bar2 = ax.bar(x + width / 2, df['unique_species'], width, label='Unique Species', color='salmon')

    # Labels and formatting
    ax.set_xlabel('Observer')
    ax.set_ylabel('Count')
    ax.set_title('Total Sightings vs Unique Species by Observer')
    ax.set_xticks(x)
    ax.set_xticklabels(observers, rotation=0)
    ax.legend()
    ax.bar_label(bar1, padding=3)
    ax.bar_label(bar2, padding=3)
    st.pyplot(fig)

elif section == "Visit Patterns":
    query = """
    SELECT
        Visit,
        COUNT(*) AS total_observations,
        COUNT(DISTINCT Scientific_Name) AS unique_species_count
    FROM (
        SELECT Visit, Scientific_Name FROM grassland
        UNION ALL
        SELECT Visit, Scientific_Name FROM forest
    ) AS combined
    GROUP BY Visit
    ORDER BY Visit;
    """

    df = pd.read_sql_query(query, engine)

    fig = plt.figure(figsize=(10, 6))
    plt.plot(df['visit'], df['total_observations'], marker='o', label='Total Observations')
    plt.plot(df['visit'], df['unique_species_count'], marker='s', label='Unique Species Count')
    plt.xlabel('Visit Number')
    plt.ylabel('Count')
    plt.title('Visit Patterns: Observations and Species Diversity by Visit')
    plt.legend()
    plt.grid(True)
    st.pyplot(fig)

elif section == 'Sex Ratio':
    query = """
    SELECT 
        Sex,
        COUNT(*) AS count
    FROM (
        SELECT Sex FROM grassland
        UNION ALL
        SELECT Sex FROM forest
    ) AS combined
    GROUP BY Sex;
    """

    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(7, 5))
    sns.barplot(data=df, x='sex', y='count', palette='pastel', hue='sex', legend=True)
    plt.title("Sex Ratio of Bird Observations")
    plt.xlabel("Sex")
    plt.ylabel("Count")
    plt.tight_layout()
    st.pyplot(plt.gcf())


elif section == "Weather Correlation":
    query = """
    SELECT 
        Sky,
        ROUND(Temperature)::int AS temperature_bucket,
        COUNT(*) AS sightings
    FROM (
        SELECT Sky, Temperature FROM grassland
        UNION ALL
        SELECT Sky, Temperature FROM forest
    ) AS combined
    WHERE Temperature IS NOT NULL
    GROUP BY Sky, temperature_bucket
    ORDER BY Sky, temperature_bucket;
    """

    df = pd.read_sql_query(query, engine)
    pivot = df.pivot(index='sky', columns='temperature_bucket', values='sightings').fillna(0)

    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot, cmap='YlGnBu', annot=True, fmt=".0f")
    plt.title("Bird Sightings by Temperature & Sky Condition")
    plt.xlabel("Temperature Bucket (°C)")
    plt.ylabel("Sky Condition")
    st.pyplot(plt.gcf())

elif section == 'Watchlist Trends':
    query = """
    SELECT 
        scientific_name,
        COUNT(*) AS sightings,
        SUM(CASE WHEN PIF_Watchlist_Status THEN 1 ELSE 0 END) AS watchlist,
        SUM(CASE WHEN Regional_Stewardship_Status THEN 1 ELSE 0 END) AS stewardship
    FROM (
        SELECT Scientific_Name, PIF_Watchlist_Status, Regional_Stewardship_Status FROM grassland
        UNION ALL
        SELECT Scientific_Name, PIF_Watchlist_Status, Regional_Stewardship_Status FROM forest
    ) AS combined
    GROUP BY Scientific_Name
    HAVING 
        SUM(CASE WHEN PIF_Watchlist_Status THEN 1 ELSE 0 END) > 0
        OR SUM(CASE WHEN Regional_Stewardship_Status THEN 1 ELSE 0 END) > 0
    ORDER BY sightings DESC
    LIMIT 10;

    """

    df = pd.read_sql_query(query, engine)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, y='scientific_name', x='sightings', orient='h', palette='rocket', hue='scientific_name',
                legend=True)
    plt.title("Top At-Risk Bird Species (Conservation Focus)")
    plt.xlabel("Sightings")
    plt.ylabel("Scientific Name")
    plt.tight_layout()
    st.pyplot(plt.gcf())

elif section == 'AOU Code Patterns':
    query = """
    SELECT 
        AOU_Code,
        COUNT(*) AS total_sightings,
        COUNT(DISTINCT Scientific_Name) AS unique_species,
        SUM(CASE WHEN PIF_Watchlist_Status THEN 1 ELSE 0 END) AS watchlist_count,
        SUM(CASE WHEN Regional_Stewardship_Status THEN 1 ELSE 0 END) AS stewardship_count
    FROM (
        SELECT AOU_Code, Scientific_Name, PIF_Watchlist_Status, Regional_Stewardship_Status FROM grassland
        UNION ALL
        SELECT AOU_Code, Scientific_Name, PIF_Watchlist_Status, Regional_Stewardship_Status FROM forest
    ) AS combined
    GROUP BY AOU_Code
    ORDER BY total_sightings DESC
    """

    df = pd.read_sql_query(query, engine)

    top_n = st.slider("Select number of top rows to display", min_value=5, max_value=20, value=10, step=1)

    # Display the top N rows from the DataFrame
    top = df.head(top_n)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top, y='aou_code', x='total_sightings', orient='h', palette='magma', hue='aou_code', legend=True)
    plt.title("Top AOU Codes by Sightings")
    plt.xlabel("Total Sightings")
    plt.ylabel("AOU Code")
    plt.tight_layout()
    st.pyplot(plt.gcf())
