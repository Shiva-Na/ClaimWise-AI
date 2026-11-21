import {Routes,Route} from "react-router-dom";
import Shell from "./components/Shell";
import Overview from "./pages/Overview";
import NewClaim from "./pages/NewClaim";
import Claims from "./pages/Claims";
import ClaimDetail from "./pages/ClaimDetail";
import Activity from "./pages/Activity";
export default function App(){
 return <Routes><Route element={<Shell/>}>
  <Route path="/" element={<Overview/>}/>
  <Route path="/new-claim" element={<NewClaim/>}/>
  <Route path="/claims" element={<Claims/>}/>
  <Route path="/claims/:id" element={<ClaimDetail/>}/>
  <Route path="/activity" element={<Activity/>}/>
  <Route path="*" element={<div className="empty-state">Page not found.</div>}/>
 </Route></Routes>
}
