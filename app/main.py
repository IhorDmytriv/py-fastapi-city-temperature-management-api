from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import (
    create_city,
    check_city_by_name_in_db
)
from app.db.database import get_db
from app.schemas import (
    CityListSchema,
    CityCreateSchema
)

app = FastAPI()


@app.post("/cities/", response_model=CityListSchema)
def add_city(city: CityCreateSchema, db: Session = Depends(get_db)):
    if check_city_by_name_in_db(db=db, city_name=city.name):
        raise HTTPException(status_code=400, detail="City already exists")
    return create_city(db, city)
