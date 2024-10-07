import CoolProp.CoolProp as CP

def calculate_boiler_efficiency(fuel_mass_flow_rate, feed_water_temperature, feed_water_pressure, HHV, steam_mass_flow_rate, steam_temperature, steam_pressure, steam_type, spray_water_mass_flow_rate, cold_reheat_mass_flow_rate, hot_reheat_temperature, hot_reheat_pressure, cold_reheat_temperature, cold_reheat_pressure, reheat_spray_mass_flow_rate):
    
    QrF = fuel_mass_flow_rate * HHV  # Heat input from fuel

    if steam_type == 'Saturated':
       # Energy output from main steam
        main_steam_enthalpy = CP.PropsSI('H', 'T', steam_temperature + 273.15, 'P', steam_pressure * 1e5, 'Water') / 4184
        feed_water_enthalpy = CP.PropsSI('H', 'T', feed_water_temperature + 273.15, 'P', feed_water_pressure * 1e5, 'Water') / 4184

        QrMSt = steam_mass_flow_rate * (main_steam_enthalpy - feed_water_enthalpy)
        QrO = QrMSt
        # Boiler efficiency calculation
        efficiency = 100 * (QrO / QrF)
        # Evaporation ratio (check for division by zero)
        if fuel_mass_flow_rate == 0:
            evaporation_ratio = 0
        else:
            evaporation_ratio = steam_mass_flow_rate / fuel_mass_flow_rate

        return round(QrF, 2), round(QrMSt, 2), round(efficiency, 2), round(evaporation_ratio, 2)

    elif steam_type == 'Supersaturated':
         
        # Check if reheat steam temperature and pressure are provided and valid
        if cold_reheat_pressure <= 0 or hot_reheat_pressure <= 0:
            return None  # Error handling

        # Perform enthalpy calculations for reheat steam
        main_steam_enthalpy = CP.PropsSI('H', 'T', steam_temperature + 273.15, 'P', steam_pressure * 1e5, 'Water') / 4184
        feed_water_enthalpy = CP.PropsSI('H', 'T', feed_water_temperature + 273.15, 'P', feed_water_pressure * 1e5, 'Water') / 4184
        spray_water_enthalpy = CP.PropsSI('H', 'T', feed_water_temperature + 273.15, 'P', feed_water_pressure * 1e5, 'Water') / 4184

        cold_reheat_enthalpy = CP.PropsSI('H', 'T', cold_reheat_temperature + 273.15, 'P', cold_reheat_pressure * 1e5, 'Water') / 4184
        hot_reheat_enthalpy = CP.PropsSI('H', 'T', hot_reheat_temperature + 273.15, 'P', hot_reheat_pressure * 1e5, 'Water') / 4184

        reheat_spray_enthalpy = CP.PropsSI('H', 'T', feed_water_temperature + 273.15, 'P', feed_water_pressure * 1e5, 'Water') / 4184

        QrMSt = ((steam_mass_flow_rate - spray_water_mass_flow_rate) * (main_steam_enthalpy - feed_water_enthalpy) + spray_water_mass_flow_rate * (main_steam_enthalpy - spray_water_enthalpy))
        QrRh = (cold_reheat_mass_flow_rate * (hot_reheat_enthalpy - cold_reheat_enthalpy) + reheat_spray_mass_flow_rate * (hot_reheat_enthalpy - reheat_spray_enthalpy))
        
        QrO = QrMSt + QrRh

        # Boiler efficiency calculation
        efficiency = 100 * (QrO / QrF)
         # Evaporation ratio (check for division by zero)
        if fuel_mass_flow_rate == 0:
            evaporation_ratio = 0
        else:
            evaporation_ratio = steam_mass_flow_rate / fuel_mass_flow_rate

        return round(QrF, 2), round(QrMSt, 2), round(QrRh, 2), round(QrO, 2), round(efficiency, 2), round(evaporation_ratio, 0)
    else:
        return None # Invalid steam type
