from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import (
    create_city,
    check_city_by_name_in_db,
    get_all_cities,
    get_city_by_id,
    update_city,
    remove_city,
    get_all_temperatures, get_temperatures_by_city_id
)
from app.db.database import get_db
from app.schemas import (
    MessageSchema,
    CityCreateSchema,
    CityListSchema,
    CityRetrieveSchema,
    CityUpdateSchema,
    TemperatureListSchema
)

app = FastAPI()


@app.post("/cities/", response_model=CityListSchema)
def add_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    if check_city_by_name_in_db(db=db, city_name=city.name):
        raise HTTPException(status_code=400, detail="City already exists")
    return create_city(db, city)


@app.get("/cities/", response_model=List[CityListSchema])
def list_cities(db: Session = Depends(get_db)):

    cities = get_all_cities(db=db)
    if not cities:
        raise HTTPException(status_code=404, detail="Cities not found")
    return cities


@app.get("/cities/{city_id}", response_model=CityRetrieveSchema)
def retrieve_city(city_id: int, db: Session = Depends(get_db)):
    city = get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=CityListSchema)
def edit_city(city_id: int, city_update: CityUpdateSchema, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return update_city(db=db, db_city=db_city, city_update=city_update)


@app.delete("/cities/{city_id}", response_model=MessageSchema)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    db_city = get_city_by_id(db=db, city_id=city_id)
    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    remove_city(db, db_city)
    return MessageSchema(message=f"City {db_city.name} was successfully removed!")


@app.get("/temperatures/", response_model=List[TemperatureListSchema])
def list_temperatures(db: Session = Depends(get_db)):
    temperatures = get_all_temperatures(db=db)

    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")
    return temperatures


@app.get("/temperatures/{city_id}", response_model=List[TemperatureListSchema])
def retrieve_temperature(city_id: int, db: Session = Depends(get_db)):
    city_temperatures = get_temperatures_by_city_id(db=db, city_id=city_id)

    if not city_temperatures:
        raise HTTPException(status_code=404, detail="Temperatures not found")

    return city_temperatures
