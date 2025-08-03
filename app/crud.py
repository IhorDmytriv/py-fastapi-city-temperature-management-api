import asyncio
from datetime import datetime
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import City, Temperature
from schemas import (
    CityCreateSchema,
    CityUpdateSchema
)
from scraper import scrape_temperature_by_city_name


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


def remove_city(db: Session, db_city: City) -> None:
    db.delete(db_city)
    db.commit()


async def create_temperatures(db: Session, cities: Sequence[City]) -> Sequence[Temperature]:
    tasks = [scrape_temperature_by_city_name(city.name) for city in cities]
    temperatures_values = await asyncio.gather(*tasks)

    db_temps = []
    for city, temp in zip(cities, temperatures_values):
        if temp is None:
            continue
        db_temps.append(
            Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temp
            )
        )

    db.add_all(db_temps)
    db.commit()
    return db_temps


def get_all_temperatures(db: Session) -> Sequence[Temperature]:
    return db.execute(select(Temperature)).scalars().all()


def get_temperatures_by_city_id(db: Session, city_id: int) -> Sequence[Temperature]:
    return db.execute(select(Temperature).where(Temperature.city_id == city_id)).scalars().all()
