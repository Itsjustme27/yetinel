from pydantic import BaseModel

class LogEvent(BaseModel):
    timestamp: str
    source: str
    level: str
    event: str
    message: str
    source_ip:str


