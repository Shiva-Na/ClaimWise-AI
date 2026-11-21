from pathlib import Path
import re,fitz
ALLOWED={'.pdf','.txt','.md'}
def extract_document_text(filename,content):
    ext=Path(filename).suffix.lower()
    if ext=='.pdf':
        with fitz.open(stream=content,filetype='pdf') as pdf:return '\n'.join(p.get_text('text') for p in pdf)
    if ext in {'.txt','.md'}:return content.decode('utf-8',errors='replace')
    raise ValueError('Upload PDF, TXT or MD files only.')
def extract_structured_fields(text):
    def m(p):
        x=re.search(p,text,re.I|re.M);return x.group(1).strip() if x else None
    amounts=[]
    for x in re.findall(r'(?:₹|INR|Rs\.?\s*)\s*([\d,]+(?:\.\d{1,2})?)',text,re.I):
        try:amounts.append(float(x.replace(',','')))
        except ValueError:pass
    return {'patient_name':m(r'(?:patient|member|customer)\s*name\s*[:\-]\s*(.+)'),
      'hospital_name':m(r'hospital\s*name\s*[:\-]\s*(.+)'),
      'policy_number':m(r'policy\s*(?:number|no\.?|#)\s*[:\-]\s*([A-Z0-9\-/]+)'),
      'admission_date':m(r'admission\s*date\s*[:\-]\s*(.+)'),
      'discharge_date':m(r'discharge\s*date\s*[:\-]\s*(.+)'), 'amounts_found':amounts,'text_characters':len(text)}
def classify_document(filename,text):
    v=(filename+' '+text[:2000]).lower();rules={'claim_form':['claim form','claim application'],'hospital_bill':['hospital bill','final bill','invoice','bill total'],'discharge_summary':['discharge summary','discharge diagnosis'],'medical_report':['medical report','lab report','diagnostic report'],'policy':['policy wording','sum insured','policy schedule','insurance policy'],'identity':['aadhaar','passport','identity proof']}
    for typ,words in rules.items():
        if any(k in v for k in words):return typ
    return 'supporting'
