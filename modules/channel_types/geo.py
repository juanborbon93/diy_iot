from pydantic import BaseModel

class GeoModel(BaseModel):
    latitude:float
    longitude:float