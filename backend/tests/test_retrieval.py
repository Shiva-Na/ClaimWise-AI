from app.services.retrieval import chunk_policy,retrieve_relevant_chunks
def test_chunk_policy():assert chunk_policy('Coverage includes hospitalization. Exclusions include cosmetic surgery.')
def test_retrieval():
 r=retrieve_relevant_chunks('hospitalization coverage','Hospitalisation is covered subject to terms. Cosmetic procedures are excluded.')
 assert r and 'Hospitalisation' in r[0]['chunk']
