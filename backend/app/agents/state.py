from typing import TypedDict
class ClaimState(TypedDict,total=False):
    claim:dict;documents:list[dict];policy_text:str;extracted_documents:list[dict];retrieved_clauses:list[dict]
    policy_analysis:dict;validation:dict;risk_analysis:dict;calculation:dict;llm_assessment:dict;final_assessment:dict
