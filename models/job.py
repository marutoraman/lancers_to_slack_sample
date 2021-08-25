import json
from sqlalchemy import Column, String,Text , Float, Integer, DateTime, Date, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import delete
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean
from common.database import Base, get_ulid
from sqlalchemy.sql.functions import current_timestamp
from datetime import datetime as dt


class Job(Base):
    __tablename__ = 'job'
    mysql_charset = 'utf8mb4',
    mysql_collate = 'utf8mb4_unicode_ci'

    id = Column(String(32), primary_key=True, default=get_ulid)
    title = Column(String(128), nullable=True)
    work_id = Column(String(128), nullable=False)
    price_min = Column(Integer, nullable=True)
    price_max = Column(Integer, nullable=True)
    proposales_number = Column(Integer, nullable=True)
    client_id = Column(String(16), nullable=True)
    
    description = Column(Text, nullable=True)
    start_at = Column(DateTime, nullable=True) # 開始日時
    end_at = Column(DateTime, nullable=True) # 締め切り日時
    desired_delivery_at = Column(DateTime, nullable=True) # 希望納期

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
