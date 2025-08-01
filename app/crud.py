from sqlalchemy.orm import Session

from db.models import City
from schemas import CityCreateSchema


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
