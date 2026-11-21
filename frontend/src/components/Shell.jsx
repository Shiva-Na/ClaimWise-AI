import {Outlet,useLocation} from "react-router-dom";
import Sidebar from "./Sidebar";
import {Bell,Search,ChevronDown,Command} from "lucide-react";
const titles={"/":"Overview","/new-claim":"Create a claim","/claims":"Claims register","/activity":"Activity log"};
export default function Shell(){
 const loc=useLocation();
 return <div className="app-shell"><Sidebar/><main className="main-area">
  <header className="topbar"><div className="breadcrumb"><span>Workspace</span><b>/</b><strong>{titles[loc.pathname]||"Claim details"}</strong></div>
   <div className="top-actions"><div className="environment-pill"><i/> DEVELOPMENT</div><button className="icon-button" title="Notifications"><Bell size={18}/></button><div className="user-chip"><div className="avatar">IO</div><div><b>Insurance Ops</b><small>Reviewer workspace</small></div><ChevronDown size={14}/></div></div>
  </header><div className="page-wrap"><Outlet/></div>
 </main></div>
}
