import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from therma_boiler.project import page3  # Import logic from page3.py
from therma_boiler.config.main import STORE_ID

dash.register_page(__name__)
app = dash.get_app()

PAGE_TITLE = "Page Three"

class PageIDs:
    def __init__(self):
        filename = os.path.basename(__file__)
        prefix = filename.replace(".py", "")
        self.prefix = prefix
        self.status = f"{prefix}_status"
        self.input = f"{prefix}_input"
        self.run_btn = f"{prefix}_run_btn"
        self.output = f"{prefix}_output"

        # IDs for input fields
        self.fuel_mass_flow_rate = f"{prefix}_fuel_mass_flow_rate"
        self.feed_water_temperature = f"{prefix}_feed_water_temperature"
        self.feed_water_pressure = f"{prefix}_feed_water_pressure"
        self.HHV = f"{prefix}_HHV"
        self.steam_mass_flow_rate = f"{prefix}_steam_mass_flow_rate"
        self.steam_temperature = f"{prefix}_steam_temperature"
        self.steam_pressure = f"{prefix}_steam_pressure"
        self.steam_type = f"{prefix}_steam_type"
        self.spray_water_mass_flow_rate = f"{prefix}_spray_water_mass_flow_rate"
        self.cold_reheat_mass_flow_rate = f"{prefix}_cold_reheat_mass_flow_rate"
        self.hot_reheat_temperature = f"{prefix}_hot_reheat_temperature"
        self.hot_reheat_pressure = f"{prefix}_hot_reheat_pressure"
        self.cold_reheat_temperature = f"{prefix}_cold_reheat_temperature"
        self.cold_reheat_pressure = f"{prefix}_cold_reheat_pressure"
        self.reheat_spray_mass_flow_rate = f"{prefix}_reheat_spray_mass_flow_rate"

ids = PageIDs()

# Layout
layout = html.Div(
    [
        html.H1("Thermalysis Boiler", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),

        # Boiler Design and Operating Data
        html.Div(id='boiler-design-specs', style={'padding-top': '20px'}),
        html.Div(id='operating-data-table', style={'padding-top': '20px'}),
        html.Div(id='efficiency-result', style={'padding-top': '20px'}),

        # Divs for dynamic content
        html.Div(id=ids.status),
        html.Div(id=ids.input, className="px-6 pb-2 w-60"),
        html.Div(id=ids.output, className="px-6 pb-2 w-60"),

        # Store for boiler design data
        dcc.Store(id='store-boiler-design')
    ],
    className="w-full",
)

# Callback to display boiler design specs
@app.callback(
    Output('boiler-design-specs', 'children'),
    [Input(STORE_ID, "data")],
)
def display_boiler_design_table(n_clicks):
    if n_clicks and n_clicks != 0:
        return html.Div([
            html.H3("Boiler Design Specifications"),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Boiler Rated Capacity (tph)"), dbc.Input(id="boiler-capacity", type='number', placeholder="Enter value...", style={'textAlign': 'center'}, required=True)])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Rated Working Pressure (bar)"), dbc.Input(id="boiler-pressure", type='number', placeholder="Enter value...", style={'textAlign': 'center'}, required=True)])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Boiler Efficiency (%)"), dbc.Input(id="boiler-efficiency", type='number', placeholder="Enter value...", style={'textAlign': 'center'}, required=True)])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Type of Steam Generated"), dcc.Dropdown(
                id='dropdown-type-of-steam',
                options=[{'label': 'Saturated', 'value': 'Saturated'}, {'label': 'Supersaturated', 'value': 'Supersaturated'}],
                value='Saturated', style={'width': '250px'}
            )])]),
            html.Br(),
            
            dbc.Button("Save Boiler Design", color="primary", id='save-boiler-design-btn', style={'width': '200px'}),
            html.Div(id='boiler-design-alert')
        ])
    return html.Div()

# Callback to store boiler design data
@app.callback(
    [Output('boiler-design-alert', 'children'), Output('store-boiler-design', 'data')],
    Input('save-boiler-design-btn', 'n_clicks'),
    [State('boiler-capacity', 'value'), State('boiler-pressure', 'value'), State('boiler-efficiency', 'value'),
     State('dropdown-type-of-steam', 'value')]
)
def save_boiler_design(n_clicks, capacity, pressure, efficiency, steam_type):
    if n_clicks and (not capacity or not pressure or not efficiency or not steam_type):
        return dbc.Alert("Please fill in all required fields.", color="danger"), None
    if n_clicks:
        return dbc.Alert("Boiler design saved successfully.", color="success"), {
            'capacity': capacity,
            'pressure': pressure,
            'efficiency': efficiency,
            'steam_type': steam_type,
           
        }
    return '', None

# Callback to display operating data table after boiler design is saved
@app.callback(
    Output('operating-data-table', 'children'),
    Input('save-boiler-design-btn', 'n_clicks')
)
def display_operating_data_table(n_clicks):
    if n_clicks:
        return display_operating_data()
    return html.Div()

# Function to display operating data table
def display_operating_data():
    return html.Div([
        html.H3("Operating Data"),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("Fuel Mass Flow Rate (kg/hr)"), dbc.Input(id="fuel-mass-flow-rate", type='number', placeholder="Enter value...", style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("Feed water Temperature (°C)"), dbc.Input(id="feed-water-temperature", type='number', placeholder="Enter value...",style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("Feed water Pressure (bar)"), dbc.Input(id="feed-water-pressure", type='number', placeholder="Enter value...", style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("HHV of Fuel (kcal/kg)"), dbc.Input(id="HHV", type='number', placeholder="Enter value...", style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("Steam Mass Flow Rate (kg/hr)"), dbc.Input(id="steam-mass-flow-rate", type='number', placeholder="Enter value...", style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.Row([dbc.InputGroup([dbc.InputGroupText("Steam Temperature (°C)"), dbc.Input(id="steam-temperature", type='number', placeholder="Enter value...",style={'textAlign': 'center'})])]),
        html.Br(),
        dbc.InputGroup([dbc.InputGroupText("Steam Pressure (bar)"), dbc.Input(id="steam-pressure", type='number', placeholder="Enter value...",style={'textAlign': 'center'})]),
        html.Br(),
        # Supersaturated Inputs
        html.Div([
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Spray Water Mass Flow Rate (kg/hr)"), dbc.Input(id='spray-water-mass-flow-rate', type='number', style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Cold Reheat Steam Mass Flow Rate (kg/hr)"), dbc.Input(id='cold-reheat-mass-flow-rate', type='number',style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Cold Reheat Steam Temperature (°C)"), dbc.Input(id='cold-reheat-temperature', type='number',style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Cold Reheat Steam Pressure (bar)"), dbc.Input(id='cold-reheat-pressure', type='number',style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Hot Reheat Steam Temperature (°C)"), dbc.Input(id='hot-reheat-temperature', type='number',style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.Row([dbc.InputGroup([dbc.InputGroupText("Hot Reheat Steam Pressure (bar)"), dbc.Input(id='hot-reheat-pressure', type='number',style={'textAlign': 'center'})])]),
            html.Br(),
            dbc.InputGroup([dbc.InputGroupText("Reheat Spray Water Mass Flow Rate (kg/hr)"), dbc.Input(id='reheat-spray-mass-flow-rate', type='number',style={'textAlign': 'center'})]),
            html.Br(),
        ], id='super-saturated-inputs'),
        dbc.Button("Proceed to Efficiency Calculation", color="success", id='proceed-efficiency-btn', style={'width': '300px'})
    ])

# Callback to toggle supersaturated inputs visibility
@app.callback(
    Output('super-saturated-inputs', 'style'),
    Input('dropdown-type-of-steam', 'value')
)
def toggle_supersaturated_inputs(steam_type):
    if steam_type == 'Supersaturated':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# Callback to calculate and display boiler efficiency in a table
@app.callback(
    Output('efficiency-result', 'children'),
    Input('proceed-efficiency-btn', 'n_clicks'),
    State('dropdown-type-of-steam', 'value'),
    State('fuel-mass-flow-rate', 'value'),
    State('feed-water-temperature', 'value'),
    State('feed-water-pressure', 'value'),
    State('HHV', 'value'),
    State('steam-mass-flow-rate', 'value'),
    State('steam-temperature', 'value'),
    State('steam-pressure', 'value'),
    # Supersaturated Inputs
    State('spray-water-mass-flow-rate', 'value'),
    State('cold-reheat-mass-flow-rate', 'value'),
    State('reheat-spray-mass-flow-rate', 'value'),
    State('hot-reheat-temperature', 'value'),
    State('cold-reheat-temperature', 'value'),
    State('hot-reheat-pressure', 'value'),
    State('cold-reheat-pressure', 'value'),
    prevent_initial_call=True
)
   
def display_efficiency(n_clicks, steam_type, fuel_mass_flow_rate, feed_water_temperature, feed_water_pressure, HHV, steam_mass_flow_rate, steam_temperature, steam_pressure, spray_water_mass_flow_rate, cold_reheat_mass_flow_rate, reheat_spray_mass_flow_rate, hot_reheat_temperature, cold_reheat_temperature, hot_reheat_pressure, cold_reheat_pressure):
    if n_clicks:   
        result = page3.calculate_boiler_efficiency(
                fuel_mass_flow_rate, feed_water_temperature, feed_water_pressure, HHV, steam_mass_flow_rate, steam_temperature, steam_pressure, steam_type,
                spray_water_mass_flow_rate, cold_reheat_mass_flow_rate, reheat_spray_mass_flow_rate, hot_reheat_temperature, cold_reheat_temperature, hot_reheat_pressure, cold_reheat_pressure)
            
        if steam_type == 'Saturated':
            # Unpack the three returned values
            heat_input, heat_output_main, efficiency, evaporation_ratio = result
            data = [
                {"Description": "Heat Input through Fuel", "value": heat_input, "unit": "kcal/hr"},
                {"Description": "Heat Output in Main Steam", "value": heat_output_main, "unit": "kcal/hr"},
                {"Description": "Boiler Efficiency", "value": efficiency, "unit": "%"},
                {"Description": "Evaporation ratio", "value": evaporation_ratio, "unit": "%"}
            ]
        elif steam_type == 'Supersaturated':
            # Unpack the five returned values
            heat_input, heat_output_main, heat_output_reheat, total_heat_output, efficiency, evaporation_ratio = result
            data = [
                {"Description": "Heat Input through Fuel", "value": heat_input, "unit": "kcal/hr"},
                {"Description": "Heat Output in Main Steam", "value": heat_output_main, "unit": "kcal/hr"},
                {"Description": "Heat Output in Reheat Steam", "value": heat_output_reheat, "unit": "kcal/hr"},
                {"Description": "Total Heat Output", "value": total_heat_output, "unit": "kcal/hr"},
                {"Description": "Boiler Efficiency", "value": efficiency, "unit": "%"},
                {"Description": "Evaporation ratio", "value": evaporation_ratio, "unit": "%"}
            ]
        else:
            return dbc.Alert("Invalid steam type.", color="danger")

        return html.Div([
            html.H3("Boiler Performance"),
            DataTable(
                columns=[{"name": "Description", "id": "Description"},
                         {"name": "Value", "id": "value"},
                         {"name": "Unit", "id": "unit"}],
                data=data,
                style_cell={'textAlign': 'left'},
                style_table={'width': '60%', 'fontSize': '18px'}
            )
        ])
    return html.Div()



