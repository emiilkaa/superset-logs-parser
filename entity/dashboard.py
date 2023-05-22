import uuid as uuid

from sqlalchemy import Column, Integer, String, DateTime, Boolean, UUID

from entity.base import Base


class Dashboard(Base):
    __tablename__ = 'dashboards'

    created_on = Column(DateTime(timezone=False))
    changed_on = Column(DateTime(timezone=False))
    id = Column(Integer, primary_key=True)
    dashboard_title = Column(String)
    position_json = Column(String)
    created_by_fk = Column(Integer)
    changed_by_fk = Column(Integer)
    css = Column(String)
    description = Column(String)
    slug = Column(String)
    json_metadata = Column(String)
    published = Column(Boolean)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    certified_by = Column(String)
    certification_details = Column(String)
    is_managed_externally = Column(Boolean)
    external_url = Column(String)
