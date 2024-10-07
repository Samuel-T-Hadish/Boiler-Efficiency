from pydantic import BaseModel, Field

class BoilerEfficiencyInput(BaseModel):
    fuel_mass_flow_rate: float = Field(..., gt=0, description="Fuel mass flow rate (kg/hr)")
    feed_water_temperature: float = Field(..., gt=0, description="Feed water temperature (°C)")
    feed_water_pressure: float = Field(..., gt=0, description="Feed water pressure (bar)")
    HHV: float = Field(..., gt=0, description="Higher Heating Value of fuel (kcal/kg)")
    steam_mass_flow_rate: float = Field(..., gt=0, description="Steam mass flow rate (kg/hr)")
    steam_temperature: float = Field(..., gt=0, description="Steam temperature (°C)")
    steam_pressure: float = Field(..., gt=0, description="Steam pressure (bar)")
    steam_type: str = Field(..., description="Type of steam (Saturated/Supersaturated)")
   
    spray_water_mass_flow_rate: float = Field(..., gt=0, description="spray_water_mass_flow_rate (kg/hr)")
    cold_reheat_mass_flow_rate: float = Field(..., gt=0, description="cold_reheat_mass_flow_rate (kg/hr)")
    hot_reheat_temperature: float = Field(..., gt=0, description="hot_reheat_temperature (°C)")
    hot_reheat_pressure: float = Field(..., gt=0, description="hot_reheat_pressure(bar)")
    cold_reheat_temperature: float = Field(..., gt=0, description="cold_reheat_temperature (°C)")
    cold_reheat_pressure: float = Field(..., gt=0, description="cold_reheat_pressure (bar)")
    reheat_spray_mass_flow_rate: float = Field(..., gt=0, description="reheat_spray_mass_flow_rate (kg/hr)")

