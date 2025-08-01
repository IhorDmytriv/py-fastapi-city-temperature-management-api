from typing import Optional

from pydantic import BaseModel


class CityBaseSchema(BaseModel):
    name: str
    additional_info: Optional[str]


class CityCreateSchema(CityBaseSchema):
    pass


class CityRetrieveSchema(CityBaseSchema):
    id: int

    class Config:
        from_attributes = True
