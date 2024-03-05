from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from .Base import Base


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'comment': 'Category'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(100), nullable=False)
    list_style: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    sort: Mapped[int] = mapped_column(INTEGER(4), nullable=False, server_default=text("'0'"))
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, comment='0.disabled 1.normal')

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, title={self.title!r}, status={self.status!r})"
