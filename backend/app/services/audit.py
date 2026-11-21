from app.models.entities import AuditEvent
def record_event(db,event_type,description,claim_id=None,actor='system',metadata=None):
    db.add(AuditEvent(claim_id=claim_id,event_type=event_type,description=description,actor=actor,metadata_json=metadata or {}))
