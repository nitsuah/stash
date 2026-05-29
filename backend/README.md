# Backend API Examples

Reference implementations for REST APIs — JWT auth, ORM, validation, pagination.

## Services

| Directory | Language / Framework | ORM | Auth |
|-----------|---------------------|-----|------|
| [`flask/`](flask/) | Python / Flask | SQLAlchemy | JWT (PyJWT) |
| [`express/`](express/) | Node.js / Express | Sequelize | JWT (jsonwebtoken) |

Both cover the same surface area so patterns are directly comparable.

---

## Flask

**Docs:** https://flask.palletsprojects.com/

### Setup

```bash
pip install flask flask-sqlalchemy flask-jwt-extended marshmallow psycopg2-binary
```

### Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///dev.db` | SQLAlchemy DB connection string |
| `JWT_SECRET` | *(insecure default)* | Random 32+ char secret |
| `FLASK_ENV` | — | Set to `development` for debug mode |
| `PORT` | `8080` | Bind port |

### Quick start

```bash
DATABASE_URL=sqlite:///dev.db JWT_SECRET=devsecret python backend/flask/app.py
```

### Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/auth/login` | — | Returns JWT access token |
| `GET` | `/auth/me` | Bearer | Current user profile |
| `GET` | `/users/` | Bearer | Paginated user list |
| `GET` | `/users/{id}` | Bearer | User detail |
| `GET` | `/items/` | Bearer | Paginated items (filter: status, owner_id) |
| `GET` | `/items/{id}` | Bearer | Item detail |
| `POST` | `/items/` | Bearer | Create item |
| `PATCH` | `/items/{id}` | Bearer | Update item (owner or admin only) |
| `DELETE` | `/items/{id}` | Bearer | Delete item (owner or admin only) |
| `GET` | `/health` | — | Health check |

---

## Express

**Docs:** https://expressjs.com/

### Setup

```bash
cd backend/express
npm install
```

### Environment variables

Same as Flask above — `DATABASE_URL`, `JWT_SECRET`, `NODE_ENV`, `PORT`.

### Quick start

```bash
cd backend/express
DATABASE_URL=sqlite::memory: JWT_SECRET=devsecret node app.js
```

### Endpoints

Same surface as Flask — identical paths and behavior, different stack.

---

## Auth flow

```
POST /auth/login  {"email": "user@example.com", "password": "password"}
→ {"access_token": "eyJ...", "token_type": "bearer"}

GET /items/
Authorization: Bearer eyJ...
```

Demo accepts any email with password `"password"` and auto-creates the user.
Replace the credential check in `login` with real password hashing (`bcrypt`).
