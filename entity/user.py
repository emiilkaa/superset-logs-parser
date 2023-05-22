from sqlalchemy import Column, Integer, String, DateTime, Boolean

from entity.base import Base


class User(Base):
    __tablename__ = 'ab_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)
    password = Column(String)
    active = Column(Boolean)
    email = Column(String)
    last_login = Column(DateTime(timezone=False))
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime(timezone=False))
    changed_on = Column(DateTime(timezone=False))
    created_by_fk = Column(Integer)
    changed_by_fk = Column(Integer)
