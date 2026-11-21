from datetime import datetime,timezone
from sqlalchemy import String,DateTime,Float,Integer,Text,JSON,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column,relationship
from app.db.session import Base
def utcnow():return datetime.now(timezone.utc)
class Claim(Base):
    __tablename__='claims'
    id:Mapped[int]=mapped_column(primary_key=True)
    claim_ref:Mapped[str]=mapped_column(String(32),unique=True,index=True)
    customer_name:Mapped[str]=mapped_column(String(160),index=True)
    policy_number:Mapped[str]=mapped_column(String(80),index=True)
    insurance_type:Mapped[str]=mapped_column(String(40),default='Health')
    hospital_name:Mapped[str]=mapped_column(String(180),default='')
    claimed_amount:Mapped[float]=mapped_column(Float)
    admission_date:Mapped[str]=mapped_column(String(40),default='')
    discharge_date:Mapped[str]=mapped_column(String(40),default='')
    incident_description:Mapped[str]=mapped_column(Text,default='')
    status:Mapped[str]=mapped_column(String(48),default='Submitted',index=True)
    recommendation:Mapped[str]=mapped_column(String(100),default='Awaiting assessment')
    risk_score:Mapped[int]=mapped_column(Integer,default=0)
    risk_level:Mapped[str]=mapped_column(String(20),default='Not assessed')
    findings:Mapped[dict]=mapped_column(JSON,default=dict)
    report:Mapped[str]=mapped_column(Text,default='')
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow,onupdate=utcnow)
    documents:Mapped[list['ClaimDocument']]=relationship(back_populates='claim',cascade='all, delete-orphan')
    reviews:Mapped[list['HumanReview']]=relationship(back_populates='claim',cascade='all, delete-orphan')
class ClaimDocument(Base):
    __tablename__='claim_documents'
    id:Mapped[int]=mapped_column(primary_key=True)
    claim_id:Mapped[int]=mapped_column(ForeignKey('claims.id',ondelete='CASCADE'),index=True)
    filename:Mapped[str]=mapped_column(String(255));stored_path:Mapped[str]=mapped_column(String(500))
    document_type:Mapped[str]=mapped_column(String(60),default='supporting');mime_type:Mapped[str]=mapped_column(String(120),default='')
    file_size:Mapped[int]=mapped_column(Integer,default=0);extracted_text:Mapped[str]=mapped_column(Text,default='')
    extraction_status:Mapped[str]=mapped_column(String(30),default='pending');created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
    claim:Mapped[Claim]=relationship(back_populates='documents')
class HumanReview(Base):
    __tablename__='human_reviews'
    id:Mapped[int]=mapped_column(primary_key=True);claim_id:Mapped[int]=mapped_column(ForeignKey('claims.id',ondelete='CASCADE'),index=True)
    reviewer:Mapped[str]=mapped_column(String(120),default='Insurance Officer');decision:Mapped[str]=mapped_column(String(60));notes:Mapped[str]=mapped_column(Text,default='')
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow);claim:Mapped[Claim]=relationship(back_populates='reviews')
class AuditEvent(Base):
    __tablename__='audit_events'
    id:Mapped[int]=mapped_column(primary_key=True);claim_id:Mapped[int|None]=mapped_column(ForeignKey('claims.id',ondelete='SET NULL'),nullable=True,index=True)
    event_type:Mapped[str]=mapped_column(String(80),index=True);description:Mapped[str]=mapped_column(Text);actor:Mapped[str]=mapped_column(String(120),default='system')
    metadata_json:Mapped[dict]=mapped_column(JSON,default=dict);created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=utcnow)
