from fastapi import APIRouter
from ..detection import detect_failed_logins

router = APIRouter()

@router.post("/detect/failed-logins")
def run_detection():
    detect_failed_logins()
    return {"status": "detection run"}
