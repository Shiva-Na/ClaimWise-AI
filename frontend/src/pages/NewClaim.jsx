import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {ArrowLeft,ArrowRight,CheckCircle2,Info} from "lucide-react";
import api from "../lib/api";
export default function NewClaim(){
 const nav=useNavigate(),[form,setForm]=useState({customer_name:"",policy_number:"",insurance_type:"Health",hospital_name:"",claimed_amount:"",admission_date:"",discharge_date:"",incident_description:""});
 const [busy,setBusy]=useState(false),[error,setError]=useState("");
 const change=e=>setForm({...form,[e.target.name]:e.target.value});
 const submit=async e=>{e.preventDefault();setBusy(true);setError("");try{const r=await api.post("/claims",{...form,claimed_amount:Number(form.claimed_amount)});nav(`/claims/${r.data.id}`)}catch(err){setError(err.message)}finally{setBusy(false)}};
 return <div className="page-content narrow-page">
  <button className="back-link" onClick={()=>nav("/")}><ArrowLeft size={15}/> Back to overview</button>
  <div className="page-title-block"><div className="eyebrow">CLAIMS INTAKE / NEW RECORD</div><h1>Create a new claim</h1><p className="page-subtitle">Capture the claimant and incident details before document verification.</p></div>
  {error&&<div className="alert error">{error}</div>}
  <form className="panel form-panel" onSubmit={submit}>
   <div className="form-section-title"><span>01</span><div><h2>Policyholder details</h2><p>Identify the customer and active policy reference.</p></div></div>
   <div className="form-grid">
    <label>Customer full name <em>*</em><input required minLength="2" name="customer_name" value={form.customer_name} onChange={change} placeholder="e.g. Aditi Sharma"/></label>
    <label>Policy number <em>*</em><input required minLength="3" name="policy_number" value={form.policy_number} onChange={change} placeholder="e.g. HLT-2026-00124"/></label>
    <label>Insurance category<select name="insurance_type" value={form.insurance_type} onChange={change}><option>Health</option><option>Motor</option><option>Travel</option><option>Property</option><option>Life</option></select></label>
    <label>Hospital / service provider<input name="hospital_name" value={form.hospital_name} onChange={change} placeholder="Provider or institution name"/></label>
   </div>
   <div className="form-divider"/>
   <div className="form-section-title"><span>02</span><div><h2>Claim information</h2><p>Enter the requested amount and incident timeline.</p></div></div>
   <div className="form-grid">
    <label>Claimed amount (INR) <em>*</em><div className="input-prefix"><span>₹</span><input required type="number" min="1" step="0.01" name="claimed_amount" value={form.claimed_amount} onChange={change} placeholder="250000"/></div></label>
    <label>Admission / incident date<input name="admission_date" value={form.admission_date} onChange={change} placeholder="e.g. 10 Nov 2026"/></label>
    <label>Discharge / completion date<input name="discharge_date" value={form.discharge_date} onChange={change} placeholder="e.g. 15 Nov 2026"/></label>
   </div>
   <label className="full-label">Incident description<textarea rows="4" name="incident_description" value={form.incident_description} onChange={change} placeholder="Briefly describe the incident, treatment or loss being claimed..."/></label>
   <div className="form-note"><Info size={17}/><span>Documents can be attached after the claim record is created. Use synthetic data for portfolio demonstrations.</span></div>
   <div className="form-actions"><button type="button" className="secondary-button" onClick={()=>nav("/")}>Cancel</button><button className="primary-button" disabled={busy}>{busy?"Creating...":"Create claim record"} <ArrowRight size={16}/></button></div>
  </form>
 </div>
}
