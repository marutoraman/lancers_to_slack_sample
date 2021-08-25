import json
from sqlalchemy import Column, String,Text , Float, Integer, DateTime, Date, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from common.database import Base, get_ulid
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime as dt


class Client(Base):
    __tablename__ = 'client'
    mysql_charset = 'utf8mb4',
    mysql_collate = 'utf8mb4_unicode_ci'

    id = Column(String(32), primary_key=True, default=get_ulid)
    client_id = Column(String(64), nullable=False)
    username = Column(String(128), nullable=True)
    profile = Column(Text, nullable=True)
    star_rate = Column(Float, nullable=True)
    orders_number = Column(Integer, nullable=True)
    order_rate = Column(Float, nullable=True)
    registed_at = Column(DateTime, nullable=True)
    industry = Column(String(32), nullable=True)

    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=current_timestamp(), onupdate=func.utc_timestamp())


    def to_dict(self):
        return self.__dict__.copy()

    def merge(self, insrtance):
        for key, value in insrtance.to_dict().items():
            if key == "id":
                continue
            if value == None:
                continue
            self.__dict__[key] = value
