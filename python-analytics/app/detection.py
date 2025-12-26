from datetime import datetime, timedelta
from .db import get_logs_collection, get_alerts_collection

def detect_failed_logins():
    logs_col = get_logs_collection()
    alerts_col = get_alerts_collection()

    one_min_ago = datetime.utcnow() - timedelta(days=3)

    pipeline = [
        {
            "$match": {
                "event": "login_failed",
                "timestamp": { "$gte": one_min_ago }
            }
        },
        {
            "$group": {
                "_id": "$source_ip",
                "count": { "$sum": 1 }
            }
        },
        {
            "$match": {
                "count": { "$gte": 5 }
            }
        }
    ]

    results = list(logs_col.aggregate(pipeline))
    for r in results:
        alert = {
            "rule": "Multiple Failed Logins",
            "source_ip": r["_id"],
            "count": r["count"],
            "severity": "medium",
            "created_at": datetime.utcnow()
        }
        alerts_col.insert_one(alert)
