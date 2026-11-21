import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def chunk_policy(text,chunk_size=850,overlap=120):
    clean=re.sub(r'\s+',' ',text).strip();chunks=[];start=0
    while start<len(clean):
        end=min(len(clean),start+chunk_size)
        if end<len(clean):
            boundary=clean.rfind('. ',start,end)
            if boundary>start+chunk_size//2:end=boundary+1
        chunks.append(clean[start:end].strip())
        if end>=len(clean):break
        start=max(end-overlap,start+1)
    return chunks
def retrieve_relevant_chunks(query,policy_text,top_k=4):
    chunks=chunk_policy(policy_text)
    if not chunks:return []
    vec=TfidfVectorizer(stop_words='english',ngram_range=(1,2));mat=vec.fit_transform([query]+chunks)
    scores=cosine_similarity(mat[0:1],mat[1:]).flatten();ranked=sorted(enumerate(scores),key=lambda x:x[1],reverse=True)[:top_k]
    return [{'chunk':chunks[i],'relevance':round(float(score),4),'source':f'Policy section {i+1}'} for i,score in ranked if score>0]
