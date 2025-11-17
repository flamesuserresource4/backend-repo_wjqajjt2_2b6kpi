import os
from typing import Any, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "app_db")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow().isoformat()
    data_with_meta = {**data, "created_at": now, "updated_at": now}
    result = await db[collection_name].insert_one(data_with_meta)
    data_with_meta["_id"] = str(result.inserted_id)
    return data_with_meta

async def get_documents(collection_name: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50):
    db = await get_db()
    filter_dict = filter_dict or {}
    cursor = db[collection_name].find(filter_dict).limit(limit)
    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # stringified for JSON
        items.append(doc)
    return items
