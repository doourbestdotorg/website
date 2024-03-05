from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from .Base import Base


class Record(Base):
    __tablename__ = 'record'
    __table_args__ = {'comment': 'Backend login record'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    ip: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    content: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    add_time: Mapped[int] = mapped_column(INTEGER, nullable=False)
    update_time: Mapped[int] = mapped_column(INTEGER, nullable=False)