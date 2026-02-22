from models.measurements import Measurements
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from database.database import session_maker


class MeasurementsCRUD:
    model = Measurements
    
    @classmethod
    def add(cls, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        with session_maker() as session:
            session.add(new_instance)
            try:
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e
        return new_instance
    
    @classmethod
    def find_rectangle_measurements(cls, date: BaseModel):
        with session_maker() as session:
            query = select(cls.model).where(
                cls.model.lat.between(date.down_lat, date.up_lat),
                cls.model.lon.between(date.up_lon, date.down_lon)
            ).order_by(cls.model.id.desc())
            
            users = session.execute(query)
            return users.scalars().all()