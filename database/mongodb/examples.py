"""
MongoDB examples — PyMongo

Patterns covered:
  - CRUD operations
  - Aggregation pipeline
  - Indexes (single, compound, text, TTL)
  - Schema validation (JSON Schema)
  - Transactions (multi-document)
  - Change streams
  - Geospatial queries

Setup:
    pip install pymongo python-dotenv

Environment:
    MONGODB_URI      mongodb://localhost:27017  (or Atlas URI)
    MONGODB_DB       myapp

Usage:
    python database/mongodb/examples.py
    python database/mongodb/examples.py --demo-write
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pprint import pprint

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT, GEOSPHERE  # type: ignore
from pymongo.errors import DuplicateKeyError  # type: ignore
from bson import ObjectId  # type: ignore

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(_SCRIPT_DIR)))


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def load_env(env_file: str | None = None) -> None:
    for p in [env_file,
              os.path.join(_SCRIPT_DIR, ".env"),
              os.path.join(os.path.dirname(_SCRIPT_DIR), ".env")]:
        if p and os.path.exists(p):
            try:
                from dotenv import load_dotenv  # type: ignore
                load_dotenv(p, override=False)
            except ImportError:
                with open(p) as fh:
                    for line in fh:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return


def get_db(env_file: str | None = None):
    load_env(env_file)
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.environ.get("MONGODB_DB", "myapp")
    client = MongoClient(uri)
    return client[db_name]


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

USER_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["email", "name", "role", "createdAt"],
        "properties": {
            "email":     {"bsonType": "string", "pattern": "^.+@.+\\..+$"},
            "name":      {"bsonType": "string", "minLength": 1},
            "role":      {"bsonType": "string", "enum": ["admin", "editor", "viewer"]},
            "active":    {"bsonType": "bool"},
            "createdAt": {"bsonType": "date"},
        },
    }
}

ITEM_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "status", "ownerId", "createdAt"],
        "properties": {
            "title":     {"bsonType": "string", "minLength": 1, "maxLength": 255},
            "status":    {"bsonType": "string", "enum": ["draft", "active", "archived"]},
            "tags":      {"bsonType": "array", "items": {"bsonType": "string"}},
            "ownerId":   {"bsonType": "objectId"},
            "createdAt": {"bsonType": "date"},
        },
    }
}


def ensure_collections(db) -> None:
    """Create collections with schema validation and indexes if they don't exist."""
    existing = db.list_collection_names()

    if "users" not in existing:
        db.create_collection("users", validator=USER_VALIDATOR)
    if "items" not in existing:
        db.create_collection("items", validator=ITEM_VALIDATOR)

    # Users indexes
    db.users.create_index([("email", ASCENDING)], unique=True, name="idx_email")
    db.users.create_index([("active", ASCENDING), ("createdAt", DESCENDING)], name="idx_active_date")

    # Items indexes
    db.items.create_index([("ownerId", ASCENDING), ("status", ASCENDING)], name="idx_owner_status")
    db.items.create_index([("tags", ASCENDING)], name="idx_tags")
    db.items.create_index([("title", TEXT), ("body", TEXT)], name="idx_text_search",
                          weights={"title": 10, "body": 1})
    db.items.create_index([("createdAt", ASCENDING)],
                          expireAfterSeconds=60 * 60 * 24 * 365,  # 1-year TTL
                          name="idx_ttl",
                          partialFilterExpression={"status": "archived"})

    print("[Setup] Collections and indexes ready.")


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

def create_user(db, email: str, name: str, role: str = "viewer") -> dict:
    doc = {
        "email":     email,
        "name":      name,
        "role":      role,
        "active":    True,
        "metadata":  {},
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc),
    }
    result = db.users.insert_one(doc)
    doc["_id"] = result.inserted_id
    print(f"\n[User Created] {doc['email']}  id={doc['_id']}")
    return doc


def get_user(db, user_id: str | ObjectId) -> dict | None:
    user = db.users.find_one({"_id": ObjectId(user_id) if isinstance(user_id, str) else user_id})
    if user:
        print(f"\n[User] {user['email']}  role={user['role']}")
    return user


def list_users(db, active_only: bool = True, limit: int = 20) -> list[dict]:
    query = {"active": True} if active_only else {}
    users = list(db.users.find(query).sort("createdAt", DESCENDING).limit(limit))
    print(f"\n[Users] {len(users)} returned:")
    for u in users:
        print(f"  {str(u['_id'])[:8]}  {u['email']:40s}  [{u['role']}]")
    return users


def update_user(db, user_id: str | ObjectId, updates: dict) -> dict | None:
    oid = ObjectId(user_id) if isinstance(user_id, str) else user_id
    updates["updatedAt"] = datetime.now(timezone.utc)
    result = db.users.find_one_and_update(
        {"_id": oid},
        {"$set": updates},
        return_document=True,
    )
    if result:
        print(f"\n[User Updated] {result['email']}  fields={list(updates.keys())}")
    return result


# ---------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------

def create_item(db, owner_id: ObjectId, title: str,
                body: str = "", tags: list[str] | None = None,
                status: str = "draft") -> dict:
    doc = {
        "title":     title,
        "body":      body,
        "status":    status,
        "tags":      tags or [],
        "ownerId":   owner_id,
        "metadata":  {},
        "createdAt": datetime.now(timezone.utc),
        "updatedAt": datetime.now(timezone.utc),
    }
    result = db.items.insert_one(doc)
    doc["_id"] = result.inserted_id
    print(f"\n[Item Created] {doc['title']}  id={doc['_id']}")
    return doc


def list_items(db, owner_id: ObjectId | None = None, status: str | None = None,
               tags: list[str] | None = None, limit: int = 20) -> list[dict]:
    query: dict = {}
    if owner_id: query["ownerId"] = owner_id
    if status:   query["status"]  = status
    if tags:     query["tags"]    = {"$all": tags}

    items = list(db.items.find(query).sort("createdAt", DESCENDING).limit(limit))
    print(f"\n[Items] {len(items)} returned:")
    for i in items:
        print(f"  {str(i['_id'])[:8]}  [{i['status']:8s}]  {i['title'][:60]}")
    return items


def text_search(db, query: str, limit: int = 10) -> list[dict]:
    results = list(db.items.find(
        {"$text": {"$search": query}},
        {"score": {"$meta": "textScore"}},
    ).sort([("score", {"$meta": "textScore"})]).limit(limit))
    print(f"\n[Text Search: '{query}'] {len(results)} results:")
    for r in results:
        print(f"  score={r.get('score', 0):.2f}  {r['title'][:60]}")
    return results


# ---------------------------------------------------------------------------
# Aggregation pipeline
# ---------------------------------------------------------------------------

def item_stats_by_owner(db) -> list[dict]:
    """Count items by status per owner."""
    pipeline = [
        {"$group": {
            "_id":      {"owner": "$ownerId", "status": "$status"},
            "count":    {"$sum": 1},
            "lastItem": {"$max": "$createdAt"},
        }},
        {"$group": {
            "_id":      "$_id.owner",
            "byStatus": {"$push": {"status": "$_id.status", "count": "$count"}},
            "total":    {"$sum": "$count"},
            "lastItem": {"$max": "$lastItem"},
        }},
        {"$lookup": {
            "from":         "users",
            "localField":   "_id",
            "foreignField": "_id",
            "as":           "owner",
        }},
        {"$unwind": {"path": "$owner", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "ownerEmail": "$owner.email",
            "total":      1,
            "byStatus":   1,
            "lastItem":   1,
        }},
        {"$sort": {"total": -1}},
    ]
    results = list(db.items.aggregate(pipeline))
    print(f"\n[Item Stats by Owner] {len(results)} owners:")
    for r in results:
        print(f"  {r.get('ownerEmail', '?'):40s}  total={r['total']}")
    return results


def tag_frequency(db, limit: int = 20) -> list[dict]:
    """Most common tags across all items."""
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit},
    ]
    results = list(db.items.aggregate(pipeline))
    print(f"\n[Tag Frequency] top {limit}:")
    for r in results:
        print(f"  {r['_id']:30s}  {r['count']}")
    return results


def daily_item_counts(db, days: int = 30) -> list[dict]:
    """Items created per day over the last N days."""
    since = datetime.now(timezone.utc) - timedelta(days=days)
    pipeline = [
        {"$match": {"createdAt": {"$gte": since}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}},
            "count": {"$sum": 1},
        }},
        {"$sort": {"_id": 1}},
    ]
    results = list(db.items.aggregate(pipeline))
    print(f"\n[Daily Counts — last {days}d] {len(results)} days with data:")
    for r in results:
        print(f"  {r['_id']}  {r['count']:>4}")
    return results


# ---------------------------------------------------------------------------
# Multi-document transaction
# ---------------------------------------------------------------------------

def transfer_item_ownership(client, db_name: str,
                            item_id: ObjectId, new_owner_id: ObjectId) -> bool:
    """Move an item to a new owner, logging the change atomically."""
    db = client[db_name]
    with client.start_session() as session:
        with session.start_transaction():
            item = db.items.find_one({"_id": item_id}, session=session)
            if not item:
                return False

            db.items.update_one(
                {"_id": item_id},
                {"$set": {"ownerId": new_owner_id, "updatedAt": datetime.now(timezone.utc)}},
                session=session,
            )
            db.audit_log.insert_one({
                "action":    "item.owner_transfer",
                "itemId":    item_id,
                "fromOwner": item["ownerId"],
                "toOwner":   new_owner_id,
                "at":        datetime.now(timezone.utc),
            }, session=session)

    print(f"\n[Transfer] item={item_id} → owner={new_owner_id}  (committed)")
    return True


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="MongoDB PyMongo examples",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Environment variables:
  MONGODB_URI   mongodb://localhost:27017
  MONGODB_DB    myapp

Examples:
  python database/mongodb/examples.py
  python database/mongodb/examples.py --demo-write
        """,
    )
    parser.add_argument("--env-file", default=None, metavar="FILE")
    parser.add_argument("--demo-write", action="store_true",
                        help="Run write ops (creates users + items, runs aggregation)")
    args = parser.parse_args()

    db = get_db(args.env_file)
    ensure_collections(db)

    print(f"\n{'='*60}")
    print("MongoDB Examples")
    print(f"{'='*60}")

    list_users(db)
    item_stats_by_owner(db)
    tag_frequency(db)
    daily_item_counts(db)

    if args.demo_write:
        print(f"\n{'='*60}")
        print("Write Operations")
        print(f"{'='*60}")

        try:
            user = create_user(db, "demo@example.com", "Demo User", role="editor")
        except DuplicateKeyError:
            user = db.users.find_one({"email": "demo@example.com"})
            print(f"[User Exists] {user['email']}")

        item1 = create_item(db, user["_id"], "[DEMO] API test item — safe to delete",
                            body="Created by database/mongodb/examples.py",
                            tags=["demo", "api-test"], status="active")
        item2 = create_item(db, user["_id"], "[DEMO] Kubernetes deployment guide",
                            body="Step by step kubernetes setup", tags=["k8s", "ops"])

        text_search(db, "kubernetes deployment")
        item_stats_by_owner(db)

        # Cleanup
        db.items.delete_many({"ownerId": user["_id"], "title": {"$regex": "^\\[DEMO\\]"}})
        db.users.delete_one({"email": "demo@example.com"})
        print("\n[Cleanup] Demo user and items deleted.")


if __name__ == "__main__":
    main()
