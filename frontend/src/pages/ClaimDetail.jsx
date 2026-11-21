import {useEffect,useState} from "react";
import {useParams,useNavigate} from "react-router-dom";
import {ArrowLeft,UploadCloud,FileText,ShieldCheck,AlertTriangle,CheckCircle2,BrainCircuit,Download,Play,ChevronDown,UserCheck} from "lucide-react";
import api from "../lib/api";
import StatusPill from "../components/StatusPill";

export default function ClaimDetail(){
 const {id}=useParams(),nav=useNavigate(),[claim,setClaim]=useState(null),[error,setError]=useState(""),[files,setFiles]=useState([]),[policy,setPolicy]=useState(null),[busy,setBusy]=useState(false),[analysis,setAnalysis]=useState(null),[decision,setDecision]=useState("More information requested"),[notes,setNotes]=useState(""),[reviewer,setReviewer]=useState("Insurance Officer");
 const load=async()=>{try{const r=await api.get(`/claims/${id}`);setClaim(r.data);if(r.data.findings&&Object.keys(r.data.findings).length)setAnalysis({analysis:r.data.findings})}catch(e){setError(e.message)}};
 useEffect(()=>{load()},[id]);
 const uploadAndAssess=async()=>{
  if(!files.length){setError("Select at least one supporting document.");return}
  setBusy(true);setError("");
  try{
   const fd=new FormData();files.forEach(f=>fd.append("files",f));
   const up=await api.post(`/claims/${id}/documents`,fd,{headers:{"Content-Type":"multipart/form-data"}});
   const assessData=new FormData();
   if(policy)assessData.append("policy_text",await policy.text());
   const r=await api.post(`/claims/${id}/assess`,assessData);
   setAnalysis(r.data);setFiles([]);setPolicy(null);await load();
  }catch(e){setError(e.message)}finally{setBusy(false)}
 };
 const submitReview=async()=>{
  setBusy(true);setError("");
  try{await api.post(`/claims/${id}/review`,{reviewer,decision,notes});await load()}catch(e){setError(e.message)}finally{setBusy(false)}
 };
 const download=()=>{
  if(!claim?.findings)return;
  const blob=new Blob([JSON.stringify(claim.findings,null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob);const a=document.createElement("a");a.href=url;a.download=`${claim.claim_ref}-assessment.json`;a.click();URL.revokeObjectURL(url);
 };
 if(!claim)return <div className="page-content">{error?<div className="alert error">{error}</div>:"Loading claim..."}</div>;
 const data=analysis?.analysis||claim.findings||{},assessment=data.assessment||{},risk=data.risk_analysis||{},validation=data.validation||{},policyData=data.policy_analysis||{},calc=data.calculation||{};
 return <div className="page-content">
  <button className="back-link" onClick={()=>nav("/claims")}><ArrowLeft size={15}/> Back to claims register</button>
  {error&&<div className="alert error">{error}</div>}
  <div className="detail-heading"><div><div className="eyebrow">CLAIM FILE / {claim.claim_ref}</div><h1>{claim.customer_name}</h1><p className="page-subtitle">{claim.policy_number} <span className="bullet">·</span> {claim.insurance_type} insurance <span className="bullet">·</span> Submitted {new Date(claim.created_at).toLocaleDateString()}</p></div><div className="detail-actions"><StatusPill status={claim.status}/><button className="secondary-button" onClick={download}><Download size={15}/> Export findings</button></div></div>
  <div className="detail-summary-grid">
   <div className="detail-summary-card"><small>CLAIMED AMOUNT</small><strong>₹{claim.claimed_amount.toLocaleString("en-IN")}</strong><span>Requested amount</span></div>
   <div className="detail-summary-card"><small>RISK INDICATOR</small><strong className={risk.level==="High"?"danger-text":risk.level==="Medium"?"warning-text":""}>{claim.risk_level==="Not assessed"?"Not assessed":`${claim.risk_level} · ${claim.risk_score}/100`}</strong><span>Rule-based investigation signal</span></div>
   <div className="detail-summary-card"><small>ESTIMATED AMOUNT</small><strong>{calc.illustrative_amount_after_basic_limits!=null?`₹${calc.illustrative_amount_after_basic_limits.toLocaleString("en-IN")}`:"—"}</strong><span>Illustrative, basic limits only</span></div>
   <div className="detail-summary-card"><small>PROVIDER</small><strong className="provider-name">{claim.hospital_name||"Not specified"}</strong><span>Service provider</span></div>
  </div>
  <div className="detail-layout">
   <div className="detail-main">
    <section className="panel detail-panel"><div className="panel-heading"><div className="heading-icon"><UploadCloud size={18}/></div><div><h2>Supporting documents</h2><p>Upload claim evidence and optional policy wording.</p></div></div>
     <div className="upload-zone"><input id="claim-files" type="file" multiple accept=".pdf,.txt,.md" onChange={e=>setFiles(Array.from(e.target.files||[]))}/><label htmlFor="claim-files"><UploadCloud size={25}/><b>Choose claim documents</b><span>PDF, TXT or MD · max 20 MB per file</span></label></div>
     {files.length>0&&<div className="selected-files">{files.map((f,i)=><div key={i}><FileText size={16}/><span>{f.name}</span><small>{(f.size/1024).toFixed(0)} KB</small></div>)}</div>}
     <label className="file-secondary">Optional policy wording (TXT)<input type="file" accept=".txt" onChange={e=>setPolicy(e.target.files?.[0]||null)}/></label>
     <button className="primary-button full-button" disabled={busy||!files.length} onClick={uploadAndAssess}><Play size={16}/>{busy?"Running claim workflow...":"Upload & run AI assessment"}</button>
     <p className="microcopy">The workflow extracts text, retrieves policy clauses, validates documents and creates a review recommendation. Existing uploaded files remain attached to the claim.</p>
    </section>
    <section className="panel detail-panel"><div className="panel-heading"><div className="heading-icon purple"><BrainCircuit size={18}/></div><div><h2>Agent investigation</h2><p>Findings from the coordinated agent workflow.</p></div></div>
     {!claim.findings&&!analysis?<div className="empty-inline">No assessment has been run. Upload supporting documents to begin.</div>:<>
      <div className="recommendation-box"><div><small>WORKFLOW RECOMMENDATION</small><b>{assessment.recommendation||claim.recommendation}</b></div><StatusPill status={assessment.status||claim.status}/></div>
      <div className="finding-grid">
       <div className="finding-card"><div className="finding-title"><FileText size={16}/> Document validation</div><strong>{validation.missing_documents?.length?`${validation.missing_documents.length} missing`:"Checklist reviewed"}</strong><small>{validation.received_document_types?.length||0} document categories identified</small></div>
       <div className="finding-card"><div className="finding-title"><ShieldCheck size={16}/> Policy retrieval</div><strong>{policyData.retrieved_clauses?.length||0} relevant clauses</strong><small>Text relevance retrieval from policy wording</small></div>
       <div className="finding-card"><div className="finding-title"><AlertTriangle size={16}/> Risk indicators</div><strong>{risk.flags?.length||0} flags raised</strong><small>{risk.level||"Not assessed"} risk indicator</small></div>
       <div className="finding-card"><div className="finding-title"><CheckCircle2 size={16}/> Basic calculation</div><strong>{calc.illustrative_amount_after_basic_limits!=null?`₹${calc.illustrative_amount_after_basic_limits.toLocaleString("en-IN")}`:"Not available"}</strong><small>After basic sum insured cap and deductible</small></div>
      </div>
      <div className="accordion-list">
       <details open><summary>Investigation findings <ChevronDown size={16}/></summary>{(assessment.reasons||risk.flags||[]).length?<ul>{(assessment.reasons||risk.flags||[]).map((x,i)=><li key={i}>{x}</li>)}</ul>:<p>No configured rule flags were raised. Human verification remains required.</p>}</details>
       <details><summary>Policy evidence & retrieved clauses <ChevronDown size={16}/></summary>{(policyData.retrieved_clauses||[]).map((x,i)=><blockquote key={i}><p>{x.chunk}</p><small>{x.source} · relevance {x.relevance}</small></blockquote>)}{!policyData.retrieved_clauses?.length&&<p>No policy clauses were retrieved.</p>}</details>
       <details><summary>Document extraction <ChevronDown size={16}/></summary>{(data.document_analysis||[]).map((d,i)=><div className="extracted-row" key={i}><b>{d.filename}</b><span>{d.document_type}</span><pre>{JSON.stringify(d.fields,null,2)}</pre></div>)}</details>
       <details><summary>LLM analyst explanation <ChevronDown size={16}/></summary>{data.llm_assessment?.enabled?<><p>{data.llm_assessment.summary}</p><pre>{JSON.stringify(data.llm_assessment,null,2)}</pre></>:<p>{data.llm_assessment?.summary||"LLM is not configured. Deterministic findings are available."}</p>}</details>
      </div>
      <div className="disclaimer-bar"><AlertTriangle size={16}/><span>{risk.disclaimer||"All findings are preliminary. They are not proof of fraud or a claim decision."}</span></div>
     </>}
    </section>
   </div>
   <aside className="detail-side">
    <section className="panel detail-panel"><div className="panel-heading"><div className="heading-icon green"><UserCheck size={18}/></div><div><h2>Officer review</h2><p>Record the authorized human decision.</p></div></div>
     <label>Reviewer name<input value={reviewer} onChange={e=>setReviewer(e.target.value)}/></label>
     <label>Decision<select value={decision} onChange={e=>setDecision(e.target.value)}><option>More information requested</option><option>Escalated for investigation</option><option>Approved by officer</option><option>Rejected by officer</option></select></label>
     <label>Review notes<textarea rows="4" value={notes} onChange={e=>setNotes(e.target.value)} placeholder="Document rationale and next steps..."/></label>
     <button className="primary-button full-button" disabled={busy} onClick={submitReview}>Save officer review</button>
     {claim.reviews?.length>0&&<div className="review-history"><b>Previous reviews</b>{claim.reviews.map(r=><div key={r.id}><strong>{r.decision}</strong><small>{r.reviewer} · {new Date(r.created_at).toLocaleString()}</small><p>{r.notes}</p></div>)}</div>}
    </section>
    <section className="panel detail-panel"><h2>Claim details</h2><dl className="detail-dl"><dt>Admission / incident</dt><dd>{claim.admission_date||"—"}</dd><dt>Discharge / completion</dt><dd>{claim.discharge_date||"—"}</dd><dt>Hospital / provider</dt><dd>{claim.hospital_name||"—"}</dd></dl>{claim.incident_description&&<p className="incident-text">{claim.incident_description}</p>}</section>
   </aside>
  </div>
 </div>
}
