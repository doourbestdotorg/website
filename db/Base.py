from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from config.config import config

engine = create_engine('mysql+pymysql://' + config['production'].DATABASE_USERNAME + ':' + config[
    'production'].DATABASE_PASSWORD + '@localhost:3306/' + config['production'].DATABASE_NAME + '?charset=utf8',
                       pool_size=100, pool_recycle=3600, echo=True)
sm = Session(engine)


class Base(DeclarativeBase):
    def to_dict(self):
        dict = {}
        dict.update(self.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict

