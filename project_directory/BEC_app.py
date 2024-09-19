import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash import dash_table
import CoolProp.CoolProp as CP
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(style={'backgroundColor': '#f0f0f0', 'padding': '20px'}, children=[
    # Header Section
    html.Div(style={'backgroundColor': '#fff9c4', 'borderRadius': '10px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)'}, children=[
        html.H1("Boiler Efficiency based on Direct method as per ASME PTC-4", style={'color': '#000000', 'width': '100%', 'padding': '10px', 'fontFamily': 'Arial, sans-serif'}),
    ]),

    # Start
    html.Div(style={'flex': '1', 'textAlign': 'left', 'marginTop': '20px'}, children=[
        html.Button('Start', id='start-button', n_clicks=0, style={'backgroundColor': '#388e3c', 'color': '#ffffff', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'}),
    ]),

    # Input Section
    html.Div(id = 'input-section', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px', 'marginTop': '20px'}, children=[
        html.H1("Input Parameters", style={'backgroundColor': '#fff9c4', 'color': '#00000', 'textAlign': 'left', 'padding': '10px', 'border': 'none', 'borderRadius': '5px', 'fontSize': '30px'}),
        dash_table.DataTable(
            id='inputs-table',
            columns=[
                {'name': 'Description', 'id': 'description'},
                {'name': 'Value', 'id': 'input', 'editable': True},
                {'name': 'Unit', 'id': 'units'}
            ],
            data=[
                {'description': 'Fuel Mass Flow Rate', 'input': 3, 'units': 'kg/hr'},
                {'description': 'Higher Heating Value of Fuel', 'input': 4000, 'units': 'kcal/kg'},
                {'description': 'Feed Water Temperature', 'input': 95, 'units': '°C'},
                {'description': 'Feed Water Pressure', 'input': 1.8, 'units': 'Bar'},
                {'description': 'Main Steam Mass Flow Rate', 'input': 12, 'units': 'kg/hr'},
                {'description': 'Main Steam Temperature', 'input': 220, 'units': '°C'},
                {'description': 'Main Steam Pressure', 'input': 15, 'units': 'Bar'},
                {'description': 'Spray Water Mass Flow Rate', 'input': 1.5, 'units': 'kg/hr'},
                {'description': 'Hot Reheat Steam Temperature', 'input': 550, 'units': '°C'},
                {'description': 'Hot Reheat Steam Pressure', 'input': 2.517, 'units': 'Bar'},
                {'description': 'Cold Reheat Steam Mass Flow Rate', 'input': 1.2, 'units': 'kg/hr'},
                {'description': 'Cold Reheat Steam Temperature', 'input': 300, 'units': '°C'},
                {'description': 'Cold Reheat Steam Pressure', 'input': 2.544, 'units': 'Bar'},
                {'description': 'Reheat Spray Water Mass Flow Rate', 'input': 0.5, 'units': 'kg/hr'},
                {'description': 'Blowdown Steam Mass Flow Rate', 'input': 0.2, 'units': 'kg/hr'},
                {'description': 'Blowdown Steam Temperature', 'input': 495, 'units': '°C'},
                {'description': 'Blowdown Steam Pressure', 'input': 2.5, 'units': 'Bar'},
            ],
            style_table={'width': '40%', 'margin': '0', 'border': '1px solid #ddd'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'},
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

    # Button to calculate efficiency
    html.Div(id = 'run-button-section', style={'display': 'none', 'textAlign': 'left', 'marginTop': '20px'}, children=[
        html.Button('Run', id='calculate-button', n_clicks=0, style={'backgroundColor': '#3498db', 'color': '#ffffff', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'}),
    ]),
    # Basis
    html.Div(id = 'basis-section', style={'display': 'none', 'textAlign': 'left', 'marginTop': '20px'}, children=[
        html.Button('Basis: 1 kilogram of fuel input', style={'backgroundColor': '#f2f2f2', 'color': '#00000', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'fontSize': '16px'}),
    ]),
    
    html.Div(style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '20px'}, children=[
        # Heat Balance Table
        html.Div(style={'flex': '1', 'marginRight': '10px'}, children=[
            html.Div(id = 'heat-balance-section', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px'}, children=[
                html.H1("Heat Balance", style={'backgroundColor': '#fff9c4', 'color': '#00000', 'textAlign': 'left', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'fontSize': '30px'}),
                dash_table.DataTable(
                    id='heat-outputs-table',
                    columns=[
                        {'name': 'Description', 'id': 'description'},
                        {'name': 'Value', 'id': 'output'},
                        {'name': 'Unit', 'id': 'units'}
                    ],
                    style_table={'width': '100%', 'margin': '0', 'border': '1px solid #ddd'},
                    style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'},
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
        html.Img(src='assets/BFD.png', style={'width': '80%', 'maxWidth': '800px', 'flag': '1',}),
      ]),
    ]),


    # Output Section - Efficiency and Evaporation Ratio Table
    html.Div(id = 'efficiency-section', style={'display': 'none', 'backgroundColor': '#f2f2f2', 'borderRadius': '5px', 'boxShadow': '0px 4px 8px rgba(0,0,0,0.1)', 'padding': '10px', 'marginTop': '20px'}, children=[
        html.H1("Boiler Efficiency and Evaporation Ratio", style={'backgroundColor': '#fff9c4', 'color': '#00000', 'textAlign': 'left', 'padding': '15px', 'border': 'none', 'borderRadius': '5px', 'fontSize': '30px'}),
        dash_table.DataTable(
            id='efficiency-table',
            columns=[
                {'name': 'Description', 'id': 'description'},
                {'name': 'Value', 'id': 'output'},
                {'name': 'Unit', 'id': 'units'}
            ],
            style_table={'width': '40%', 'margin': '0', 'border': '1px solid #ddd'},
            style_cell={'textAlign': 'left', 'padding': '5px', 'fontFamily': 'Arial, sans-serif', 'fontSize': '16px'},
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
# Callback to reveal Input Section and Run Button after clicking Start
@app.callback(
    [Output('input-section', 'style'),
     Output('run-button-section', 'style')],
    [Input('start-button', 'n_clicks')]
)
def show_inputs(n_clicks):
    if n_clicks > 0:
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}

# Callback to reveal Output Section and after clicking Run
@app.callback(
    [Output('heat-outputs-table', 'data'),
     Output('efficiency-table', 'data'),
     Output('basis-section', 'style'),
     Output('heat-balance-section', 'style'),
     Output('bfd-section', 'style'),
     Output('efficiency-section', 'style')],
    [Input('calculate-button', 'n_clicks')],
    [State('inputs-table', 'data')]
)
def update_output(n_clicks, inputs_data):
    if n_clicks == 0:
        return [{'description': 'Error', 'output': 'An error occurred', 'units': ''}], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    
    try:
        input_dict = {item['description']: float(item['input']) for item in inputs_data}
        
        # Extract values from inputs data
        fuel_mass_flow_rate = input_dict['Fuel Mass Flow Rate']
        HHVF = input_dict['Higher Heating Value of Fuel']
        main_steam_mass_flow_rate = input_dict['Main Steam Mass Flow Rate']
        main_steam_temp = input_dict['Main Steam Temperature']
        main_steam_pressure = input_dict['Main Steam Pressure']
        feed_water_temp = input_dict['Feed Water Temperature']
        feed_water_pressure = input_dict['Feed Water Pressure']
        spray_water_mass_flow_rate = input_dict['Spray Water Mass Flow Rate']
        cold_reheat_steam_mass_flow_rate = input_dict['Cold Reheat Steam Mass Flow Rate']
        hot_reheat_steam_temp = input_dict['Hot Reheat Steam Temperature']
        hot_reheat_steam_pressure = input_dict['Hot Reheat Steam Pressure']
        cold_reheat_steam_temp = input_dict['Cold Reheat Steam Temperature']
        cold_reheat_steam_pressure = input_dict['Cold Reheat Steam Pressure']
        reheat_spray_mass_flow_rate = input_dict['Reheat Spray Water Mass Flow Rate']
        blowdown_steam_mass_flow_rate = input_dict['Blowdown Steam Mass Flow Rate']
        blowdown_steam_temp= input_dict['Blowdown Steam Temperature']
        blowdown_steam_pressure= input_dict['Blowdown Steam Pressure']
    except KeyError as e:
        print(f"KeyError: Missing data for key {e}")
        return [{'description': 'Error', 'output': f'Missing or invalid data: {str(e)}', 'units': ''}], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    except ValueError as e:
        print(f"ValueError: {e}")
        return [{'description': 'Error', 'output': f'Missing or invalid data: {str(e)}', 'units': ''}], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
    except Exception as e:
        print(f"Exception: {e}")
        return [{'description': 'Error', 'output': f'Missing or invalid data: {str(e)}', 'units': ''}], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    # Thermodynamic calculations using CoolProp
    try:
        main_steam_enthalpy = CP.PropsSI('H', 'T', main_steam_temp + 273.15, 'P', main_steam_pressure * 100000, 'Water') 
        feed_water_enthalpy = CP.PropsSI('H', 'T', feed_water_temp + 273.15, 'P', feed_water_pressure * 100000, 'Water')
        spray_water_enthalpy = CP.PropsSI('H', 'T', feed_water_temp + 273.15, 'P', feed_water_pressure * 100000, 'Water')
        hot_reheat_steam_enthalpy = CP.PropsSI('H', 'T', hot_reheat_steam_temp + 273.15, 'P', hot_reheat_steam_pressure * 100000, 'Water')
        cold_reheat_steam_enthalpy = CP.PropsSI('H', 'T', cold_reheat_steam_temp + 273.15, 'P', cold_reheat_steam_pressure * 100000, 'Water')
        reheat_spray_enthalpy = CP.PropsSI('H', 'T', feed_water_temp + 273.15, 'P', feed_water_pressure * 100000, 'Water')
        blowdown_steam_enthalpy = CP.PropsSI('H', 'T', blowdown_steam_temp + 273.15, 'P', blowdown_steam_pressure * 100000, 'Water')
    except Exception as e:
        print(f"CoolProp Error: {e}")
        return [{'description': 'Error', 'output': f'Missing or invalid data: {str(e)}', 'units': ''}], [], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    # Calculate energy input and output
    QrF = HHVF  # Assuming HHVF is in kJ/kg already
    QrMSt = ((main_steam_mass_flow_rate - spray_water_mass_flow_rate) * (main_steam_enthalpy - feed_water_enthalpy) + spray_water_mass_flow_rate * (main_steam_enthalpy - spray_water_enthalpy)) / fuel_mass_flow_rate / 4184
    QrRh = (cold_reheat_steam_mass_flow_rate * (hot_reheat_steam_enthalpy - cold_reheat_steam_enthalpy) + reheat_spray_mass_flow_rate * (hot_reheat_steam_enthalpy - reheat_spray_enthalpy)) / fuel_mass_flow_rate / 4184
    QrBd = (blowdown_steam_mass_flow_rate * (blowdown_steam_enthalpy - feed_water_enthalpy)) / fuel_mass_flow_rate / 4184
    QrO = QrMSt + QrRh + QrBd

    # Calculate efficiency and evaporation ratio
    EF = 100 * (QrO / QrF)
    Evaporation_ratio = main_steam_mass_flow_rate / fuel_mass_flow_rate

    # Prepare data for the outputs table
    Heat_data = [
        {'description': 'Heat Input Through Fuel', 'output': f'{QrF:.0f}', 'units': 'kcal/kg'},
        {'description': 'Heat Output In Main Steam', 'output': f'{QrMSt:.0f}', 'units': 'kcal/kg'},
        {'description': 'Heat Output In Reheat steam', 'output': f'{QrRh:.0f}', 'units': 'kcal/kg'},
        {'description': 'Heat Output In Blowdown steam', 'output': f'{QrBd:.0f}', 'units': 'kcal/kg'},
        {'description': 'Total Heat Output', 'output': f'{QrO:.0f}', 'units': 'kcal/kg'},
    ]
    Efficiency_data = [{'description':'Boiler Efficiency', 'output': f'{EF:.0f}', 'units': '%'},
                    {'description':'Evaporation Ratio', 'output': f'{Evaporation_ratio:.2f}', 'units': ''}]
    
    return Heat_data, Efficiency_data, {'display': 'flex'}, {'display': 'block'}, {'display': 'flex'}, {'display': 'block'}

if __name__ == '__main__':
    app.run_server(debug=True)
