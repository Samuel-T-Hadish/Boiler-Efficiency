def Boiler():
    '''Boiler Efficiency Calculation based on Direct method as Per ASME PTC 4
        '''
print(Boiler.__doc__)   
Boiler()

import CoolProp.CoolProp as CP




Parameter_dict={ 'fuel_mass_flow_rate' : 3, # kg/hr 
            'HHVF': 4000, # kcal/kg
            'main_steam_mass_flow_rate' : 12, # kg/hr 
            'main_steam_enthalpy' : CP.PropsSI('H', 'T', 220+273.15, 'P', 15e5, 'Water')/4184,  #H: kcal/kg, T: K, P: Pa
            'feed_water_enthalpy' : CP.PropsSI('H', 'T', 95+273.15, 'P', 1.8e5, 'Water')/4184, # H: kcal/kg, T: K, P: Pa
            'spray_water_mass_flow_rate' : 1.5, # kg/hr 
            'spray_water_enthalpy' : CP.PropsSI('H', 'T', 95+273.15, 'P', 1.8e5, 'Water')/4184, # H: kcal/kg, T: K, P: Pa
            'cold_reheat_steam_mass_flow_rate' : 1.2, # kg/hr 
            'cold_reheat_steam_enthalpy' : CP.PropsSI('H', 'T', 300+273.15, 'P', 2.544e5, 'Water')/4184, # H: kcal/kg, T: K, P: Pa
            'hot_reheat_steam_enthalpy' : CP.PropsSI('H', 'T', 550+273.15, 'P',  2.517e5, 'Water')/4184, # H: kcal/kg, T: K, P: Pa
            'reheat_spray_mass_flow_rate' : 0.8,  # kg/hr 
            'reheat_spray_enthalpy' : CP.PropsSI('H', 'T', 95+273.15, 'P', 1.8e5, 'Water')/4184, # H: kcal/kg, T: K, P: Pa
            'blowdown_steam_mass_flow_rate' : 0.3, # kg/hr 
            'blowdown_steam_enthalpy' : CP.PropsSI('H', 'T', 495+273.15, 'P', 2.5e5, 'Water')/4184,  # H: kcal/kg, T: K, P: Pa
            
}


def energy_input_from_fuel(fuel_mass_flow_rate, HHVF, d_p = 2):
    """
    - Calculate the energy input from the fuel.

    - This function computes the energy input (in terms of heat) from the fuel based on the fuel mass flow rate and the higher heating value (HHV) of the fuel.

    Args:
        fuel_mass_flow_rate (float): The mass flow rate of the fuel in kg/hr.
        HHVF (float): The higher heating value of the fuel in J/kg.

    Returns:
        float: The total energy input from the fuel in Joules per hour.
    """
    QrF = fuel_mass_flow_rate * HHVF/fuel_mass_flow_rate
    return round(QrF, d_p)

QrF = energy_input_from_fuel(Parameter_dict['fuel_mass_flow_rate'], Parameter_dict['HHVF'])
print(f"Heat input through fuel: {QrF} kcal/kg")


def energy_output_main_steam(main_steam_mass_flow_rate,spray_water_mass_flow_rate, main_steam_enthalpy, feed_water_enthalpy, spray_water_enthalpy, d_p = 2):
    """
    - Calculate the energy output from the main steam.

    - This function computes the energy output of the main steam, considering the effect of spray water used for temperature control. The calculation is based on the mass flow rates and enthalpies of the main steam, feed water, and spray water.

    Args:
        main_steam_mass_flow_rate (float): The mass flow rate of the main steam in kg/hr.
        spray_water_mass_flow_rate (float): The mass flow rate of the spray water in kg/hr.
        main_steam_enthalpy (float): The enthalpy of the main steam in J/kg.
        feed_water_enthalpy (float): The enthalpy of the feed water in J/kg.
        spray_water_enthalpy (float): The enthalpy of the spray water in J/kg.

    Returns:
        float: The total energy output from the main steam in Joules per hour.
    """
    QrMSt = ((main_steam_mass_flow_rate - spray_water_mass_flow_rate )* (main_steam_enthalpy - feed_water_enthalpy) + spray_water_mass_flow_rate* (main_steam_enthalpy - spray_water_enthalpy))/Parameter_dict['fuel_mass_flow_rate']
    return round(QrMSt, d_p)

QrMSt = energy_output_main_steam(Parameter_dict['main_steam_mass_flow_rate'],Parameter_dict['spray_water_mass_flow_rate'], Parameter_dict['main_steam_enthalpy'], Parameter_dict['feed_water_enthalpy'], Parameter_dict['spray_water_enthalpy'])
print(f"Heat output through main steam: {QrMSt} kcal/kg")


def energy_output_reheat_steam(cold_reheat_steam_mass_flow_rate, hot_reheat_steam_enthalpy, cold_reheat_steam_enthalpy, reheat_spray_mass_flow_rate, reheat_spray_enthalpy, d_p = 2):
    """
    - Calculate the energy output from the reheat steam.

    - This function computes the energy output of the reheat steam, taking into account both the energy contribution from the reheating process and the effect of spray water used for temperature control.

    Args:
        cold_reheat_steam_mass_flow_rate (float): The mass flow rate of the cold reheat steam in kg/hr.
        hot_reheat_steam_enthalpy (float): The enthalpy of the hot reheat steam in J/kg.
        cold_reheat_steam_enthalpy (float): The enthalpy of the cold reheat steam in J/kg.
        spray_water_mass_flow_rate (float): The mass flow rate of the spray water in kg/hr.
        spray_water_enthalpy (float): The enthalpy of the spray water in J/kg.

    Returns:
        float: The total energy output from the reheat steam in Joules per hour.
    """
    QrRh = (cold_reheat_steam_mass_flow_rate * (hot_reheat_steam_enthalpy - cold_reheat_steam_enthalpy) + reheat_spray_mass_flow_rate * (hot_reheat_steam_enthalpy - reheat_spray_enthalpy))/Parameter_dict['fuel_mass_flow_rate']
    return round(QrRh, d_p)

QrRh = energy_output_reheat_steam(Parameter_dict['cold_reheat_steam_mass_flow_rate'], Parameter_dict['hot_reheat_steam_enthalpy'], Parameter_dict['cold_reheat_steam_enthalpy'], Parameter_dict['reheat_spray_mass_flow_rate'], Parameter_dict['reheat_spray_enthalpy'])
print(f"Heat output through reheat steam: {QrRh} kcal/kg")


def energy_output_blowdown_steam(blowdown_steam_mass_flow_rate, blowdown_steam_enthalpy, feed_water_enthalpy, d_p = 2):
    """
    - Calculate the energy output from the blowdown steam.

    - This function computes the energy output associated with the blowdown steam, which is released from the boiler to remove impurities. The calculation is based on the mass flow rate of the blowdown steam and the difference in enthalpy between the blowdown steam and the feed water.

    Args:
        blowdown_steam_mass_flow_rate (float) : The mass flow rate of the blowdown steam in kg/hr.
        blowdown_steam_enthalpy (float) : The enthalpy of the blowdown steam in J/kg.
        feed_water_enthalpy (float) : The enthalpy of the feed water in J/kg.

    Returns:
        float: The total energy output from the blowdown steam in Joules per hour.
    """
    QrBd = (blowdown_steam_mass_flow_rate * (blowdown_steam_enthalpy - feed_water_enthalpy))/Parameter_dict['fuel_mass_flow_rate']
    return round(QrBd, d_p)

# Calculate energy output
QrBd = energy_output_blowdown_steam(Parameter_dict['blowdown_steam_mass_flow_rate'], Parameter_dict['blowdown_steam_enthalpy'], Parameter_dict['feed_water_enthalpy'])
print(f"Heat output through blowdown steam: {QrBd} kcal/kg")


# Calculate total energy output of the boiler
def Energy_Output():
    """
    - Calculate the total energy output from various steam sources.

    - This function computes the total energy output by summing the energy outputs from the main steam, reheat steam, auxiliary steam, and blowdown steam. The individual energy outputs from these sources are assumed to be defined as `QrMSt`, `QrRh`, `QrAxSt`, and `QrBd` respectively.

    Returns:
        None
        This function does not return a value. It prints the total energy output directly.

     
    """
QrO = (QrMSt + QrRh + QrBd)
print (f"Total Heat output: {QrO: .2f} kcal/kg")



def efficiency_by_direct_method(QrO, QrF, d_p = 2):
    """
    - Calculate the efficiency of a steam generator using the direct method.

    - This function computes the efficiency of a steam generator by comparing the energy output (`QrO`) to the energy input from the fuel (`QrF`). The efficiency is expressed as a percentage.

    Args:
        QrO (float): The total energy output from the steam generator in Joules per hour.
        QrF (float): The total energy input from the fuel in Joules per hour.

    Returns:
        efficiency (float): The efficiency of the steam generator as a percentage.

    """
    #print(efficiency_by_direct_method.__doc__)
    EF = 100*(QrO/QrF)
    return round(EF, d_p)

# Calculating Efficiency by Energy Balance Method
EF = efficiency_by_direct_method(QrO, QrF)
print(f"Fuel Efficiency by direct method: {EF} %")
Evaporation_ratio = Parameter_dict['main_steam_mass_flow_rate'] / Parameter_dict['fuel_mass_flow_rate']
print(f"Evaporation_ration: {Evaporation_ratio: .2f} ")



print(f"main_steam_enthalpy: {Parameter_dict['main_steam_enthalpy']: .2f} kcal/kg")
print(f"feed_water_enthalpy: {Parameter_dict['feed_water_enthalpy']: .2f}kcal/kg")
print(f"spray_water_enthalpy: {Parameter_dict['spray_water_enthalpy']: .2f} kcal/kg")
print(f"cold_reheat_steam_enthalpy: {Parameter_dict['cold_reheat_steam_enthalpy']: .2f} kcal/kg")
print(f"hot_reheat_steam_enthalpy: {Parameter_dict['hot_reheat_steam_enthalpy']: .2f} kcal/kg")
print(f"reheat_spray_enthalpy: {Parameter_dict['reheat_spray_enthalpy']: .2f} kcal/kg")
print(f"blowdown_steam_enthalpy: {Parameter_dict['blowdown_steam_enthalpy']: .2f} kcal/kg")

