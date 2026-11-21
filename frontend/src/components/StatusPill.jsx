export default function StatusPill({status}){
 const cls=(status||"submitted").toLowerCase().replaceAll(" ","-");
 return <span className={"status-pill "+cls}><i/>{status||"Submitted"}</span>
}
