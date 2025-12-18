from dash import Dash, dcc, html, Input, Output, State, callback
import dash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

from data_loader import load_dataset
from preprocess import preprocess_data
import visualizations as vz


# =============================
# LOAD AND PREPARE DATA
# =============================
df = load_dataset()
prep = preprocess_data(df)

df = prep["df"]
df_filtered = prep["df_filtered"]
fuel_palette = prep["fuel_palette"]
numeric_palette = prep["numeric_palette"]
energy_colors = prep["energy_colors"]
data_note = prep["data_note"]

# =============================
# DASH APP LAYOUT
# =============================
app = Dash(__name__)
app.title = "Global Power Plant Visualization"

app.layout = html.Div([
    dcc.Tabs([

        # TAB 1
        dcc.Tab(label="Global Capacity Overview", children=[
            html.H2("Global Renewable vs Non-Renewable Capacity (2017)"),

            html.Div([
                html.Div([
                    html.Label("Select Fuel Type:"),
                    dcc.Dropdown(
                        id="fuel-filter",
                        options=[{"label": f, "value": f} for f in sorted(df["primary_fuel"].unique())],
                        value=None,
                        placeholder="All fuels",
                        clearable=True
                    )
                ], style={"width": "45%", "display": "inline-block"}),

                html.Div([
                    html.Label("Capacity Threshold (MW):"),
                    dcc.Slider(
                        id="capacity-threshold",
                        min=0,
                        max=int(df["capacity_mw"].max()),
                        step=1000,
                        value=int(df["capacity_mw"].max()),
                        tooltip={"placement": "bottom"}
                    )
                ], style={"width": "45%", "display": "inline-block", "marginLeft": "5%"})
            ], style={"marginBottom": "40px"}),

            dcc.Graph(id="tab1-scatter"),
            dcc.Graph(id="tab1-deviation"),
            dcc.Graph(id="tab1-piebar"),
            dcc.Graph(id="tab1-box"),
        ]),

        # TAB 2
        dcc.Tab(label="Capacity Trends and Timing", children=[
            html.H2("Global Capacity Trends (1950–2016)"),

            html.Label("Select Year Range:"),
            dcc.RangeSlider(
                id="year-range",
                min=1950, max=2016, step=1,
                value=[1950, 2016],
                marks={year: str(year) for year in range(1950, 2017, 10)}
            ),
            dcc.Graph(id="tab2-area"),
            dcc.Graph(id="tab2-scatter")
        ]),

        # TAB 3
        dcc.Tab(label="Global Power Plant Map", children=[
            html.H2("Global Power Plant Map (1950–2016)"),

            html.Div([
                html.Label("Filter by Energy Category:"),
                dcc.Dropdown(
                    id="tab3-energy-filter",
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "Renewable", "value": "Renewable"},
                        {"label": "Non-Renewable", "value": "Non-Renewable"}
                    ],
                    value="All",
                    clearable=False
                ),
                html.Label("Select Year:"),
                dcc.Slider(
                    id="tab3-year",
                    min=1950, max=2016, step=1, value=2016,
                    marks={year: str(year) for year in range(1950, 2017, 10)},
                    tooltip={"placement": "bottom"}
                ),
                html.Div([
                    html.Button("▶ Play", id="tab3-play", n_clicks=0, style={"marginRight": "10px"}),
                    html.Button("⏸ Pause", id="tab3-pause", n_clicks=0)
                ], style={"marginTop": "10px"}),
                dcc.Interval(id="tab3-interval", interval=1000, n_intervals=0, disabled=True)
            ], style={"marginBottom": "30px", "width": "80%", "marginLeft": "5%"}),

            dcc.Graph(id="tab3-map")
        ]),

        # TAB 4
        dcc.Tab(label="Regional Fuel Mix", children=[
            html.H2("Regional Fuel Mix Comparison"),

            html.Div([
                html.Label("Select Country:"),
                dcc.Dropdown(
                    id="tab4-country",
                    options=sorted([{"label": c, "value": c} for c in df_filtered["country_long"].unique()],
                                   key=lambda x: x["label"]),
                    value="United States Of America",
                    clearable=False
                )
            ], style={"width": "40%", "marginLeft": "5%", "marginBottom": "25px"}),

            dcc.Graph(id="tab4-barhist"),

            html.Div([
                html.Label("Treemap Filter (Energy Category):"),
                dcc.Dropdown(
                    id="tab4-energy-filter",
                    options=[
                        {"label": "All", "value": "All"},
                        {"label": "Renewable", "value": "Renewable"},
                        {"label": "Non-Renewable", "value": "Non-Renewable"}
                    ],
                    value="All",
                    clearable=False
                )
            ], style={"width": "30%", "marginLeft": "5%", "marginTop": "40px"}),

            dcc.Graph(id="tab4-treemap")
        ])
    ])
])

# =============================
# TAB 1 CALLBACKS
# =============================
@callback(
    [
        Output("tab1-scatter", "figure"),
        Output("tab1-deviation", "figure"),
        Output("tab1-piebar", "figure"),
        Output("tab1-box", "figure")
    ],
    [
        Input("fuel-filter", "value"),
        Input("capacity-threshold", "value")
    ]
)
def update_tab1(selected_fuel, cap_threshold):
    df_local = df.copy()
    if selected_fuel:
        df_local = df_local[df_local["primary_fuel"] == selected_fuel]
    df_local = df_local[df_local["capacity_mw"] <= cap_threshold]
    df_trim = df_local[df_local["capacity_mw"] <= df_local["capacity_mw"].quantile(0.95)]

    fig1 = vz.fig_tab1_scatter(df_local, data_note)
    fig2 = vz.fig_tab1_deviation(df_trim)
    fig3 = vz.fig_tab1_piebar(df_local, data_note)
    fig4 = vz.fig_tab1_box(df_trim, data_note)
    return fig1, fig2, fig3, fig4


# =============================
# TAB 2 CALLBACKS
# =============================
@callback(
    [
        Output("tab2-area", "figure"),
        Output("tab2-scatter", "figure")
    ],
    Input("year-range", "value")
)
def update_tab2(year_range):
    year_min, year_max = year_range
    df_year = df_filtered[df_filtered["commissioning_year"].between(year_min, year_max)]
    return vz.fig_tab2_area(df_year), vz.fig_tab2_scatter(df_year)


# =============================
# TAB 3 CALLBACKS
# =============================
@callback(
    Output("tab3-map", "figure"),
    [Input("tab3-year", "value"), Input("tab3-energy-filter", "value")]
)
def update_tab3(year, energy_filter):
    df_map = df_filtered[df_filtered["commissioning_year"] <= year].copy()
    if energy_filter != "All":
        df_map = df_map[df_map["energy_category"] == energy_filter]
    return vz.fig_tab3_map(df_map)


@callback(
    Output("tab3-year", "value"),
    Output("tab3-interval", "disabled"),
    Input("tab3-interval", "n_intervals"),
    Input("tab3-play", "n_clicks"),
    Input("tab3-pause", "n_clicks"),
    State("tab3-interval", "disabled"),
    State("tab3-year", "value")
)
def animate_tab3(n_intervals, play_clicks, pause_clicks, disabled, year):
    ctx = dash.callback_context
    if not ctx.triggered:
        return year, disabled
    trigger = ctx.triggered_id
    if trigger == "tab3-play":
        return year, False
    if trigger == "tab3-pause":
        return year, True
    if trigger == "tab3-interval" and not disabled:
        next_year = year + 1 if year < 2016 else 1950
        return next_year, False
    return year, disabled


# =============================
# TAB 4 CALLBACKS
# =============================
@callback(
    Output("tab4-barhist", "figure"),
    Input("tab4-country", "value")
)
def update_tab4_barhist(country):
    return vz.fig_tab4_barhist(df_filtered, selected_country=country)


@callback(
    Output("tab4-treemap", "figure"),
    Input("tab4-energy-filter", "value")
)
def update_tab4_treemap(filter_choice):
    return vz.fig_tab4_treemap(df_filtered, energy_filter=filter_choice)


# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)