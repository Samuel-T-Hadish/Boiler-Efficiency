import os
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dash_table import DataTable
from therma_boiler.project import page3  # Import logic from page3.py
from therma_boiler.config.main import STORE_ID
import CoolProp.CoolProp as CP

dash.register_page(__name__)
app = dash.get_app()

PAGE_TITLE = "Page Four"

class PageIDs:
    def __init__(self):
        filename = os.path.basename(__file__)
        prefix = filename.replace(".py", "")
        self.prefix = prefix
        self.status = f"{prefix}_status"
        self.input = f"{prefix}_input"
        self.run_btn = f"{prefix}_run_btn"
        self.output = f"{prefix}_output"
        # Default parameters for calculations

ids = PageIDs()

Parameter_dict = {
    'Ambient Temperature': 26.7,
    'Relative Humidity': 50,
    'Radiation loss': 0.05,
    'Oxygen content on wet basis': 5,
    'Flue gas exit temperature': 446,
    'CO2 Mass fraction': 0.1527,
    'H2O Mass fraction': 0.0715,
    'O2 Mass fraction': 0.062,
    'N2 Mass fraction': 0.709,
    'SO2 Mass fraction': 0.502e-2,
    'Combustion air temperature': 40,
    'Fuel temperature': 25,
    'Fuel mass flow rate': 12000,
    'Datum temperature': 15,
    'hL': 38520.4,
    'Specific heat of Fuel': 1.7,
    'Steam Mass Flow Rate': 4200,
    'Enthalpy of steam': 2777,
    'Flue Gas Mass': 239165.572,
    'Wet Air Mass': 222965.572,
    'Humidity of air': 0.4,
    'Psat': CP.PropsSI('P', 'T', 26.7 + 273.15, 'Q', 0, 'Water'),
}

# Calculate molar fraction water equivalent to humidity
molar_fraction_water_equivalent_to_humidity = (
    Parameter_dict['Relative Humidity'] * Parameter_dict['Psat'] * 18 / 28 / 100 / 101325
)

# Layout
layout = html.Div(
    [
        html.H1("Thermalysis Fired Heater", className="app-title"),
        html.H2(PAGE_TITLE, className="page-title"),
        html.Hr(),

        # Start button
    html.Div(style={'flex': '1', 'textAlign': 'left', 'marginTop': '20px'}, children=[
        html.Button('Start', id='start-button', n_clicks=0, style={'backgroundColor': '#388e3c', 'color': '#ffffff', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'})
    ]),

    # Input Section
    html.Div(id='input-section', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px', 'marginTop': '20px'}, children=[
        html.H2("Input Parameters", style={'backgroundColor': '#fff9c4', 'color': '#000', 'padding': '10px'}),
        
        # Input table
        dash_table.DataTable(
            id='inputs-table',
            columns=[
                {'name': 'Description', 'id': 'description'},
                {'name': 'Value', 'id': 'input', 'editable': True},
                {'name': 'Unit', 'id': 'units'}
            ],
            data=[
                {'description': 'Ambient Temperature', 'input': 26.7, 'units': 'C'},
                {'description': 'Relative Humidity', 'input': 50, 'units': '%'},
                {'description': 'Radiation loss', 'input': 0.05, 'units': '%'},
                {'description': 'Oxygen content on wet basis', 'input': 5, 'units': '%'},
                {'description': 'Flue Gas Exit Temperature', 'input': 446, 'units': '°C'},
                {'description': 'CO2 Mass fraction', 'input': 0.1527, 'units': ''},           
                {'description': 'H2O Mass fraction', 'input': 0.0715, 'units': ''},
                {'description': 'O2 Mass fraction', 'input': 0.062, 'units': ''},
                {'description': 'N2 Mass fraction', 'input': 0.709, 'units': ''},
                {'description': 'SO2 Mass fraction', 'input': 0.502e-2, 'units': ''},
                {'description': 'Combustion air temperature', 'input': 40, 'units': ''},
                {'description': 'Fuel temperature', 'input': 25, 'units': ''},
                {'description': 'Fuel Mass Flow Rate', 'input': 12000, 'units': 'kg/hr'},
                {'description': 'Datum temperature', 'input': 15, 'units': 'C'},
                {'description': 'hL', 'input': 38520.4, 'units': 'kJ/kg'},
                {'description': 'Specific heat of Fuel', 'input': 1.7, 'units': 'kJ/kg.K'},
                {'description': 'Steam Mass Flow Rate', 'input': 4200, 'units': 'kg/hr'},
                {'description': 'Enthalpy of Steam', 'input': 2777, 'units': 'kJ/kg'},
                {'description': 'Flue Gas Mas', 'input': 239165.572, 'units': 'kg'},
                {'description': 'Wet Air Mass', 'input': 222965.572, 'units': 'kg'},
                {'description': 'Humidity of air', 'input': 0.4, 'units': 'kg h2o/ kg wet air'},
                {'description': 'Psat', 'input': CP.PropsSI('P', 'T', 26.7 + 273.15, 'Q', 0, 'Water'), 'units': 'Pa'},
    
            ],
            style_table={'width': '60%', 'margin': '0', 'border': '1px solid #ddd'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#f2f2f2'},
                {'if': {'row_index': 'even'}, 'backgroundColor': '#ffffff'}
            ]
        ),
    
    ]),

    # Run button
    html.Div(id='run-button-section', style={'display': 'none', 'textAlign': 'left', 'marginTop': '20px'}, children=[
        html.Button('Run', id='calculate-button', n_clicks=0, style={'backgroundColor': '#3498db', 'color': '#ffffff', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'})
    ]),
    
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        # Heat Balance Table
        html.Div(style={'flex': '1', 'marginRight': '10px'}, children=[
            html.Div(id = 'output-results', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px'}, children=[
                html.H1("Heat Balance", style={'backgroundColor': '#fff9c4', 'color': '#00000', 'textAlign': 'left', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'fontSize': '30px'}),
                dash_table.DataTable(
                    id='output-table',
                    columns=[
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Value', 'id': 'output'},
                        {'name': 'Unit', 'id': 'units'}
                    ],
                    style_table={'width': '60%', 'margin': '0', 'border': '1px solid #ddd'},
                    style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px', 'font-weight': 'bold'},
                    style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f2f2f2'
                        },
                        {
                            'if': {'row_index': 'even'},
                            'backgroundColor': '#ffffff'
                        }
                    ]
                ),
            ]),
        ]),

        # Block Flow Diagram
        html.Div(id = 'bfd-section', style={'display': 'none', 'flex': '1', 'marginLeft': '10px'}, children=[
        html.Img(src='assets/BFD.png', style={'width': '100%', 'maxWidth': '800px', 'flag': '1',}),
        ]),
    ]),
    # Output Section - Efficiency 
    html.Div(id = 'efficiency-section', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px', 'marginTop': '20px'}, children=[
        html.H1("Efficiency", style={'backgroundColor': '#fff9c4', 'color': '#00000', 'textAlign': 'left', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'fontSize': '30px'}),
        dash_table.DataTable(
            id='efficiency-table',
            columns=[
                {'name': 'Description', 'id': 'description'},
                {'name': 'Value', 'id': 'output'},
                {'name': 'Unit', 'id': 'units'}
            ],
            style_table={'width': '60%', 'margin': '0', 'border': '1px solid #ddd'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '20px', 'font-weight': 'bold'},
            style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f2f2f2'
                },
                {
                    'if': {'row_index': 'even'},
                    'backgroundColor': '#ffffff'
                }
            ]
        ),
    ])
])


# Callback to reveal input and run sections
@app.callback(
    [Output('input-section', 'style'), Output('run-button-section', 'style')],
    [Input('start-button', 'n_clicks')]
)
def show_inputs(n_clicks):
    if n_clicks > 0:
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}

# Callback to calculate results
@app.callback(
    [Output('output-table', 'data'), Output('output-results', 'style'), Output('bfd-section', 'style'), Output('efficiency-table', 'data'), Output('efficiency-section', 'style')],
    [Input('calculate-button', 'n_clicks')],
    [State('inputs-table', 'data')]
)
def update_output(n_clicks, inputs_data):
    if n_clicks == 0:
        return [], {'display': 'none'}, {'display': 'none'}, [], {'display': 'none'}
    

    input_dict = {item['description']: float(item['input']) for item in inputs_data}
    
    # Extract values from inputs
    fuel_mass_flow_rate = input_dict['Fuel Mass Flow Rate']
    flue_gas_exit_temp = input_dict['Flue Gas Exit Temperature']
    steam_mass_flow_rate = input_dict['Steam Mass Flow Rate']
    enthalpy_steam = input_dict['Enthalpy of Steam']
    
    # Calculate Q_in and Qu
    Q_in = page4.energy_input_from_fuel(fuel_mass_flow_rate, Parameter_dict['hL'], Parameter_dict['Specific heat of Fuel'],
                                  molar_fraction_water_equivalent_to_humidity, Parameter_dict['Fuel temperature'],
                                  Parameter_dict['Datum temperature'], Parameter_dict['Combustion air temperature'],
                                  Parameter_dict['Wet Air Mass'], steam_mass_flow_rate, enthalpy_steam)
    
    Qu = page4.Energy_Output(fuel_mass_flow_rate, Parameter_dict['hL'], Parameter_dict['Radiation loss'], flue_gas_exit_temp,
                       Parameter_dict['Datum temperature'], Parameter_dict['CO2 Mass fraction'], Parameter_dict['Flue Gas Mass'],
                       Parameter_dict['O2 Mass fraction'], Parameter_dict['N2 Mass fraction'], Parameter_dict['H2O Mass fraction'],
                       Parameter_dict['SO2 Mass fraction'], Q_in)
    
    # Calculate efficiencies
    net_efficiency = page4.efficiency_by_direct_method_Net(Qu, Q_in)
    gross_efficiency = page4.efficiency_by_direct_method_Gross(Qu, Q_in, Parameter_dict['hL'], molar_fraction_water_equivalent_to_humidity)
    fuel_efficiency = page4.efficiency_by_direct_method_Fuel(Qu, fuel_mass_flow_rate, Parameter_dict['hL'])
    
    # Prepare output data
    output_data = [
        {'description': 'Heat Input', 'output': f'{Q_in:.2f}', 'units': 'kJ'},
        {'description': 'Energy Useful', 'output': f'{Qu:.2f}', 'units': 'kJ'},

    ]
    Efficiency_data = [
        {'description': 'Net Efficiency', 'output': f'{net_efficiency:.2f}', 'units': '%'},
        {'description': 'Gross Efficiency', 'output': f'{gross_efficiency:.2f}', 'units': '%'},
        {'description': 'Fuel Efficiency', 'output': f'{fuel_efficiency:.2f}', 'units': '%'} 
    ]
    
    return output_data, {'display': 'block'}, {'display': 'block'}, Efficiency_data, {'display': 'block'}
if __name__ == '__main__':
    app.run_server(debug=True)
