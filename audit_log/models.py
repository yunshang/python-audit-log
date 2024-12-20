# audit_log/models.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config import DATABASE_URL 


Base = declarative_base()
class AuditLog(Base):
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    action_type = Column(String(50))  # Specify length for VARCHAR
    resource_type = Column(String(50))  # Specify length for VARCHAR
    resource_id = Column(String(100))  # Specify length for VARCHAR
    result = Column(String(50))  # Specify length for VARCHAR
    principal_type = Column(String(50))  # Specify length for VARCHAR
    principal_authority = Column(String(100))  # Specify length for VARCHAR
    principal_id = Column(String(100))  # Specify length for VARCHAR
    request_id = Column(String(100))  # Specify length for VARCHAR
    outcome_reason = Column(String(255))  # Specify length for VARCHAR
    before = Column(String(255))  # Specify length for VARCHAR
    after = Column(String(255))  # Specify length for VARCHAR
