from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.database import Base, int_pk, float_zero, created_at


class Measurements(Base):
    __tablename__='measurements'
    
   
    ## int cid;
    ## int pci;
    ## int rsrp;
    ## int rssi;
    
    id: Mapped[int_pk]
    device_id: Mapped[int] = mapped_column(ForeignKey("devices.id"), nullable=False)
    lat: Mapped[float_zero]
    lon: Mapped[float_zero]
    bs_num: Mapped[int] ## код региона - номер базовой
    cell_num: Mapped[int] ## номер сектора
    operator: Mapped[str] ## Mobile Network Code (MNC)
    upload: Mapped[float_zero] 
    download: Mapped[float_zero]
    rsrp: Mapped[int]
    rssi: Mapped[int]
    event_datetime: Mapped[created_at]

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__(self) -> str:
        return f"{self.id} - {self.operator} - {self.lat:.6f}; {self.lon:.6f}; upload: {self.upload}, download: {self.download}"

