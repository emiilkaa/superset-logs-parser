from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, mapped_column

from entity.base import Base
from entity.dashboard import Dashboard
from entity.user import User


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    action = Column(String)
    user_id = mapped_column('user_id', Integer, ForeignKey(User.id))
    json = Column(String)
    dttm = Column(DateTime(timezone=False))
    dashboard_id = mapped_column('dashboard_id', Integer, ForeignKey(Dashboard.id))
    slice_id = Column(Integer)
    duration_ms = Column(Integer)
    referrer = Column(String)

    dashboard = relationship(Dashboard, backref='dashboard', foreign_keys=[dashboard_id])
    user = relationship(User, backref='user', foreign_keys=[user_id])

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
