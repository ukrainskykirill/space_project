import datetime
from enum import Enum

import pydantic
from pydantic import BaseModel

day = str(datetime.date.today())


class Extra(str, Enum):
    ignore = 'ignore'


class EstimatedDiameter(BaseModel):
    kilometers: dict


class AsteroidInfo(BaseModel):
    name: str
    nasa_jpl_url: str
    estimated_diameter: EstimatedDiameter
    is_potentially_hazardous_asteroid: bool
    close_approach_data: list

    class Config:
        extra = Extra.ignore


class NearEarthObjects(BaseModel):
    day: list[AsteroidInfo] = pydantic.Field(alias=day)

    class Config:
        extra = Extra.ignore


class AsteroidsData(BaseModel):
    element_count: int
    near_earth_objects: NearEarthObjects

    class Config:
        extra = Extra.ignore
