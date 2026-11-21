from fastapi import APIRouter,Depends,HTTPException,UploadFile,File,Form
from sqlalchemy.orm import Session
from sqlalchemy import desc,func
from pathlib import Path
from uuid import uuid4
from app.db.session import get_db
from app.models.entities import Claim,ClaimDocument,HumanReview,AuditEvent
from app.schemas.claims import ClaimCreate,ReviewCreate
from app.services.documents import extract_document_text,classify_document,ALLOWED
from app.services.assessment import run_assessment
from app.services.audit import record_event
from app.core.config import settings
router=APIRouter()
def serialize(x,detail=False):
 d={'id':x.id,'claim_ref':x.claim_ref,'customer_name':x.customer_name,'policy_number':x.policy_number,'insurance_type':x.insurance_type,'hospital_name':x.hospital_name,'claimed_amount':x.claimed_amount,'status':x.status,'recommendation':x.recommendation,'risk_score':x.risk_score,'risk_level':x.risk_level,'created_at':x.created_at.isoformat() if x.created_at else None}
 if detail:d.update({'admission_date':x.admission_date,'discharge_date':x.discharge_date,'incident_description':x.incident_description,'findings':x.findings or {},'report':x.report or '', 'documents':[{'id':z.id,'filename':z.filename,'document_type':z.document_type,'file_size':z.file_size,'extraction_status':z.extraction_status} for z in x.documents],'reviews':[{'id':z.id,'reviewer':z.reviewer,'decision':z.decision,'notes':z.notes,'created_at':z.created_at.isoformat()} for z in x.reviews]})
 return d
@router.get('/health')
def health(db:Session=Depends(get_db)):
 db.execute(func.now());return {'status':'ok','database':'connected','service':'ClaimWise AI'}
@router.get('/metrics')
def metrics(db:Session=Depends(get_db)):
 return {'total_claims':db.query(Claim).count(),'review_required':db.query(Claim).filter(Claim.status=='Review Required').count(),'high_risk':db.query(Claim).filter(Claim.risk_score>=50).count(),'total_claim_value':float(db.query(func.coalesce(func.sum(Claim.claimed_amount),0)).scalar() or 0),'ready_for_review':db.query(Claim).filter(Claim.status=='Ready for Review').count()}
@router.get('/claims')
def listing(q:str='',status:str='',limit:int=200,db:Session=Depends(get_db)):
 query=db.query(Claim)
 if q:
  t=f'%{q}%';query=query.filter((Claim.claim_ref.ilike(t))|(Claim.customer_name.ilike(t))|(Claim.policy_number.ilike(t)))
 if status and status!='All statuses':query=query.filter(Claim.status==status)
 return [serialize(x) for x in query.order_by(desc(Claim.created_at)).limit(min(max(limit,1),500)).all()]
@router.post('/claims',status_code=201)
def create(payload:ClaimCreate,db:Session=Depends(get_db)):
 x=Claim(claim_ref='CLM-'+uuid4().hex[:8].upper(),**payload.model_dump());db.add(x);db.flush();record_event(db,'claim_created',f'Claim {x.claim_ref} created.',x.id);db.commit();db.refresh(x);return serialize(x,True)
@router.get('/claims/{cid}')
def detail(cid:int,db:Session=Depends(get_db)):
 x=db.get(Claim,cid)
 if not x:raise HTTPException(404,'Claim not found')
 return serialize(x,True)
@router.post('/claims/{cid}/documents')
async def upload(cid:int,files:list[UploadFile]=File(...),document_type:str=Form('supporting'),db:Session=Depends(get_db)):
 x=db.get(Claim,cid)
 if not x:raise HTTPException(404,'Claim not found')
 saved=[]
 for f in files:
  suffix=Path(f.filename or '').suffix.lower()
  if suffix not in ALLOWED:raise HTTPException(415,f'Unsupported file type: {suffix}')
  content=await f.read()
  if len(content)>settings.max_upload_mb*1024*1024:raise HTTPException(413,f'{f.filename} exceeds upload limit')
  try:text=extract_document_text(f.filename or 'document.txt',content)
  except Exception as e:raise HTTPException(400,f'Unable to read {f.filename}: {e}')
  if not text.strip():raise HTTPException(422,f'No selectable text in {f.filename}; scanned PDFs require OCR.')
  name=Path(f.filename or 'document').name;typ=classify_document(name,text);typ=typ if typ!='supporting' else document_type
  folder=Path(settings.upload_dir)/x.claim_ref;folder.mkdir(parents=True,exist_ok=True);path=folder/(uuid4().hex+'_'+name);path.write_bytes(content)
  db.add(ClaimDocument(claim_id=x.id,filename=name,stored_path=str(path),document_type=typ,mime_type=f.content_type or '',file_size=len(content),extracted_text=text,extraction_status='extracted'))
  saved.append({'filename':name,'document_type':typ,'characters_extracted':len(text)})
 record_event(db,'documents_uploaded',f'{len(saved)} document(s) uploaded.',x.id,metadata={'files':saved});db.commit();return {'uploaded':saved,'count':len(saved)}
@router.post('/claims/{cid}/assess')
def assess(cid:int,policy_text:str=Form(''),db:Session=Depends(get_db)):
 x=db.get(Claim,cid)
 if not x:raise HTTPException(404,'Claim not found')
 if not x.documents:raise HTTPException(400,'Upload claim documents before assessment.')
 docs=[{'filename':d.filename,'document_type':d.document_type,'text':d.extracted_text} for d in x.documents]
 if not policy_text:policy_text='\n'.join(d.extracted_text for d in x.documents if d.document_type=='policy')
 if not policy_text:policy_text='SAMPLE POLICY DEMONSTRATION ONLY; Sum insured: INR 500000; Hospitalisation: Covered subject to policy terms and exclusions; Room rent limit: INR 5000 per day; Deductible: INR 10000 per claim; Waiting period: 30 days; Exclusions: Cosmetic procedures and non-medical expenses.'
 c={'claim_ref':x.claim_ref,'customer_name':x.customer_name,'policy_number':x.policy_number,'insurance_type':x.insurance_type,'hospital_name':x.hospital_name,'claimed_amount':x.claimed_amount,'admission_date':x.admission_date,'discharge_date':x.discharge_date,'incident_description':x.incident_description}
 try:r=run_assessment(c,docs,policy_text)
 except Exception as e:raise HTTPException(500,f'Agent workflow failed: {str(e)[:250]}')
 x.findings=r;x.risk_score=r['risk_analysis']['score'];x.risk_level=r['risk_analysis']['level'];x.recommendation=r['assessment']['recommendation'];x.status=r['assessment']['status'];x.report=r['assessment'].get('agent_summary','')+'\n'+'\n'.join('- '+z for z in r['assessment']['reasons']);record_event(db,'assessment_completed',f'Agent workflow completed for {x.claim_ref}.',x.id,metadata={'risk_score':x.risk_score});db.commit();return {'claim':serialize(x,True),'analysis':r}
@router.post('/claims/{cid}/review')
def review(cid:int,payload:ReviewCreate,db:Session=Depends(get_db)):
 allowed={'Approved by officer','Rejected by officer','More information requested','Escalated for investigation'}
 if payload.decision not in allowed:raise HTTPException(422,'Invalid officer decision')
 x=db.get(Claim,cid)
 if not x:raise HTTPException(404,'Claim not found')
 db.add(HumanReview(claim_id=x.id,reviewer=payload.reviewer,decision=payload.decision,notes=payload.notes));x.status=payload.decision;record_event(db,'human_review',f'Officer recorded: {payload.decision}',x.id,actor=payload.reviewer);db.commit();return {'message':'Officer review saved.','status':x.status}
@router.get('/claims/{cid}/report')
def report(cid:int,db:Session=Depends(get_db)):
 x=db.get(Claim,cid)
 if not x:raise HTTPException(404,'Claim not found')
 if not x.findings:raise HTTPException(404,'No assessment report exists yet')
 return {'claim_ref':x.claim_ref,'report':x.report,'findings':x.findings}
@router.get('/activity')
def activity(limit:int=30,db:Session=Depends(get_db)):
 rows=db.query(AuditEvent).order_by(desc(AuditEvent.created_at)).limit(min(max(limit,1),100)).all()
 return [{'id':x.id,'claim_id':x.claim_id,'event_type':x.event_type,'description':x.description,'actor':x.actor,'created_at':x.created_at.isoformat()} for x in rows]
