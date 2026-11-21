from app.agents.nodes import workflow
def run_assessment(claim,documents,policy_text):
    x=workflow.invoke({'claim':claim,'documents':documents,'policy_text':policy_text})
    return {'document_analysis':x.get('extracted_documents',[]),'policy_analysis':x.get('policy_analysis',{}),'retrieval':x.get('retrieved_clauses',[]),'validation':x.get('validation',{}),'risk_analysis':x.get('risk_analysis',{}),'calculation':x.get('calculation',{}),'llm_assessment':x.get('llm_assessment',{}),'assessment':x.get('final_assessment',{})}
