import folium
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_folium import st_folium

# Load dataset
df = pd.read_csv("Crime_Data_from_2020_to_Present.csv")

# Data Cleaning
st.title("Los Angeles Crime Data (2020-2023)")

# Display raw data preview
st.subheader("Raw Data Preview")
st.dataframe(df.head())

# Display shape and missing values information
st.write(f"Shape of DataFrame: {df.shape}")
st.write(f"Missing values per column in the DataFrame:")
st.write(df.isna().sum())

# Drop unnecessary columns
columns_to_drop = ['division_number', 'crime_code', 'area', 'crime_code_1', 'crime_code_2', 'crime_code_3', 'crime_code_4', 'status_description', 'status', 'weapon_code','premise_code', 'premise_description', 'victim_descent', 'modus_operandi', 'area','cross_street']
df = df.drop(columns=columns_to_drop, axis=1)

# Display cleaned data
st.write("Data after dropping unnecessary columns:")
st.write(df.head())

# Check missing values again
st.write(f"Missing values after dropping columns:")
st.write(df.isna().sum())

# Clean data: Remove rows with missing 'victim_sex'
df = df.dropna(subset=['victim_sex'])
df=df.dropna(subset=['weapon_description'])
st.write("Cleaned DataFrame after removing rows with missing 'victim_sex':")
st.write(df.head())

# Display missing values after cleaning
st.write(f"Missing values after cleaning:")
st.write(df.isna().sum())

# Preprocessing
df['date_occurred'] = pd.to_datetime(df['date_occurred'])
df['date_reported'] = pd.to_datetime(df['date_reported'])
df['month'] = df['date_occurred'].dt.month
df['year'] = df['date_occurred'].dt.year

# Sidebar filters
st.sidebar.title("Filters")

# Filter: Month
selected_months = st.sidebar.multiselect(
    "Select Month(s) to View Crime Trend:",
    options=list(range(1, 13)),
    default=list(range(1, 13))
)

# Filter: Area
areas = df['area_name'].unique()
selected_areas = st.sidebar.multiselect(
    "Select Area(s):",
    options=areas,
    default=areas
)

# Filter: Age Group
bins = [0, 18, 35, 50, 100]
labels = ['0-18', '19-35', '36-50', '51+']
df['age_group'] = pd.cut(df['victim_age'], bins=bins, labels=labels)
age_groups = df['age_group'].cat.categories
selected_age_groups = st.sidebar.multiselect(
    "Select Age Group(s):",
    options=age_groups,
    default=age_groups
)

# Filter: Weapon Type
top_weapons = df['weapon_description'].value_counts().head(10).index
selected_weapons = st.sidebar.multiselect(
    "Select Weapon(s):",
    options=top_weapons,
    default=top_weapons
)

# Apply Filters
filtered_df = df[
    (df['month'].isin(selected_months)) &
    (df['area_name'].isin(selected_areas)) &
    (df['age_group'].isin(selected_age_groups)) &
    (df['weapon_description'].isin(selected_weapons))
]

# Section: Crime Trend Over Time
st.header("Crime Trend Over Time")
monthly_crimes = filtered_df.groupby(['year', 'month']).size().reset_index(name='crime_count')
plt.figure(figsize=(12, 6))
plt.plot(monthly_crimes['month'], monthly_crimes['crime_count'], marker='o', color='b')
plt.title('Crime Trend Over Time', fontsize=20)
plt.xlabel('Month')
plt.ylabel('Number of Crimes')
plt.grid(True)
st.pyplot(plt)

# Section: Crime Distribution by Area
st.header("Crime Distribution by Area")
area_crimes = filtered_df['area_name'].value_counts().reset_index()
area_crimes.columns = ['Area Name', 'Crime Count']
norm = plt.Normalize(area_crimes['Crime Count'].min(), area_crimes['Crime Count'].max())
colors = plt.cm.viridis(norm(area_crimes['Crime Count']))
plt.figure(figsize=(10, 6))
plt.bar(area_crimes['Area Name'], area_crimes['Crime Count'], color=colors)
plt.xticks(rotation=90)
plt.title('Crime Distribution by Area', fontsize=16)
plt.xlabel('Area', fontsize=14)
plt.ylabel('Crime Count', fontsize=14)
st.pyplot(plt)

# Section: Age-Wise Crime Distribution
st.header("Age-Wise Crime Distribution")
age_crime_counts = filtered_df['age_group'].value_counts().reset_index()
age_crime_counts.columns = ['Age Group', 'Crime Count']
plt.figure(figsize=(8, 5))
plt.bar(age_crime_counts['Age Group'], age_crime_counts['Crime Count'], color='skyblue')
plt.title('Age-Wise Crime Distribution', fontsize=16)
plt.xlabel('Age Group', fontsize=14)
plt.ylabel('Number of Crimes', fontsize=14)
st.pyplot(plt)

# Section: Weapon-Wise Crime Distribution
st.header("Weapon-Wise Crime Distribution")
weapon_crimes = filtered_df['weapon_description'].value_counts().head(10)
plt.figure(figsize=(10, 6))
weapon_crimes.plot(kind='bar', color='crimson')
plt.title('Top 10 Weapon Types Used in Crimes', fontsize=16)
plt.xlabel('Weapon Type', fontsize=14)
plt.ylabel('Number of Crimes', fontsize=14)
plt.xticks(rotation=45)
st.pyplot(plt)

# Section: Correlation Matrix
st.header("Correlation Matrix")
numeric_df = filtered_df.select_dtypes(include=['float64', 'int64'])
numeric_df = numeric_df.dropna()
correlation = numeric_df.corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
st.pyplot(plt)

# Section: Crime Hotspots
st.header("Crime Hotspots")
if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
    crime_data = filtered_df[['latitude', 'longitude']]
    st.map(crime_data)
else:
    st.error("The dataset does not contain 'latitude' and 'longitude' columns.")

# Section: Crime Frequency Map
st.header("Crime Frequency Map")

# Define color based on crime frequency
def get_color(frequency):
    if frequency == 'high':
        return 'red'
    elif frequency == 'medium':
        return 'orange'
    else:
        return 'green'

# Calculate crime frequency
if filtered_df.empty or 'area_name' not in filtered_df.columns:
    st.error("Filtered DataFrame is empty or missing 'area_name' column.")
else:
    center_lat = filtered_df['latitude'].mean()
    center_lon = filtered_df['longitude'].mean()

    # Calculate crime counts and thresholds
    crime_counts = filtered_df['area_name'].value_counts()
    high_threshold = crime_counts.quantile(0.67)
    medium_threshold = crime_counts.quantile(0.33)

    # Define a safe function for crime frequency
    def get_crime_frequency(name):
        if name in crime_counts:
            if crime_counts[name] >= high_threshold:
                return 'high'
            elif crime_counts[name] >= medium_threshold:
                return 'medium'
            else:
                return 'low'
        else:
            return 'low'

    # Assign the crime_frequency column
    filtered_df = filtered_df.copy()
    filtered_df['crime_frequency'] = filtered_df['area_name'].apply(get_crime_frequency)

    # Debug outputs
    st.write("Crime Counts:", crime_counts)
    st.write("High Threshold:", high_threshold)
    st.write("Medium Threshold:", medium_threshold)
    st.write("Filtered DataFrame (With Crime Frequency):", filtered_df.head())


# Map crime frequencies
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
for name, group in filtered_df.groupby('area_name'):
    coords = group[['latitude', 'longitude']].mean().values.tolist()
    crime_frequency = group['crime_frequency'].iloc[0]
    folium.Circle(
        location=coords,
        radius=700,
        color=get_color(crime_frequency),
        fill=True,
        fill_color=get_color(crime_frequency),
        fill_opacity=0.6
    ).add_to(m)
st_folium(m, width=800, height=500)

# Add legend
st.markdown("""
    <div style="border: 2px solid grey; padding: 10px; background-color: white; display: inline-block;">
        <strong>Crime Frequency Legend</strong><br>
        <span style="color: red;">⬤</span> High Crimes<br>
        <span style="color: orange;">⬤</span> Medium Crimes<br>
        <span style="color: green;">⬤</span> Low Crimes
    </div>
""", unsafe_allow_html=True)
