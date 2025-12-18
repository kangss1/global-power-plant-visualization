import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================
# TAB 1 — GLOBAL CAPACITY PLOTS
# ==============================

def fig_tab1_scatter(df, data_note):
    df_summary = (
        df.groupby(['primary_fuel', 'energy_category'], as_index=False)
          .agg({'capacity_mw': 'sum', 'estimated_generation_gwh_2017': 'sum'})
          .sort_values('capacity_mw', ascending=False)
    )
    fuel_order = df_summary['primary_fuel'].tolist()
    fig = px.scatter(
        df_summary,
        x='capacity_mw',
        y='estimated_generation_gwh_2017',
        size='capacity_mw',
        color='primary_fuel',
        symbol='energy_category',
        hover_data={
            'primary_fuel': True,
            'energy_category': True,
            'capacity_mw': ':.0f',
            'estimated_generation_gwh_2017': ':.0f'
        },
        category_orders={'primary_fuel': fuel_order},
        size_max=55,
        title='Global Renewable vs Non-Renewable Capacity (2017)',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig.update_layout(
        template='simple_white',
        xaxis_title='Installed Capacity (MW)',
        yaxis_title='Estimated Generation (GWh, 2017)',
        legend_title_text='Fuel Type',
        height=600,
        hoverlabel=dict(bgcolor="white", font_size=12),
        annotations=[dict(
            text=data_note, x=0.5, y=-0.15,
            xref='paper', yref='paper', showarrow=False,
            font=dict(size=11, color='gray')
        )]
    )
    return fig


def fig_tab1_deviation(df_filtered):
    df_dev = df_filtered.copy()
    df_dev['fuel_median'] = df_dev.groupby('primary_fuel')['capacity_mw'].transform('median')
    df_dev['diff_from_median'] = df_dev['capacity_mw'] - df_dev['fuel_median']
    deviation_min, deviation_max = -500, 500
    df_dev_filtered = df_dev[
        (df_dev['diff_from_median'] >= deviation_min) &
        (df_dev['diff_from_median'] <= deviation_max)
    ]
    df_dev_filtered['fuel_index'] = df_dev_filtered['primary_fuel'].astype('category').cat.codes
    fuel_labels = dict(
        enumerate(df_dev_filtered['primary_fuel'].astype('category').cat.categories)
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_dev_filtered['fuel_index'],
        y=df_dev_filtered['capacity_mw'],
        mode='markers',
        marker=dict(
            size=7, opacity=0.6,
            color=df_dev_filtered['diff_from_median'],
            colorscale='Cividis',
            cmin=deviation_min, cmax=deviation_max,
            colorbar=dict(title='Deviation (MW)')
        ),
        text=df_dev_filtered['primary_fuel'],
        hovertemplate='<b>%{text}</b><br>Capacity: %{y:.0f} MW<br>Deviation: %{marker.color:.0f} MW<extra></extra>'
    ))
    fig.update_layout(
        title='Capacity Deviation from Median by Fuel Type (Filtered)',
        template='simple_white',
        height=600,
        width=1000,
        xaxis=dict(
            title='Fuel Type',
            tickmode='array',
            tickvals=list(fuel_labels.keys()),
            ticktext=list(fuel_labels.values()),
            tickangle=30
        ),
        yaxis=dict(title='Capacity (MW)')
    )
    return fig


def fig_tab1_piebar(df, data_note):
    capacity_by_category = df.groupby('energy_category', as_index=False)['capacity_mw'].sum()
    fuel_split = (
        df.groupby(['primary_fuel', 'energy_category'], as_index=False)['capacity_mw']
          .sum().pivot(index='primary_fuel', columns='energy_category', values='capacity_mw')
          .fillna(0).reset_index()
    )
    fuel_split['Total'] = fuel_split[['Renewable', 'Non-Renewable']].sum(axis=1)
    fuel_split = fuel_split.sort_values('Total', ascending=False)
    colors = {'Renewable': 'steelblue', 'Non-Renewable': 'indianred'}
    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "xy"}]],
        column_widths=[0.35, 0.65],
        subplot_titles=[
            "Share of Renewable vs Non-Renewable Capacity (2017)",
            "Installed Capacity by Fuel Type (2017)"
        ],
        horizontal_spacing=0.08
    )
    fig.add_trace(
        go.Pie(
            labels=capacity_by_category['energy_category'],
            values=capacity_by_category['capacity_mw'],
            textinfo='percent+label',
            marker=dict(colors=[colors[c] for c in capacity_by_category['energy_category']]),
            hovertemplate="%{label}<br>%{percent}<extra></extra>",
            showlegend=False
        ),
        row=1, col=1
    )
    for category in ['Renewable', 'Non-Renewable']:
        if category in fuel_split.columns:
            y_vals = fuel_split[category].fillna(0)
            fig.add_trace(
                go.Bar(
                    name=category,
                    x=fuel_split['primary_fuel'],
                    y=y_vals,
                    marker_color=colors[category],
                    showlegend=True
                ),
                row=1, col=2
            )
    fig.update_layout(
        template='simple_white',
        title='Renewable vs Non-Renewable Capacity Comparison (2017)',
        barmode='stack',
        height=640,
        width=1250,
        font=dict(size=13),
        margin=dict(t=130, b=240, l=70, r=160),
        hoverlabel=dict(bgcolor='white')
    )
    fig.add_annotation(
        text=data_note, x=0.5, y=-0.47,
        xref='paper', yref='paper',
        showarrow=False,
        font=dict(size=11, color='gray')
    )
    return fig


def fig_tab1_box(df_filtered, data_note):
    df_source = df_filtered.copy()
    df_source['cap_log10'] = np.log10(df_source['capacity_mw'] + 1)
    colors = {'Renewable': 'steelblue', 'Non-Renewable': 'indianred'}
    fuel_order = (
        df_filtered.groupby('primary_fuel', as_index=False)['capacity_mw']
          .median().sort_values('capacity_mw', ascending=True)['primary_fuel'].tolist()
    )
    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.25, 0.75],
        subplot_titles=[
            "Renewables vs Non-Renewables (Log Scale)",
            "Capacity by Fuel Type (Log Scale)"
        ],
        horizontal_spacing=0.09
    )
    for cat in ["Renewable", "Non-Renewable"]:
        subset = df_source.loc[df_source['energy_category'] == cat, 'cap_log10'].dropna()
        if not subset.empty:
            fig.add_trace(go.Box(
                y=subset, name=cat,
                marker_color=colors[cat], opacity=0.55,
                boxpoints='outliers', showlegend=True
            ), row=1, col=1)
    for fuel in fuel_order:
        subset = df_filtered.loc[df_filtered['primary_fuel'] == fuel]
        if not subset.empty:
            cat = subset['energy_category'].iloc[0]
            fig.add_trace(go.Box(
                y=subset['capacity_mw'],
                name=fuel,
                marker_color=colors[cat],
                opacity=0.7,
                boxpoints='outliers',
                showlegend=False
            ), row=1, col=2)
    fig.update_layout(
        template='simple_white',
        title='Global Power Plant Capacity Distributions (2017)',
        height=560,
        width=1250,
        margin=dict(t=80, b=200, l=70, r=160),
        hoverlabel=dict(bgcolor='white')
    )
    fig.add_annotation(
        text=data_note, x=0.5, y=-0.34,
        xref='paper', yref='paper', showarrow=False,
        font=dict(size=11, color='gray')
    )
    return fig

# ===========================
# TAB 2 — TEMPORAL ANALYSIS
# ===========================

def fig_tab2_area(df_filtered):
    df_trend = df_filtered[df_filtered['commissioning_year'].notna()].copy()
    df_trend['commissioning_year'] = pd.to_numeric(df_trend['commissioning_year'], errors='coerce').round().astype(int)
    df_trend = df_trend[df_trend['commissioning_year'].between(1950, 2016)]
    annual_capacity = (
        df_trend.groupby(['commissioning_year', 'primary_fuel'], as_index=False)['capacity_mw'].sum()
    )
    fuel_order = (
        annual_capacity.groupby('primary_fuel')['capacity_mw'].sum().sort_values(ascending=True).index.tolist()
    )
    fig = px.area(
        annual_capacity,
        x='commissioning_year', y='capacity_mw', color='primary_fuel',
        category_orders={'primary_fuel': fuel_order},
        labels={'capacity_mw': 'Installed Capacity (MW)', 'commissioning_year': 'Year'},
        title='Global Installed Capacity Over Time by Fuel Type (1950–2016)',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    fig.update_layout(template='simple_white', height=600)
    return fig


def fig_tab2_scatter(df_filtered):
    d = df_filtered.dropna(subset=["capacity_mw", "commissioning_year", "energy_category"]).copy()
    d["commissioning_year"] = pd.to_numeric(d["commissioning_year"], errors="coerce")
    d = d[d["commissioning_year"].between(1950, 2016)]
    d = d.groupby("energy_category", group_keys=False).sample(frac=0.05, random_state=42)
    np.random.seed(42)
    x_map = {"Non-Renewable": 0, "Renewable": 1}
    d["x_jitter"] = d["energy_category"].map(x_map) + (np.random.rand(len(d)) - 0.5) * 0.25
    fig = px.scatter(
        d, x="x_jitter", y="capacity_mw", color="commissioning_year",
        color_continuous_scale="Viridis",
        hover_data=["country_long", "primary_fuel", "commissioning_year"],
        title="Plant Capacity by Type and Year (log scale)", log_y=True
    )
    fig.update_layout(template="simple_white", height=550)
    return fig

# ===========================
# TAB 3 — GLOBAL MAP
# ===========================

def fig_tab3_map(df_filtered):
    df_map = df_filtered.dropna(subset=['latitude', 'longitude']).copy()
    df_map['capacity_mw'] = pd.to_numeric(df_map['capacity_mw'], errors='coerce')
    df_map['capacity_size'] = np.sqrt(df_map['capacity_mw'].clip(lower=0))
    MAX_PER_FUEL = 1000
    sampled_frames = []
    for fuel, group in df_map.groupby("primary_fuel"):
        n_samples = min(len(group), MAX_PER_FUEL)
        sampled_frames.append(group.sample(n=n_samples, random_state=42))
    df_map_limited = pd.concat(sampled_frames, ignore_index=True)
    fig = px.scatter_geo(
        df_map_limited,
        lat='latitude', lon='longitude', color='primary_fuel', size='capacity_size',
        hover_name='name',
        hover_data=['country_long', 'capacity_mw', 'energy_category'],
        projection='natural earth',
        title='Global Distribution of Power Plants by Fuel Type',
        color_discrete_sequence=px.colors.qualitative.Set1,
        size_max=10
    )
    fig.update_traces(marker=dict(opacity=0.75, line=dict(width=0.3, color='DarkSlateGrey'), sizemin=3))
    fig.update_layout(
        template='simple_white',
        geo=dict(showframe=False, showcoastlines=True, coastlinecolor='LightGray',
                 landcolor='rgb(240,240,240)', projection_scale=1.0),
        height=700
    )
    return fig

# ===========================
# TAB 4 — REGIONAL FUEL MIX
# ===========================

def fig_tab4_barhist(df_filtered, selected_country="United States Of America"):
    d = df_filtered[df_filtered['country_long'] == selected_country].copy()
    d['capacity_mw'] = pd.to_numeric(d['capacity_mw'], errors='coerce')
    bar_data = (
        d.groupby('primary_fuel', as_index=False)['capacity_mw']
         .sum().sort_values('capacity_mw', ascending=True)
    )
    cap_limit = d['capacity_mw'].quantile(0.99)
    hist_data = d[d['capacity_mw'] <= cap_limit].copy()
    fig = make_subplots(rows=1, cols=2, subplot_titles=[
        f"Installed Capacity by Fuel Type – {selected_country}",
        f"Plant Capacity Distribution – {selected_country}"
    ], column_widths=[0.45, 0.55])
    fig.add_trace(go.Bar(
        x=bar_data['capacity_mw'], y=bar_data['primary_fuel'],
        orientation='h', marker=dict(color=bar_data['capacity_mw'], colorscale='Cividis'),
        name='Installed Capacity'
    ), row=1, col=1)
    palette = px.colors.qualitative.Safe
    for i, fuel in enumerate(hist_data['primary_fuel'].unique()):
        subset = hist_data[hist_data['primary_fuel'] == fuel]
        fig.add_trace(go.Histogram(
            x=subset['capacity_mw'], name=fuel, opacity=0.6, nbinsx=60,
            marker_color=palette[i % len(palette)]
        ), row=1, col=2)
    fig.update_layout(template='simple_white', height=550, barmode='overlay', title_x=0.5)
    return fig

def fig_tab4_treemap(df_filtered, energy_filter="All"):
    """Treemap visualization for Tab 4 — Regional Fuel Mix by Energy Type."""

    d = df_filtered.copy()
    d["capacity_mw"] = pd.to_numeric(d["capacity_mw"], errors="coerce")

    if energy_filter == "All":
        fig = px.treemap(
            d,
            path=["country_long", "energy_category", "primary_fuel"],
            values="capacity_mw",
            color="energy_category",
            color_discrete_map={
                "Renewable": "#1f77b4",       # blue
                "Non-Renewable": "#d62728"    # red
            },
            title="Regional Fuel Mix by Country and Energy Type"
        )

    elif energy_filter == "Renewable":
        d = d[d["energy_category"] == "Renewable"].copy()
        fuels = sorted(d["primary_fuel"].unique())

        # Use light-to-dark blue palette
        palette = px.colors.sequential.Blues
        color_map = {fuel: palette[i % len(palette)] for i, fuel in enumerate(fuels)}

        fig = px.treemap(
            d,
            path=["country_long", "primary_fuel"],
            values="capacity_mw",
            color="primary_fuel",
            color_discrete_map=color_map,
            title="Renewable Capacity by Country and Fuel Type"
        )

    else:  # Non-Renewable
        d = d[d["energy_category"] == "Non-Renewable"].copy()
        fuels = sorted(d["primary_fuel"].unique())

        # Use light-to-dark red palette
        palette = px.colors.sequential.Reds
        color_map = {fuel: palette[i % len(palette)] for i, fuel in enumerate(fuels)}

        fig = px.treemap(
            d,
            path=["country_long", "primary_fuel"],
            values="capacity_mw",
            color="primary_fuel",
            color_discrete_map=color_map,
            title="Non-Renewable Capacity by Country and Fuel Type"
        )

    # Consistent layout
    fig.update_layout(
        template="simple_white",
        title_x=0.5,
        height=700,
        margin=dict(t=60, l=40, r=40, b=40)
    )

    return fig