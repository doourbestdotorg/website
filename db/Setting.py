from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped

from .Base import Base


class Setting(Base):
    __tablename__ = 'setting'
    __table_args__ = {'comment': 'Setting'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    key: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    value: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)