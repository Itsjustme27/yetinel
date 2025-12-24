from fastapi import APIRouter
from ..db import get_logs_collection
from ..models import LogEvent

router = APIRouter()

@router.get("/logs", response_model=list[LogEvent])
def get_logs(limit: int = 50):
    logs_cursor = (
        get_logs_collection()
        .find({}, {"_id": 0})
        .sort("timestamp", -1)
        .limit(limit)
    )
    return list(logs_cursor)
