from pydantic import BaseModel, Field

class SDeviceAdd(BaseModel):
    id: int = Field(...)
    android_id: str = Field(..., max_length=100, description="Уникальный идентификатор устройства")
    
class SDeviceAID(BaseModel):
    android_id: str = Field(..., max_length=100, description="Уникальный идентификатор устройства")