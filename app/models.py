from .database import Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, INTEGER
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE, UUIDTypeDecorator
import uuid
from uuid import UUID, uuid4

from sqlalchemy.types import TypeDecorator, CHAR
#from sqlalchemy.dialects.postgresql import UUID


# class GUID(TypeDecorator):
#     """Platform-independent GUID type.
#     Uses PostgreSQL's UUID type, otherwise uses
#     CHAR(32), storing as stringified hex values.
#     """
#     impl = CHAR

#     def load_dialect_impl(self, dialect):
#         if dialect.name == 'postgresql':
#             return dialect.type_descriptor(UUID())
#         else:
#             return dialect.type_descriptor(CHAR(32))

#     def process_bind_param(self, value, dialect):
#         if value is None:
#             return value
#         elif dialect.name == 'postgresql':
#             return str(value)
#         else:
#             if not isinstance(value, uuid.UUID):
#                 return "%.32x" % uuid.UUID(value).int
#             else:
#                 # hexstring
#                 return "%.32x" % value.int

#     def process_result_value(self, value, dialect):
#         if value is None:
#             return value
#         else:
#             if not isinstance(value, uuid.UUID):
#                 value = uuid.UUID(value)
#             return value

class GUID(TypeDecorator):
    """GUID column."""
 
    impl = CHAR
 
    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))
 
    def process_bind_param(self, value, dialect):
        if not isinstance(value, uuid.UUID):
            try:
                return '%.32x' % int(uuid.UUID(value))
            except ValueError:
                return None
        else:
            return '%.32x' % int(value)
 
    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)
 
    @staticmethod
    def gen_value():
        return uuid.uuid4()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    phonenumber = Column(String, nullable=False)
    phonenumber_ext = Column(String, nullable=False)
    phonenumber_home = Column(String, nullable=False)
    category = Column(String, nullable=True)
    #published = Column(Boolean, nullable=False, default=True)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())

class Call(Base):
    __tablename__ = 'calls'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    number = Column(String, nullable=False)
    category = Column(String, nullable=True)        # chould be SPAM or Daniele, Papà
    receivedOn = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
