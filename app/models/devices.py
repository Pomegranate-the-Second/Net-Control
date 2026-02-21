from sqlalchemy.orm import Mapped, relationship
from database.database import Base, int_pk, str_uniq


class Devices(Base):
    __tablename__='devices'
    
    id: Mapped[int_pk]
    imeisv: Mapped[str_uniq]

    extend_existing = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"
    
    def __str__(self) -> str:
        return f"{self.id} - {self.imeisv}"
  