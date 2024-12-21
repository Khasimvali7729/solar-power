# Solar Power Plant Performance Dashboard  

## Introduction  
The **Solar Power Plant Performance Dashboard** is an interactive web application designed to monitor and visualize the performance of solar power plants. It helps track key metrics such as power generation (DC and AC), temperature (ambient and module), solar irradiation, and energy yield. This dashboard is a comprehensive tool for plant operators and energy analysts to analyze the efficiency and performance of solar power plants over selected time ranges.  

## Project Type  
Fullstack  

## Deployed App  
[Solar Power Dashboard](https://khasimvali7729-solar-power-main-4imb7x.streamlit.app/)  

## Project Presentation  
[YouTube Project Walkthrough](https://youtu.be/Zlan9NbITM4)  

## Directory Structure  
```
solar-power/
├─ backend/
├─ frontend/
│  ├─ ...
```  

## Features  
- Interactive dashboard with filters for **date ranges**, **power types**, **temperature types**, and **irradiation types**.  
- Descriptive statistics for key metrics, including **daily energy yield**, **temperature patterns**, and more.  
- Correlation heatmap to analyze relationships between power generation, temperature, and irradiation.  
- Visualizations for:  
  - Distribution of power generation.  
  - Hourly solar irradiation patterns.  
  - Temperature distribution for both plants.  
  - Cumulative yield comparison between two plants.  
  - Top 10 days with the highest total energy yield.  
- 7-day rolling averages for DC and AC power trends.  

## Design Decisions or Assumptions  
- Data is processed and resampled daily to create clear and concise visualizations.  
- CSV file is used as the primary data source.  
- Streamlit is chosen for its simplicity in creating interactive dashboards.  
- Filters are implemented to allow users to explore specific metrics over custom date ranges.  

## Installation & Getting Started  

To run the project locally, follow these steps:  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-repo/solar-power-dashboard.git  
   cd solar-power-dashboard  
   ```  

2. Install required Python libraries:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Run the Streamlit application:  
   ```bash  
   streamlit run main.py  
   ```  

4. Place your CSV file in the correct path (update the `file_path` variable in the code if necessary).  

## Usage  

- Open the deployed app in a browser: [Solar Power Dashboard](https://khasimvali7729-solar-power-main-4imb7x.streamlit.app/).  
- Use the sidebar to filter data by:  
  - Date ranges.  
  - Power types (DC, AC).  
  - Temperature types (Ambient, Module).  
  - Irradiation types.  
- View the interactive visualizations and descriptive statistics for performance insights.  

## APIs Used  
- Not applicable; data is sourced from a CSV file.  

## API Endpoints  
- Not applicable; backend APIs are not used in this project.  

## Technology Stack  
- **Python**: Data processing and backend logic.  
- **Pandas**: For data cleaning, filtering, and aggregation.  
- **Streamlit**: To build the interactive dashboard.  
- **Plotly**: For creating professional visualizations.  

## Credentials  
- No authentication is required for this application.  
