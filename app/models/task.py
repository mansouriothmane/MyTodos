import uuid

from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID

# from sqlalchemy.orm import relathionship

from app.database import Base


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4
    )
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    done = Column(Boolean, default=False)
