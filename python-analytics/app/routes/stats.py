from fastapi import APIRouter
from ..db import get_logs_collection

router = APIRouter()

@router.get("/stats")
def get_stats():
    collection = get_logs_collection()

    total_logs = collection.count_documents({})

    by_level = list(collection.aggregate([
        {"$group": {"_id": "$level", "count": {"$sum": 1}}}
    ]))

    by_source = list(collection.aggregate([
        {"$group": {"_id": "$source", "count": {"$sum": 1}}}
    ]))

    return {
        "total_logs": total_logs,
        "by_level": by_level,
        "by_source": by_source
    }
