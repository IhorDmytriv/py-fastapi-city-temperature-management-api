from typing import List, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import City
from schemas import (
    CityCreateSchema,
    CityUpdateSchema
)


def check_city_by_name_in_db(db: Session, city_name: str) -> City | None:
    return db.query(City).filter(City.name == city_name).first()


def create_city(db: Session, city: CityCreateSchema) -> City:
    db_city = City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_all_cities(db: Session) -> Sequence[City]:
    return db.execute(select(City)).scalars().all()


def get_city_by_id(db: Session, city_id: int) -> City | None:
    return db.execute(select(City).where(City.id == city_id)).scalar_one_or_none()


def update_city(db: Session, db_city: City, city_update: CityUpdateSchema):
    update_data = city_update.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(db_city, key, value)

    db.commit()
    db.refresh(db_city)
    return db_city
