# Project Notes – Global Power Plant Visualization Dashboard

## Executive Summary

The Global Power Plant Visualization Dashboard presents an integrated exploration of global power generation capacity, technology mix, and spatial distribution using the World Resources Institute’s Global Power Plant Database. The dashboard combines geospatial, temporal, and categorical analytics to examine global trends in renewable and non-renewable energy systems. Through interactive visualizations, it illustrates how global capacity evolved between 1950 and 2017, emphasizing the growing role of renewables and the regional diversity of energy strategies across countries.

---

## Tab 1 – Global Renewable vs Non-Renewable Capacity (2017)

### Overview
This tab visualizes the distribution of installed power generation capacity across renewable and non-renewable sources using four distinct plots:
- Bubble Scatter: Installed capacity vs. generation by fuel type.
- Deviation Plot: Deviation of plant capacities from the median within each fuel category.
- Pie + Bar Comparison: Proportional breakdown of global capacity.
- Boxplots: Distributions of plant capacities across fuels and energy categories.

### Key Takeaways
- The bubble scatter shows that Gas and Coal dominate global capacity and energy generation, representing the bulk of large-scale plants. Hydro is the only renewable source approaching similar capacity scales.
- The deviation plot highlights that Coal, Gas, and Nuclear have wide spreads around their median capacity, signifying a mixture of massive plants and numerous smaller facilities.
- Renewable fuels, in contrast, form tight, vertical clusters—especially Solar and Biomass, which are characterized by more uniform and smaller plant sizes.
- The pie and stacked bar charts confirm that nearly three-quarters of global 2017 capacity is non-renewable, led by Gas and Coal.
- The boxplots illustrate that non-renewable plants have much higher median capacities—often more than ten times larger than most renewables. Hydro and Nuclear exhibit long tails, while Solar and Biomass maintain compact distributions.

### Interpretation
Together, these visuals demonstrate the global asymmetry between large-scale centralized non-renewable systems and smaller distributed renewable plants. The filters in the dashboard allow users to explore how different fuel types or capacity thresholds reshape these relationships.

---

## Tab 2 – Capacity Trends and Commissioning Year Analysis (1950–2016)

### Overview
This tab focuses on how installed power generation capacity has evolved over time. It includes:
- Stacked Area Chart: Annual global installed capacity by fuel type.
- Scatter Plot: Plant-level capacity vs. year, separated by renewable category.

### Key Takeaways
- Global installed capacity remained relatively stable through the 1970s–1990s but accelerated sharply in the 2000s, driven primarily by Gas and Coal.
- Since the early 2010s, Wind and Solar have experienced exponential growth, signaling a worldwide shift toward cleaner technologies.
- The scatter plot highlights distinct temporal and technological clusters:
  - Non-renewables (Coal, Gas, Nuclear) appear as fewer but larger plants.
  - Renewables appear as many smaller plants with more consistent capacity ranges.
- Newer renewable plants increasingly dominate the most recent years, showing the pace of the energy transition.

### Interpretation
This tab captures the historical evolution of the global energy mix, revealing that the growth of renewables represents not only technological progress but also a diversification in plant scale and geography.

---

## Tab 3 – Global Power Plant Map (1950–2016)

### Overview
An animated global map visualizes the spatial and temporal distribution of power plants across countries, fuel types, and commissioning years. The map supports filtering by energy category and includes a year slider with play/pause controls for animation.

### Key Takeaways
- Early decades (1950–1980) show dense concentrations of fossil-fuel power plants in North America, Europe, and parts of Asia.
- Non-renewable plants tend to cluster in developed regions and near industrial centers.
- From the 1990s onward, there is visible global expansion of renewable energy, with new clusters in China, India, and South America.
- Solar and Wind projects emerge globally in the 21st century, emphasizing distributed, smaller-scale installations compared to the large, centralized fossil-fuel plants.

### Interpretation
This map vividly illustrates the global trajectory of energy infrastructure: from concentrated, fossil-heavy regions to a widespread renewable revolution. The cumulative visualization underscores the shift toward decentralized, low-carbon energy systems worldwide.

---

## Tab 4 – Regional Fuel Mix Comparison (Country-Level)

### Overview
This section enables users to explore individual countries’ energy compositions. It combines:
- Horizontal Bar Chart: Installed capacity by fuel type for the selected country.
- Histogram: Distribution of plant sizes (capacity) by fuel.
- Treemap: Hierarchical visualization of capacity by country, fuel, and renewable category.

### Key Takeaways
- Bar Chart: Each country exhibits a unique energy profile. Examples include:
  - United States – Gas dominates, followed by Wind, Hydro, and Coal.
  - Canada – Strongly Hydro-dominated with minor Wind and Gas.
  - Brazil – Balanced renewables with Hydro, Biomass, and Wind.
  - China – Coal-heavy but rapidly expanding Solar and Wind capacity.
- Histogram: Renewable fuels (Solar, Wind, Biomass) consist of many small-capacity plants, while non-renewables (Gas, Coal, Oil) have fewer but much larger facilities.
- Treemap: Summarizes how countries’ capacities divide between renewable and non-renewable sources.
  - Renewable treemaps (blue scale) emphasize Hydro and Wind dominance.
  - Non-renewable treemaps (red scale) show the persistence of Coal and Gas as major contributors.

### Interpretation
These visuals illustrate how energy strategy, geography, and policy influence each country’s fuel mix. The combination of size, diversity, and distribution provides a comparative view of global progress toward sustainable energy goals.

---

## Overall Conclusions

The Global Power Plant Visualization Dashboard synthesizes data across 34,000+ facilities to reveal:
- The global imbalance between non-renewable and renewable capacity.
- The temporal acceleration of renewable adoption post-2000.
- The spatial diffusion of clean energy technologies worldwide.
- The regional diversity of national energy portfolios.

By integrating interactive filtering and comparative analytics, this dashboard serves as a powerful exploratory tool for understanding the world’s energy transition and its underlying geographic, temporal, and technological patterns.

---

Data Source: [Global Power Plant Database – World Resources Institute (WRI)](https://datasets.wri.org/dataset/globalpowerplantdatabase)  
License: Creative Commons Attribution 4.0 International (CC BY 4.0)

