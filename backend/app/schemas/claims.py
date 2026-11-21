from pydantic import BaseModel,Field
class ClaimCreate(BaseModel):
    customer_name:str=Field(min_length=2,max_length=160);policy_number:str=Field(min_length=3,max_length=80)
    insurance_type:str=Field(default='Health',max_length=40);hospital_name:str=Field(default='',max_length=180)
    claimed_amount:float=Field(gt=0,le=100000000);admission_date:str='';discharge_date:str='';incident_description:str=''
class ReviewCreate(BaseModel):
    reviewer:str='Insurance Officer';decision:str;notes:str=''
