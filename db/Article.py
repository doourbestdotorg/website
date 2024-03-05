from typing import Optional

from sqlalchemy import INTEGER, VARCHAR, text
from sqlalchemy.dialects.mysql import MEDIUMTEXT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base


class Article(Base):
    __tablename__ = 'article'
    __table_args__ = {'comment': 'Article'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    category_id: Mapped[int] = mapped_column(INTEGER, nullable=False)
    title: Mapped[str] = mapped_column(VARCHAR(300), nullable=False)
    keyword: Mapped[Optional[str]] = mapped_column(VARCHAR(100), nullable=False, server_default=text("''"))
    description: Mapped[Optional[str]] = mapped_column(VARCHAR(500), nullable=False, server_default=text("''"))
    thumbnail: Mapped[str] = mapped_column(VARCHAR(200), nullable=False)
    video: Mapped[Optional[str]] = mapped_column(VARCHAR(300), nullable=False, server_default=text("''"), comment='video path')
    content: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=False)
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    sort: Mapped[int] = mapped_column(INTEGER, nullable=False, server_default=text("'0'"))
    from_title: Mapped[str] = mapped_column(VARCHAR(100))
    from_url: Mapped[str] = mapped_column(VARCHAR(300))
    add_time: Mapped[int] = mapped_column(INTEGER, nullable=False)
    update_time: Mapped[int] = mapped_column(INTEGER, nullable=False)

    # def __repr__(self) -> str:
    #     return f"Article(id={self.id!r}, title={self.title!r})"
