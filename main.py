import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Streamlit configuration
st.set_page_config(
    page_title="Solar Power Plant Performance Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Display project name as the headline with improved font size and style
st.markdown("<h1 style='text-align: center; font-size: 45px;'>Solar Power Plant Performance Dashboard</h1>", unsafe_allow_html=True)

# Add a detailed description about the Solar Power Plant Dashboard
st.markdown("""
    <p style='text-align: center; font-size: 18px; color: gray;'>This interactive dashboard visualizes the performance of solar power plants, helping to track key metrics 
    such as power generation, temperature, irradiation, and more. The dashboard includes several filters to explore specific data 
    points over selected time ranges, allowing plant operators and energy analysts to gain insights into the operational efficiency and 
    performance of solar power plants.</p>
""", unsafe_allow_html=True)

# Corrected file path for Windows
file_path = r"https://github.com/Khasimvali7729/solar-power/blob/main/Cleaned_File.csv"

try:
    # Read the dataset
    df = pd.read_csv(file_path, parse_dates=["DATE_TIME"], index_col="DATE_TIME")

    # Filters for the app (organized and more professional)
    st.sidebar.header("Filters")

    # Date range filter
    min_date = df.index.min()
    max_date = df.index.max()

    # Separate start and end date filters
    start_date = st.sidebar.date_input(
        "Select Start Date",
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )

    end_date = st.sidebar.date_input(
        "Select End Date",
        min_value=start_date,  # Ensures end date cannot be before start date
        max_value=max_date,
        value=max_date
    )

    # Apply date range filter
    df_filtered = df[(df.index >= pd.to_datetime(start_date)) & (df.index <= pd.to_datetime(end_date))]

    # Filters for Power Type, Temperature Type, and Irradiation Type
    st.sidebar.subheader("Select Data Types")

    # Power filter (DC and AC power)
    power_types = ["DC_POWER_Plant_1", "DC_POWER_Plant_2", "AC_POWER_Plant_1", "AC_POWER_Plant_2"]
    power_filter = st.sidebar.multiselect(
        "Select Power Types to Display",
        options=power_types,
        default=power_types
    )

    # Add "Select All" option for Power filter
    if "Select All" in power_filter:
        power_filter = power_types

    # Temperature filter (Ambient and Module temperature)
    temperature_types = ["Ambient_Temperature_Plant_1", "Module_Temperature_Plant_1", "Ambient_Temperature_Plant_2", "Module_Temperature_Plant_2"]
    temperature_filter = st.sidebar.multiselect(
        "Select Temperature Types to Display",
        options=temperature_types,
        default=temperature_types
    )

    # Add "Select All" option for Temperature filter
    if "Select All" in temperature_filter:
        temperature_filter = temperature_types

    # Irradiation filter
    irradiation_types = ["Irradiation_Plant_1", "Irradiation_Plant_2"]
    irradiation_filter = st.sidebar.multiselect(
        "Select Irradiation Types to Display",
        options=irradiation_types,
        default=irradiation_types
    )

    # Add "Select All" option for Irradiation filter
    if "Select All" in irradiation_filter:
        irradiation_filter = irradiation_types

    # Resample data by day with filters applied
    daily_df = df_filtered.resample("D").agg({
        "DC_POWER_Plant_1": "sum",
        "AC_POWER_Plant_1": "sum",
        "Daily_Yield_Plant_1": "sum",
        "Total_Yield_Plant_1": "sum",
        "Ambient_Temperature_Plant_1": "mean",
        "Module_Temperature_Plant_1": "mean",
        "Irradiation_Plant_1": "mean",
        "DC_POWER_Plant_2": "sum",
        "AC_POWER_Plant_2": "sum",
        "Daily_Yield_Plant_2": "sum",
        "Total_Yield_Plant_2": "sum",
        "Ambient_Temperature_Plant_2": "mean",
        "Module_Temperature_Plant_2": "mean",
        "Irradiation_Plant_2": "mean",
    })

    # Descriptive statistics
    st.header("Descriptive Statistics")
    st.write(daily_df.describe())

    # Top 10 Days with Highest Total Yield
    st.subheader("Top 10 Days with Highest Total Yield")
    top_10_days = daily_df[["Total_Yield_Plant_1", "Total_Yield_Plant_2"]].nlargest(10, "Total_Yield_Plant_1").reset_index()
    fig2 = px.bar(
        top_10_days,
        x="DATE_TIME",
        y=["Total_Yield_Plant_1", "Total_Yield_Plant_2"],
        barmode="group",
        labels={"value": "Total Yield (kWh)", "variable": "Plant"},
        title="Top 10 Days with Highest Total Yield",
        color_discrete_map={'Total_Yield_Plant_1': '#0072B2', 'Total_Yield_Plant_2': '#D55E00'}  # Professional blue and orange
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 7-Day Rolling Average of DC and AC Power for Plant 1
    st.subheader("7-Day Rolling Average of DC and AC Power for Plant 1")
    daily_df["DC_POWER_Plant_1_7d"] = daily_df["DC_POWER_Plant_1"].rolling(window=7).mean()
    daily_df["AC_POWER_Plant_1_7d"] = daily_df["AC_POWER_Plant_1"].rolling(window=7).mean()
    fig5 = px.line(
        daily_df.reset_index(),
        x="DATE_TIME",
        y=["DC_POWER_Plant_1_7d", "AC_POWER_Plant_1_7d"],
        labels={"value": "Power (kW)", "variable": "Power Type"},
        title="7-Day Rolling Average of DC and AC Power (Plant 1)",
        color_discrete_sequence=["#0072B2", "#D55E00"]  # Professional colors
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Distribution of Selected Power Generation
    st.subheader("Distribution of Selected Power Generation")
    fig1 = px.box(
        daily_df[power_filter].reset_index(),
        y=power_filter,
        points="all",  # Adds individual data points
        labels={"variable": "Power Type", "value": "Power (kW)"},
        title="Distribution of Selected Power Generation",
        color_discrete_sequence=["#0072B2", "#D55E00", "#E69F00", "#56B4E9"]  # Professional colors
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Cumulative Yield Comparison
    st.subheader("Cumulative Yield Comparison")
    fig6 = px.area(
        daily_df.reset_index(),
        x="DATE_TIME",
        y=["Total_Yield_Plant_1", "Total_Yield_Plant_2"],
        labels={"value": "Total Yield (kWh)", "variable": "Plant"},
        title="Cumulative Yield Comparison (Plant 1 vs Plant 2)",
        color_discrete_sequence=["#0072B2", "#D55E00"]  # Professional colors
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Correlation Heatmap for Key Variables
    st.subheader("Correlation Heatmap: Key Variables for Plant 1")
    correlation_df = daily_df[[ 
        "DC_POWER_Plant_1", "AC_POWER_Plant_1", "Daily_Yield_Plant_1",
        "Total_Yield_Plant_1", "Ambient_Temperature_Plant_1", "Module_Temperature_Plant_1", "Irradiation_Plant_1"
    ]]
    correlation_matrix = correlation_df.corr()

    fig4 = px.imshow(
        correlation_matrix,
        color_continuous_scale="RdBu_r",  # Reversed RdBu for better visualization
        labels={"x": "Variables", "y": "Variables", "color": "Correlation"},
        title="Correlation Heatmap: Key Variables for Plant 1"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # Temperature Distribution for Both Plants
    st.subheader("Temperature Distribution for Both Plants")
    fig7 = px.box(
        df_filtered[temperature_filter].reset_index(),
        y=temperature_filter,
        points="all",
        labels={"variable": "Temperature Type", "value": "Temperature (°C)"},
        title="Temperature Distribution for Both Plants",
        color_discrete_sequence=["#0072B2", "#D55E00", "#E69F00", "#56B4E9"]  # Professional colors
    )
    st.plotly_chart(fig7, use_container_width=True)

    # Hourly Solar Irradiation Patterns for Plant 1
    st.subheader("Hourly Solar Irradiation Patterns for Plant 1")
    hourly_df = df_filtered.resample("H").agg({
        "Irradiation_Plant_1": "mean",
        "Irradiation_Plant_2": "mean",
    })
    if not hourly_df.empty:
        hourly_pivot = hourly_df.pivot_table(index=hourly_df.index.hour, columns=hourly_df.index.date, values="Irradiation_Plant_1")
        fig3 = go.Figure(data=go.Heatmap(
            z=hourly_pivot.values,
            x=hourly_pivot.columns,  # Dates
            y=hourly_pivot.index,    # Hours
            colorscale="Viridis",     # Professional color scale
            colorbar_title="Irradiation (W/m²)"
        ))
        fig3.update_layout(
            title="Hourly Solar Irradiation Patterns for Plant 1",
            xaxis_title="Date",
            yaxis_title="Hour of Day"
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Hourly data not available for heatmap visualization.")

except FileNotFoundError:
    st.error(f"File not found at: {file_path}. Please verify the file path.")
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
 
