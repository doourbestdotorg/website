from sqlalchemy import String
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMTEXT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base


class About(Base):
    __tablename__ = 'about'
    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    title: Mapped[str] = mapped_column(String(300, 'utf8mb4_unicode_ci'), nullable=False)
    keyword: Mapped[str] = mapped_column(String(100, 'utf8mb4_unicode_ci'))
    description: Mapped[str] = mapped_column(String(300, 'utf8mb4_unicode_ci'))
    video: Mapped[str] = mapped_column(String(300, 'utf8mb4_unicode_ci'))
    sort: Mapped[int] = mapped_column(INTEGER)
    content: Mapped[str] = mapped_column(MEDIUMTEXT, nullable=False)
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    def __repr__(self) -> str:
        return f"About(id={self.id!r}, title={self.title!r}, content={self.content!r}, status={self.status!r})"
