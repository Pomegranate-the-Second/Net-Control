from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SMeasurementAdd(BaseModel):
    device_id: int = Field(...)
    lat: float = Field(..., example=47.2333, description="Северная широта")
    lon: float = Field(..., example=38.9034, description="Восточная долгота")
    bs_num: int = Field(..., example=618946, description="Номер базовой станции")
    cell_num: int = Field(..., example=1, description="Номер сектора")
    operator: str = Field(..., example="2", max_length=10, description="Номер оператора")
    upload: float = Field(..., example=23.0, description="Скорость загрузки")
    download: float = Field(..., example=22.0, description="Скорость скачивания")
    rsrp: int = Field(..., example=-110, description="Мощность опорного сигнала")
    rssi: int = Field(..., example=-100, description="Мощность принимаемого сигнала")
    
class SMeasurement(BaseModel):
    lat: float = Field(..., example=47.2333, description="Северная широта")
    lon: float = Field(..., example=38.9034, description="Восточная долгота")
    bs_num: int = Field(..., example=618946, description="Номер базовой станции")
    cell_num: int = Field(..., example=1, description="Номер сектора")
    operator: str = Field(..., example="2", max_length=10, description="Номер оператора")
    upload: float = Field(..., example=23.0, description="Скорость загрузки")
    download: float = Field(..., example=22.0, description="Скорость скачивания")
    rsrp: int = Field(..., example=-110, description="Мощность опорного сигнала")
    rssi: int = Field(..., example=-100, description="Мощность принимаемого сигнала")

class SRectangle(BaseModel):
    up_lat: float = Field(..., example=47.211996, description="Северная широта левого верхнего угла")
    up_lon: float = Field(..., example=38.898138, description="Восточная долгота левого верхнего угла")
    down_lat: float = Field(..., example=47.207487, description="Северная широта правого нижнего угла")
    down_lon: float = Field(..., example=38.909314, description="Восточная долгота правого нижнего угла")
    dtime: Optional[datetime] = Field(..., description="Дата и время добавления измерения")

class SDevice(BaseModel):
    device_id: int = Field(...)