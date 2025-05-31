# Statistical Analysis of CO2 Emissions and Socio-Economic Factors

## Overview

This project investigates the relationship between CO2 emissions (pollution index) and socio-economic factors,
specifically the **Local Purchasing Power Index (LPPI)** and **Time Index (TI)**, across 249 cities worldwide (primarily
in Europe, Asia, and North America) from 2012 to 2025.

The research was presented at the **61st Scientific Conference of Postgraduate Students, Master’s Students, and Students
of BSUIR**, Minsk, 2025.

## Authors

- **T.V. Kozlova** - Belarusian State University of Informatics and Radioelectronics (BSUIR), Minsk, Belarus
- **A.V. Zhvakina** - Associate Professor, Department of Computer Science, BSUIR

## Objectives

The primary goal is to analyze how CO2 emissions in cities correlate with:

- **Local Purchasing Power Index (LPPI)**: A measure of relative purchasing power based on average net salary,
  benchmarked against New York City (value of 100). A lower LPPI indicates reduced purchasing power compared to New
  York.
- **Time Index (TI)**: The average one-way commuting time in minutes, reflecting urban mobility and traffic conditions.

## Methodology

The analysis follows these steps:

1. **Data Collection**:
    - Data sourced from Numbeo datasets for cost of living, pollution, and
      traffic ([Numbeo Cost of Living](https://www.numbeo.com/cost-of-living/), [Numbeo Pollution](https://www.numbeo.com/pollution/), [Numbeo Traffic](https://www.numbeo.com/traffic/)).
    - Datasets cover 249 cities globally, with annual data from 2012 to 2025.
2. **Data Processing**:
    - For each year, the following calculations are performed:
        - **Median** of the comparer column (LPPI or TI) and the comparable column (Pollution Index).
        - Division of data into two groups based on the median of the comparer column (above and below median).
        - **Median** of the Pollution Index for each group.
        - **Correlation coefficient**
        - **T-test**
        - **Difference** and **percentage difference** between group medians relative to the overall median.
3. **Visualization**:
    - Scatter plots with regression lines to visualize relationships between LPPI/TI and Pollution Index for selected
      years (2015, 2025).
    - Line plots of correlation coefficients over years to show trends.

## Dependencies

- Python 3.8+
- pandas
- scipy
- matplotlib
- seaborn

## Usage

To run the analysis:

1. Clone the repository.
2. Ensure the data files (`cost_of_living_{year}.csv`, `pollution_{year}.csv`, `traffic_{year}.csv`) are in the `data`
   directory.
3. Run the main script:
   ```bash
   python main.py
   ```
4. Results will be saved as CSV files (`pollution_COL_dependence.csv`, `pollution_time_in_road_dependence.csv`) and
   plots (`plot_*.png`, `correlation_plot_*.png`).
