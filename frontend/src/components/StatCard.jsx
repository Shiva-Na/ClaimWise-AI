export default function StatCard({label,value,detail,icon:Icon,tone="blue"}){
 return <div className="stat-card"><div className={"stat-icon "+tone}><Icon size={19}/></div><div className="stat-copy"><span>{label}</span><strong>{value}</strong><small>{detail}</small></div></div>
}
