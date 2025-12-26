from fastapi import FastAPI
from .routes import logs, stats, detect

app = FastAPI(title="SIEM analytics service")

app.include_router(logs.router)
app.include_router(stats.router)
app.include_router(detect.router)

@app.get('/')
def home():
    return {"status": "Python Analytics Service Running"}
