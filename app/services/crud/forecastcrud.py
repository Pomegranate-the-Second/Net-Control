from models.forecasts import Forecasts
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from database.database import session_maker


class ForecastsCRUD:
    model = Forecasts
    
    @classmethod
    def add(cls, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        with session_maker() as session:
            session.add(new_instance)
            try:
                session.commit()
                session.refresh(new_instance)
            except SQLAlchemyError as e:
                session.rollback()
                raise e
        return new_instance
    
    @classmethod
    def update_forecast_by_id(cls, id: BaseModel, new_upload: BaseModel, new_download: BaseModel, new_status: BaseModel):
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(id=id)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                record.upload = new_upload
                record.download = new_download
                record.status = new_status
                session.commit()
                session.refresh(record)
                return record
            except SQLAlchemyError as e:
                raise
    
    @classmethod
    def find_rectangle_measurements(cls, date: BaseModel):
        with session_maker() as session:
            query = select(cls.model).where(
                cls.model.lat.between(date.down_lat, date.up_lat),
                cls.model.lon.between(date.up_lon, date.down_lon)
            ).order_by(cls.model.id.desc())
            
            users = session.execute(query)
            return users.scalars().all()
        
    