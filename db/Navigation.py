from sqlalchemy import INTEGER, VARCHAR, text
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base


class Navigation(Base):
    __tablename__ = 'navigation'
    __table_args__ = {'comment': 'Menu navigation'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    url: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    sort: Mapped[int] = mapped_column(INTEGER, nullable=False, server_default=text("'0'"))
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    # def __repr__(self) -> str:
    #     return f"Navigation(id={self.id!r}, title={self.title!r})"
