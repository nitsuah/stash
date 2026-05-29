"""
Flask REST API — reference implementation

Patterns covered:
  - App factory with blueprints
  - JWT authentication (PyJWT)
  - SQLAlchemy ORM with PostgreSQL
  - Request validation (marshmallow)
  - Pagination, filtering, error handling
  - Health check + metrics endpoints

Setup:
    pip install flask flask-sqlalchemy flask-jwt-extended marshmallow psycopg2-binary

Environment:
    DATABASE_URL   postgresql://user:pass@host:5432/dbname
    JWT_SECRET     random 32+ char string
    FLASK_ENV      development | production
    PORT           8080 (default)

Usage:
    python backend/flask/app.py
    # or
    FLASK_APP=backend/flask/app.py flask run --port 8080
"""

import os
import sys
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from flask_jwt_extended import (  # type: ignore
    JWTManager, create_access_token, jwt_required, get_jwt_identity,
)
from marshmallow import Schema, fields, validate, ValidationError  # type: ignore
import sqlalchemy as sa

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

class Config:
    DATABASE_URL   = os.environ.get("DATABASE_URL", "sqlite:///dev.db")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET", "change-me-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SQLALCHEMY_DATABASE_URI    = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


# ---------------------------------------------------------------------------
# Extensions
# ---------------------------------------------------------------------------

db  = SQLAlchemy()
jwt = JWTManager()


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True)
    email      = db.Column(db.String(255), unique=True, nullable=False)
    name       = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(50), default="viewer")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    active     = db.Column(db.Boolean, default=True)

    items = db.relationship("Item", back_populates="owner", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
        }


class Item(db.Model):
    __tablename__ = "items"

    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status      = db.Column(db.String(50), default="active")
    owner_id    = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at  = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                            onupdate=lambda: datetime.now(timezone.utc))

    owner = db.relationship("User", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# ---------------------------------------------------------------------------
# Schemas (validation)
# ---------------------------------------------------------------------------

class ItemCreateSchema(Schema):
    title       = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    description = fields.Str(load_default=None)
    status      = fields.Str(load_default="active",
                             validate=validate.OneOf(["active", "archived", "draft"]))


class ItemUpdateSchema(Schema):
    title       = fields.Str(validate=validate.Length(min=1, max=255))
    description = fields.Str()
    status      = fields.Str(validate=validate.OneOf(["active", "archived", "draft"]))


class LoginSchema(Schema):
    email    = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def paginate(query, page: int, per_page: int) -> dict:
    total   = query.count()
    records = query.offset((page - 1) * per_page).limit(per_page).all()
    return {
        "items": records,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
        },
    }


def error_response(message: str, status: int = 400, details=None) -> tuple:
    body = {"error": message}
    if details:
        body["details"] = details
    return jsonify(body), status


# ---------------------------------------------------------------------------
# Blueprints
# ---------------------------------------------------------------------------

from flask import Blueprint

auth_bp  = Blueprint("auth",  __name__, url_prefix="/auth")
users_bp = Blueprint("users", __name__, url_prefix="/users")
items_bp = Blueprint("items", __name__, url_prefix="/items")


# ── Auth ────────────────────────────────────────────────────────────────────

@auth_bp.post("/login")
def login():
    """POST /auth/login — returns JWT access token."""
    try:
        data = LoginSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("Validation failed", 422, e.messages)

    # Demo: accept any email with password "password"
    # Replace with real credential verification
    if data["password"] != "password":
        return error_response("Invalid credentials", 401)

    user = db.session.scalar(sa.select(User).where(User.email == data["email"]))
    if not user:
        # Auto-create on first login for demo purposes
        user = User(email=data["email"], name=data["email"].split("@")[0])
        db.session.add(user)
        db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "token_type": "bearer"})


@auth_bp.get("/me")
@jwt_required()
def me():
    """GET /auth/me — current authenticated user."""
    user_id = int(get_jwt_identity())
    user    = db.session.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
    return jsonify(user.to_dict())


# ── Users ───────────────────────────────────────────────────────────────────

@users_bp.get("/")
@jwt_required()
def list_users():
    """GET /users — paginated user list. Query: page, per_page, active."""
    page     = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    active   = request.args.get("active", type=lambda v: v.lower() == "true")

    q = sa.select(User).order_by(User.created_at.desc())
    if active is not None:
        q = q.where(User.active == active)

    total   = db.session.scalar(sa.select(sa.func.count()).select_from(q.subquery()))
    records = db.session.scalars(q.offset((page - 1) * per_page).limit(per_page)).all()
    return jsonify({
        "users": [u.to_dict() for u in records],
        "pagination": {"page": page, "per_page": per_page, "total": total},
    })


@users_bp.get("/<int:user_id>")
@jwt_required()
def get_user(user_id: int):
    """GET /users/{id}"""
    user = db.session.get(User, user_id)
    if not user:
        return error_response("User not found", 404)
    return jsonify(user.to_dict())


# ── Items ───────────────────────────────────────────────────────────────────

@items_bp.get("/")
@jwt_required()
def list_items():
    """GET /items — paginated. Query: page, per_page, status, owner_id."""
    page     = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 20, type=int), 100)
    status   = request.args.get("status")
    owner_id = request.args.get("owner_id", type=int)

    q = sa.select(Item).order_by(Item.created_at.desc())
    if status:
        q = q.where(Item.status == status)
    if owner_id:
        q = q.where(Item.owner_id == owner_id)

    total   = db.session.scalar(sa.select(sa.func.count()).select_from(q.subquery()))
    records = db.session.scalars(q.offset((page - 1) * per_page).limit(per_page)).all()
    return jsonify({
        "items": [i.to_dict() for i in records],
        "pagination": {"page": page, "per_page": per_page, "total": total},
    })


@items_bp.get("/<int:item_id>")
@jwt_required()
def get_item(item_id: int):
    """GET /items/{id}"""
    item = db.session.get(Item, item_id)
    if not item:
        return error_response("Item not found", 404)
    return jsonify(item.to_dict())


@items_bp.post("/")
@jwt_required()
def create_item():
    """POST /items"""
    try:
        data = ItemCreateSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("Validation failed", 422, e.messages)

    owner_id = int(get_jwt_identity())
    item = Item(owner_id=owner_id, **data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@items_bp.patch("/<int:item_id>")
@jwt_required()
def update_item(item_id: int):
    """PATCH /items/{id}"""
    item = db.session.get(Item, item_id)
    if not item:
        return error_response("Item not found", 404)

    requester_id = int(get_jwt_identity())
    requester    = db.session.get(User, requester_id)
    if item.owner_id != requester_id and requester.role != "admin":
        return error_response("Forbidden", 403)

    try:
        data = ItemUpdateSchema().load(request.get_json() or {})
    except ValidationError as e:
        return error_response("Validation failed", 422, e.messages)

    for key, val in data.items():
        setattr(item, key, val)
    item.updated_at = datetime.now(timezone.utc)
    db.session.commit()
    return jsonify(item.to_dict())


@items_bp.delete("/<int:item_id>")
@jwt_required()
def delete_item(item_id: int):
    """DELETE /items/{id}"""
    item = db.session.get(Item, item_id)
    if not item:
        return error_response("Item not found", 404)

    requester_id = int(get_jwt_identity())
    requester    = db.session.get(User, requester_id)
    if item.owner_id != requester_id and requester.role != "admin":
        return error_response("Forbidden", 403)

    db.session.delete(item)
    db.session.commit()
    return "", 204


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app(config: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(items_bp)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})

    @app.errorhandler(404)
    def not_found(e):
        return error_response("Not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return error_response("Method not allowed", 405)

    @app.errorhandler(500)
    def server_error(e):
        return error_response("Internal server error", 500)

    with app.app_context():
        db.create_all()

    return app


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app  = create_app()
    print(f"Flask API running on http://localhost:{port}")
    print(f"  POST /auth/login    {{\"email\": \"user@example.com\", \"password\": \"password\"}}")
    print(f"  GET  /auth/me       (requires Bearer token)")
    print(f"  GET  /users/        (requires Bearer token)")
    print(f"  GET  /items/        (requires Bearer token)")
    print(f"  POST /items/        (requires Bearer token)")
    print(f"  GET  /health")
    app.run(port=port, debug=os.environ.get("FLASK_ENV") == "development")
