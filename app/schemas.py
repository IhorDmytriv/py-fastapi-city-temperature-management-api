from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class CityBaseSchema(BaseModel):
    name: str
    additional_info: Optional[str]


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityRetrieveSchema(CityBaseSchema):
    id: int

    class Config:
        from_attributes = True


class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    pass


class TemperatureRetrieveSchema(TemperatureBaseSchema):
    id: int

    class Config:
        from_attributes = True
