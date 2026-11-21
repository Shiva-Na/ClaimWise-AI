from app.agents.nodes import policy_node,calculation_node,validation_node
def test_policy_parse():
 r=policy_node({'claim':{'claimed_amount':100000},'policy_text':'Sum insured: INR 500000\nDeductible: INR 10000','retrieved_clauses':[{'chunk':'Hospitalization covered','relevance':.5}]})
 assert r['policy_analysis']['sum_insured']==500000 and r['policy_analysis']['deductible']==10000
def test_calculation():
 r=calculation_node({'claim':{'claimed_amount':300000},'policy_analysis':{'sum_insured':500000,'deductible':10000}})
 assert r['calculation']['illustrative_amount_after_basic_limits']==290000
def test_missing_docs():
 r=validation_node({'extracted_documents':[],'claim':{'customer_name':'Test','policy_number':'P-1'}})
 assert 'hospital_bill' in r['validation']['missing_documents']
