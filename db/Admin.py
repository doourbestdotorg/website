from sqlalchemy import String, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base


class Admin(Base):
    __tablename__ = 'admin'
    __table_args__ = {'comment': 'Admin'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    username: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'), nullable=False)
    token: Mapped[str] = mapped_column(String(64, 'utf8mb4_unicode_ci'), nullable=False)
    salt: Mapped[str] = mapped_column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='mixed code')
    failed_count: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'0'"),
                                              comment='total number of consecutive login failures')
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"),
                                        comment='account status 1.normal 0.disabled')

    def __repr__(self) -> str:
        return f"Admin(id={self.id!r}, salt={self.salt!r})"
