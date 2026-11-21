from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base,engine
from app.models import entities
from app.api.routes import router
app=FastAPI(title=settings.app_name,version='1.0.0',description='Multi-agent insurance claims decision-support platform.')
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router,prefix='/api')
@app.on_event('startup')
def startup():Base.metadata.create_all(bind=engine)
@app.get('/')
def root():return {'name':settings.app_name,'docs':'/docs','api':'/api'}
