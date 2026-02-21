from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.database import Base, int_pk, float_zero, created_at


class Forecasts(Base):
    __tablename__='forecasts'
    
    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    lat: Mapped[float_zero]
    lon: Mapped[float_zero]
    bs_num: Mapped[str]
    cell_num: Mapped[str]
    operator: Mapped[str]
    upload: Mapped[float_zero]
    download: Mapped[float_zero]
    event_datetime: Mapped[created_at]

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__(self) -> str:
        return f"{self.id} - {self.operator} - {self.lat:.6f}; {self.lon:.6f}; upload: {self.upload}, download: {self.download}"