from models.user import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from database.database import session_maker

class UsersCRUD:
    model = User
    
    @classmethod
    def find_all_users(cls):
        with session_maker() as session:
            query = select(User).order_by(cls.model.id.desc())
            users = session.execute(query)
            return users.scalars().all()
    
    @classmethod
    def find_one_or_none(cls, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_dict)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                return record
            except SQLAlchemyError as e:
                raise

    @classmethod
    def find_one_or_none_by_email(cls, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_dict)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                return record
            except SQLAlchemyError as e:
                raise

    @classmethod
    def find_one_or_none_by_id(cls, filters: BaseModel):
        filter_dict = filters.model_dump(exclude_unset=True)
        with session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_dict)
                result = session.execute(query)
                record = result.scalar_one_or_none()
                return record
            except SQLAlchemyError as e:
                raise
    
    @classmethod
    def add(cls, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        new_instance = cls.model(**values_dict)
        new_instance.email = new_instance.email.lower()
        with session_maker() as session:
            session.add(new_instance)
            try:
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise e
        return new_instance