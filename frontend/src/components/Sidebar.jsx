import {NavLink} from "react-router-dom";
import {ShieldCheck,LayoutDashboard,FilePlus2,Files,ClipboardCheck,Activity,Settings2,ChevronLeft} from "lucide-react";
const links=[
  ["/","Overview",LayoutDashboard],
  ["/new-claim","New claim",FilePlus2],
  ["/claims","Claims register",Files],
  ["/activity","Activity log",Activity]
];
export default function Sidebar(){
 return <aside className="sidebar">
  <div className="brand"><div className="brand-mark"><ShieldCheck size={22}/></div><div><b>claimwise<span>.</span></b><small>CLAIMS INTELLIGENCE</small></div></div>
  <div className="workspace-label">WORKSPACE</div>
  <nav>{links.map(([to,label,Icon])=><NavLink key={to} to={to} end={to==="/"} className={({isActive})=>"nav-link "+(isActive?"active":"")}><Icon size={18}/><span>{label}</span></NavLink>)}</nav>
  <div className="sidebar-bottom"><div className="sidebar-status"><i/> <span>Local workspace</span><small>DEVELOPMENT</small></div><div className="sidebar-note">AI-assisted review.<br/>Human-led decisions.</div></div>
 </aside>
}
