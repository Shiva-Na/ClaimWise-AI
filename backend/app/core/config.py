from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
class Settings(BaseSettings):
    app_name:str='ClaimWise AI'
    database_url:str='postgresql+psycopg://postgres:postgres@localhost:5432/claimwise'
    openai_api_key:str=''
    openai_model:str='gpt-4o-mini'
    cors_origins:str='http://localhost:5173'
    upload_dir:str='storage/uploads'
    max_upload_mb:int=20
    model_config=SettingsConfigDict(env_file='.env',extra='ignore')
    @property
    def origins(self): return [x.strip() for x in self.cors_origins.split(',') if x.strip()]
settings=Settings();Path(settings.upload_dir).mkdir(parents=True,exist_ok=True)
