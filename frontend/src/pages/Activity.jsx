import {useEffect,useState} from "react";
import {Activity as ActivityIcon,FilePlus2,UploadCloud,BrainCircuit,UserCheck,RefreshCw} from "lucide-react";
import api from "../lib/api";
const icons={claim_created:FilePlus2,documents_uploaded:UploadCloud,assessment_completed:BrainCircuit,human_review:UserCheck};
export default function Activity(){
 const [items,setItems]=useState([]),[error,setError]=useState("");
 const load=async()=>{try{const r=await api.get("/activity?limit=100");setItems(r.data);setError("")}catch(e){setError(e.message)}};
 useEffect(()=>{load()},[]);
 return <div className="page-content"><div className="welcome-row"><div><div className="eyebrow">SYSTEM / AUDIT TRAIL</div><h1>Activity log</h1><p className="page-subtitle">A chronological record of claim operations and reviewer actions.</p></div><button className="secondary-button" onClick={load}><RefreshCw size={15}/> Refresh</button></div>
  {error&&<div className="alert error">{error}</div>}
  <section className="panel activity-log-panel">{items.length?items.map(x=>{const Icon=icons[x.event_type]||ActivityIcon;return <div className="log-row" key={x.id}><div className="log-icon"><Icon size={17}/></div><div className="log-content"><b>{x.description}</b><p>{x.actor} · {x.event_type.replaceAll("_"," ")}</p></div><time>{new Date(x.created_at).toLocaleString()}</time></div>}):<div className="empty-state"><ActivityIcon size={25}/><h3>No activity recorded</h3><p>Claim creation, uploads, assessments and officer reviews will appear here.</p></div>}</section>
 </div>
}
