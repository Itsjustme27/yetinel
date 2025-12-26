from pydantic import BaseModel
from datetime import datetime

class LogEvent(BaseModel):
    timestamp: datetime 
    source: str
    level: str
    event: str
    message: str
    source_ip:str


