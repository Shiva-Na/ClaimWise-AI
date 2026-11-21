import {useEffect,useState} from "react";
import {useNavigate} from "react-router-dom";
import {ArrowUpRight,ArrowRight,FileCheck2,AlertTriangle,ShieldAlert,Wallet,Plus,Clock3,Activity as ActivityIcon} from "lucide-react";
import {AreaChart,Area,XAxis,YAxis,Tooltip,ResponsiveContainer,CartesianGrid} from "recharts";
import api from "../lib/api";
import StatCard from "../components/StatCard";
import StatusPill from "../components/StatusPill";

export default function Overview(){
 const [metrics,setMetrics]=useState(null),[claims,setClaims]=useState([]),[activity,setActivity]=useState([]),[err,setErr]=useState("");
 const nav=useNavigate();
 const load=async()=>{try{const [m,c,a]=await Promise.all([api.get("/metrics"),api.get("/claims?limit=6"),api.get("/activity?limit=5")]);setMetrics(m.data);setClaims(c.data);setActivity(a.data);setErr("");}catch(e){setErr(e.message)}};
 useEffect(()=>{load()},[]);
 const trend=[{day:"Mon",value:12},{day:"Tue",value:18},{day:"Wed",value:14},{day:"Thu",value:24},{day:"Fri",value:19},{day:"Sat",value:29},{day:"Sun",value:25}];
 return <div className="page-content">
  <div className="welcome-row"><div><div className="eyebrow">{new Date().toLocaleDateString("en-IN", {weekday:"long",day:"2-digit",month:"long",year:"numeric"}).toUpperCase()} · OPERATIONS</div><h1>Good evening, team.</h1><p className="page-subtitle">Here’s what’s happening across your claims workspace.</p></div><button className="primary-button" onClick={()=>nav("/new-claim")}><Plus size={17}/> Create new claim</button></div>
  {err&&<div className="alert error"><AlertTriangle size={17}/>{err} <button onClick={load}>Retry</button></div>}
  <div className="stats-grid">
   <StatCard label="Total claims" value={metrics?.total_claims??"—"} detail="All submitted claims" icon={FileCheck2} tone="blue"/>
   <StatCard label="Awaiting investigation" value={metrics?.review_required??"—"} detail="Require additional checks" icon={Clock3} tone="amber"/>
   <StatCard label="High-risk indicators" value={metrics?.high_risk??"—"} detail="Flagged for human review" icon={ShieldAlert} tone="rose"/>
   <StatCard label="Total claim value" value={metrics?`₹${(metrics.total_claim_value/100000).toFixed(1)}L`:"—"} detail="Submitted amount · INR" icon={Wallet} tone="green"/>
  </div>
  <div className="dashboard-grid">
   <section className="panel chart-panel"><div className="panel-heading"><div><h2>Claims activity</h2><p>Illustrative weekly activity view</p></div><span className="period-chip">LAST 7 DAYS</span></div>
    <div className="chart-area"><ResponsiveContainer width="100%" height="100%"><AreaChart data={trend} margin={{top:8,right:8,left:-22,bottom:0}}><defs><linearGradient id="fillBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor="#426fba" stopOpacity={.22}/><stop offset="100%" stopColor="#426fba" stopOpacity={0}/></linearGradient></defs><CartesianGrid stroke="#edf1f6" vertical={false}/><XAxis dataKey="day" axisLine={false} tickLine={false} tick={{fill:"#8a96a8",fontSize:12}}/><YAxis axisLine={false} tickLine={false} tick={{fill:"#8a96a8",fontSize:12}}/><Tooltip contentStyle={{border:"1px solid #e7ebf1",borderRadius:12,boxShadow:"0 8px 24px #172d5014"}}/><Area type="monotone" dataKey="value" stroke="#426fba" strokeWidth={2.5} fill="url(#fillBlue)"/></AreaChart></ResponsiveContainer></div>
    <div className="chart-foot"><span><i className="legend-dot"/>Claims received</span><small>Sample visual · not live historical aggregation</small></div>
   </section>
   <section className="panel workflow-panel"><div className="panel-heading"><div><h2>Review pipeline</h2><p>Current case distribution</p></div><ActivityIcon size={18} className="muted-icon"/></div>
    <div className="workflow-list">
     <div><span className="workflow-dot blue-dot"/><div><b>Submitted</b><small>New claims awaiting processing</small></div><strong>{metrics?.total_claims??"—"}</strong></div>
     <div><span className="workflow-dot amber-dot"/><div><b>Review required</b><small>Missing evidence or flagged issues</small></div><strong>{metrics?.review_required??"—"}</strong></div>
     <div><span className="workflow-dot green-dot"/><div><b>Ready for review</b><small>Initial checks completed</small></div><strong>{metrics?.ready_for_review??"—"}</strong></div>
    </div><button className="text-button" onClick={()=>nav("/claims")}>View all claims <ArrowRight size={15}/></button>
   </section>
  </div>
  <div className="bottom-grid">
   <section className="panel table-panel"><div className="panel-heading"><div><h2>Recent claims</h2><p>Latest activity in your portfolio</p></div><button className="text-button" onClick={()=>nav("/claims")}>View register <ArrowUpRight size={15}/></button></div>
    {claims.length? <div className="table-scroll"><table><thead><tr><th>CLAIM REFERENCE</th><th>CUSTOMER</th><th>CLAIM VALUE</th><th>STATUS</th><th></th></tr></thead><tbody>{claims.map(c=><tr key={c.id} onClick={()=>nav(`/claims/${c.id}`)}><td><b className="ref-text">{c.claim_ref}</b><small>{c.insurance_type} insurance</small></td><td>{c.customer_name}</td><td className="amount-cell">₹{c.claimed_amount.toLocaleString("en-IN")}</td><td><StatusPill status={c.status}/></td><td><ArrowUpRight size={15} className="muted-icon"/></td></tr>)}</tbody></table></div>:<div className="empty-inline">No claims yet. Create your first claim to get started.</div>}
   </section>
   <section className="panel activity-panel"><div className="panel-heading"><div><h2>Recent activity</h2><p>System audit trail</p></div></div>
    {activity.length?activity.map(a=><div className="activity-item" key={a.id}><span className="activity-marker"/><div><b>{a.description}</b><small>{new Date(a.created_at).toLocaleString()}</small></div></div>):<div className="empty-inline">No activity recorded yet.</div>}
   </section>
  </div>
  <div className="disclaimer-bar"><ShieldAlert size={16}/><span><b>Decision-support workspace.</b> AI findings are preliminary indicators. All claim decisions must be made by an authorized insurance professional.</span></div>
 </div>
}
