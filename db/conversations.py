import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pymongo import DESCENDING
from db.mongo import get_collection

conversations = get_collection("conversations")
conversations.create_index([("last_interacted", DESCENDING)])

def now_utc():
    """Get current UTC time"""
    return datetime.now(timezone.utc)

def create_new_conversation_id() -> str:
    """Generate unique conversation ID"""
    return str(uuid.uuid4())

def create_new_conversation(title: Optional[str] = None, role: Optional[str] = None, content: Optional[str] = None) -> str:
    """Create new conversation"""
    conv_id = create_new_conversation_id()
    ts = now_utc()
    doc = {
        "_id": conv_id,
        "title": title or "Untitled Conversation",
        "messages": [],
        "last_interacted": ts,
    }
    if role and content:
        doc["messages"].append({"role": role, "content": content, "ts": ts})
    conversations.insert_one(doc)
    return conv_id

def add_message(conv_id: str, role: str, content: str) -> bool:
    """Add message to conversation"""
    ts = now_utc()
    res = conversations.update_one(
        {"_id": conv_id},
        {
            "$push": {"messages": {"role": role, "content": content, "ts": ts}},
            "$set": {"last_interacted": ts},
        },
    )
    return res.matched_count == 1

def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    """Get conversation by ID"""
    ts = now_utc()
    doc = conversations.find_one_and_update(
        {"_id": conv_id},
        {"$set": {"last_interacted": ts}},
        return_document=True,
    )
    return doc

def get_all_conversations() -> Dict[str, str]:
    """Get all conversations sorted by last interaction"""
    cursor = conversations.find({}, {"title": 1}).sort("last_interacted", DESCENDING)
    return {doc["_id"]: doc["title"] for doc in cursor}

def delete_conversation(conv_id: str) -> bool:
    """Delete conversation"""
    res = conversations.delete_one({"_id": conv_id})
    return res.deleted_count == 1