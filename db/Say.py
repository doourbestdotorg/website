from sqlalchemy import text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TINYINT
from sqlalchemy.orm import mapped_column, Mapped

from .Base import Base


class Say(Base):
    __tablename__ = 'say'
    __table_args__ = {'comment': 'tweets'}

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True)
    content: Mapped[str] = mapped_column(VARCHAR(2000), nullable=False)
    img: Mapped[str] = mapped_column(VARCHAR(1000), comment='image path, separated by |')
    status: Mapped[int] = mapped_column(TINYINT(1), nullable=False, comment='-1.delete 0.forbidden 1.normal')
    is_post: Mapped[int] = mapped_column(TINYINT(1), nullable=False, server_default=text("'1'"), comment='1.tweeted 0.not tweeted')
    add_time: Mapped[int] = mapped_column(INTEGER, nullable=False)
    update_time: Mapped[int] = mapped_column(INTEGER, nullable=False)