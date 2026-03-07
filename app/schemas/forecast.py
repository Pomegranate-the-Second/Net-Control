from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SForecastAdd(BaseModel):
    """ Схема для добавления данных в таблицу forecasts """
    user_id: int = Field(...)
    lat: float = Field(..., example=47.2333, description="Северная широта")
    lon: float = Field(..., example=38.9034, description="Восточная долгота")
    operator: str = Field(..., example="2", max_length=10, description="Номер оператора")
    
class SForecast(BaseModel):
    """ Схема для валидации данных при добавлении прогнозируемой точки """
    lat: float = Field(..., example=47.2333, description="Северная широта")
    lon: float = Field(..., example=38.9034, description="Восточная долгота")
    operator: str = Field(..., example="2", max_length=10, description="Номер оператора")
    
class SRectangle(BaseModel):
    up_lat: float = Field(..., example=47.211996, description="Северная широта левого верхнего угла")
    up_lon: float = Field(..., example=38.898138, description="Восточная долгота левого верхнего угла")
    down_lat: float = Field(..., example=47.207487, description="Северная широта правого нижнего угла")
    down_lon: float = Field(..., example=38.909314, description="Восточная долгота правого нижнего угла")
    dtime: Optional[datetime] = Field(..., description="Дата и время добавления измерения")