import {useEffect,useState} from "react";
import {useNavigate} from "react-router-dom";
import {Search,Plus,SlidersHorizontal,ArrowUpRight,RefreshCw} from "lucide-react";
import api from "../lib/api";
import StatusPill from "../components/StatusPill";
export default function Claims(){
 const [rows,setRows]=useState([]),[q,setQ]=useState(""),[status,setStatus]=useState("All statuses"),[err,setErr]=useState(""),[loading,setLoading]=useState(true);
 const nav=useNavigate();
 const load=async()=>{setLoading(true);try{const r=await api.get("/claims",{params:{q,status,limit:300}});setRows(r.data);setErr("")}catch(e){setErr(e.message)}finally{setLoading(false)}};
 useEffect(()=>{load()},[q,status]);
 return <div className="page-content">
  <div className="welcome-row"><div><div className="eyebrow">PORTFOLIO / CLAIM OPERATIONS</div><h1>Claims register</h1><p className="page-subtitle">Search, review and manage submitted insurance claims.</p></div><button className="primary-button" onClick={()=>nav("/new-claim")}><Plus size={17}/> New claim</button></div>
  <section className="panel register-panel">
   <div className="register-toolbar"><div className="search-box"><Search size={17}/><input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search by reference, customer or policy..."/></div><div className="filter-box"><SlidersHorizontal size={16}/><select value={status} onChange={e=>setStatus(e.target.value)}><option>All statuses</option><option>Submitted</option><option>Review Required</option><option>Ready for Review</option><option>Approved by officer</option><option>Rejected by officer</option><option>More information requested</option><option>Escalated for investigation</option></select></div><button className="icon-button light" onClick={load} title="Refresh"><RefreshCw size={16}/></button></div>
   {err&&<div className="alert error">{err}</div>}
   {loading?<div className="loading-state">Loading claims...</div>:rows.length?<div className="table-scroll"><table className="large-table"><thead><tr><th>CLAIM REFERENCE</th><th>POLICYHOLDER</th><th>TYPE</th><th>CLAIM AMOUNT</th><th>RISK</th><th>STATUS</th><th>SUBMITTED</th><th/></tr></thead><tbody>{rows.map(c=><tr key={c.id} onClick={()=>nav(`/claims/${c.id}`)}><td><b className="ref-text">{c.claim_ref}</b><small>{c.policy_number}</small></td><td>{c.customer_name}<small>{c.hospital_name||"—"}</small></td><td>{c.insurance_type}</td><td className="amount-cell">₹{c.claimed_amount.toLocaleString("en-IN")}</td><td><span className={"risk-text "+(c.risk_level||"").toLowerCase()}>{c.risk_level==="Not assessed"?"—":`${c.risk_level} · ${c.risk_score}`}</span></td><td><StatusPill status={c.status}/></td><td>{new Date(c.created_at).toLocaleDateString()}</td><td><ArrowUpRight size={16} className="muted-icon"/></td></tr>)}</tbody></table></div>:<div className="empty-state"><div className="empty-icon"><Search size={24}/></div><h3>No claims found</h3><p>Try changing your search or create a new claim record.</p><button className="primary-button" onClick={()=>nav("/new-claim")}><Plus size={16}/> Create claim</button></div>}
   <div className="table-footer"><span>Showing {rows.length} claim{rows.length===1?"":"s"}</span><span>Records are stored in your PostgreSQL database</span></div>
  </section>
 </div>
}
