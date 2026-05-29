/**
 * Express REST API — reference implementation
 *
 * Patterns covered:
 *   - App factory with Express Router
 *   - JWT authentication (jsonwebtoken)
 *   - Sequelize ORM with PostgreSQL
 *   - Request validation (joi)
 *   - Pagination, filtering, error handling
 *   - Health check endpoint
 *
 * Setup:
 *   npm install express sequelize pg pg-hstore jsonwebtoken joi dotenv
 *
 * Environment:
 *   DATABASE_URL   postgresql://user:pass@host:5432/dbname
 *   JWT_SECRET     random 32+ char string
 *   NODE_ENV       development | production
 *   PORT           8080 (default)
 *
 * Usage:
 *   node backend/express/app.js
 *   # or with nodemon for dev:
 *   npx nodemon backend/express/app.js
 */

"use strict";

require("dotenv").config();

const express    = require("express");
const jwt        = require("jsonwebtoken");
const Joi        = require("joi");
const { Sequelize, DataTypes, Op } = require("sequelize");

// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------

const config = {
  databaseUrl: process.env.DATABASE_URL || "sqlite::memory:",
  jwtSecret:   process.env.JWT_SECRET   || "change-me-in-production",
  jwtExpiry:   "1h",
  port:        parseInt(process.env.PORT || "8080", 10),
  isDev:       process.env.NODE_ENV !== "production",
};

// ---------------------------------------------------------------------------
// Database
// ---------------------------------------------------------------------------

const sequelize = new Sequelize(config.databaseUrl, {
  logging: config.isDev ? console.log : false,
  dialectOptions: config.databaseUrl.startsWith("postgres")
    ? { ssl: { require: true, rejectUnauthorized: false } }
    : {},
});

const User = sequelize.define("User", {
  email:     { type: DataTypes.STRING, allowNull: false, unique: true },
  name:      { type: DataTypes.STRING, allowNull: false },
  role:      { type: DataTypes.STRING, defaultValue: "viewer" },
  active:    { type: DataTypes.BOOLEAN, defaultValue: true },
}, { underscored: true });

const Item = sequelize.define("Item", {
  title:       { type: DataTypes.STRING, allowNull: false },
  description: { type: DataTypes.TEXT },
  status:      { type: DataTypes.STRING, defaultValue: "active" },
}, { underscored: true });

User.hasMany(Item, { foreignKey: "owner_id", as: "items" });
Item.belongsTo(User, { foreignKey: "owner_id", as: "owner" });

// ---------------------------------------------------------------------------
// Auth middleware
// ---------------------------------------------------------------------------

function authenticate(req, res, next) {
  const header = req.headers.authorization || "";
  const token  = header.startsWith("Bearer ") ? header.slice(7) : null;
  if (!token) return res.status(401).json({ error: "Missing token" });
  try {
    req.user = jwt.verify(token, config.jwtSecret);
    next();
  } catch {
    res.status(401).json({ error: "Invalid or expired token" });
  }
}

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function paginate(req) {
  const page    = Math.max(1, parseInt(req.query.page    || "1",  10));
  const perPage = Math.min(100, parseInt(req.query.per_page || "20", 10));
  return { limit: perPage, offset: (page - 1) * perPage, page, perPage };
}

function paginatedResponse(res, rows, count, { page, perPage }) {
  res.json({
    data: rows,
    pagination: { page, per_page: perPage, total: count, pages: Math.ceil(count / perPage) },
  });
}

function validate(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, { abortEarly: false, stripUnknown: true });
    if (error) {
      return res.status(422).json({
        error:   "Validation failed",
        details: error.details.map(d => d.message),
      });
    }
    req.validated = value;
    next();
  };
}

// ---------------------------------------------------------------------------
// Schemas
// ---------------------------------------------------------------------------

const loginSchema = Joi.object({
  email:    Joi.string().email().required(),
  password: Joi.string().required(),
});

const itemCreateSchema = Joi.object({
  title:       Joi.string().min(1).max(255).required(),
  description: Joi.string().allow("", null),
  status:      Joi.string().valid("active", "archived", "draft").default("active"),
});

const itemUpdateSchema = Joi.object({
  title:       Joi.string().min(1).max(255),
  description: Joi.string().allow("", null),
  status:      Joi.string().valid("active", "archived", "draft"),
}).min(1);

// ---------------------------------------------------------------------------
// Routes — Auth
// ---------------------------------------------------------------------------

const authRouter = express.Router();

authRouter.post("/login", validate(loginSchema), async (req, res) => {
  const { email, password } = req.validated;

  // Demo: accept any email with password "password"
  if (password !== "password") {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  let user = await User.findOne({ where: { email } });
  if (!user) {
    user = await User.create({ email, name: email.split("@")[0] });
  }

  const token = jwt.sign({ id: user.id, role: user.role }, config.jwtSecret, {
    expiresIn: config.jwtExpiry,
  });
  res.json({ access_token: token, token_type: "bearer" });
});

authRouter.get("/me", authenticate, async (req, res) => {
  const user = await User.findByPk(req.user.id);
  if (!user) return res.status(404).json({ error: "User not found" });
  res.json(user);
});

// ---------------------------------------------------------------------------
// Routes — Users
// ---------------------------------------------------------------------------

const usersRouter = express.Router();
usersRouter.use(authenticate);

usersRouter.get("/", async (req, res) => {
  const { limit, offset, page, perPage } = paginate(req);
  const where = {};
  if (req.query.active !== undefined) {
    where.active = req.query.active === "true";
  }
  const { rows, count } = await User.findAndCountAll({
    where, limit, offset, order: [["created_at", "DESC"]],
  });
  paginatedResponse(res, rows, count, { page, perPage });
});

usersRouter.get("/:id", async (req, res) => {
  const user = await User.findByPk(req.params.id);
  if (!user) return res.status(404).json({ error: "User not found" });
  res.json(user);
});

// ---------------------------------------------------------------------------
// Routes — Items
// ---------------------------------------------------------------------------

const itemsRouter = express.Router();
itemsRouter.use(authenticate);

itemsRouter.get("/", async (req, res) => {
  const { limit, offset, page, perPage } = paginate(req);
  const where = {};
  if (req.query.status)   where.status   = req.query.status;
  if (req.query.owner_id) where.owner_id = parseInt(req.query.owner_id, 10);

  const { rows, count } = await Item.findAndCountAll({
    where, limit, offset, order: [["created_at", "DESC"]],
    include: [{ model: User, as: "owner", attributes: ["id", "name", "email"] }],
  });
  paginatedResponse(res, rows, count, { page, perPage });
});

itemsRouter.get("/:id", async (req, res) => {
  const item = await Item.findByPk(req.params.id, {
    include: [{ model: User, as: "owner", attributes: ["id", "name", "email"] }],
  });
  if (!item) return res.status(404).json({ error: "Item not found" });
  res.json(item);
});

itemsRouter.post("/", validate(itemCreateSchema), async (req, res) => {
  const item = await Item.create({ ...req.validated, owner_id: req.user.id });
  res.status(201).json(item);
});

itemsRouter.patch("/:id", validate(itemUpdateSchema), async (req, res) => {
  const item = await Item.findByPk(req.params.id);
  if (!item) return res.status(404).json({ error: "Item not found" });

  if (item.owner_id !== req.user.id && req.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden" });
  }
  await item.update(req.validated);
  res.json(item);
});

itemsRouter.delete("/:id", async (req, res) => {
  const item = await Item.findByPk(req.params.id);
  if (!item) return res.status(404).json({ error: "Item not found" });

  if (item.owner_id !== req.user.id && req.user.role !== "admin") {
    return res.status(403).json({ error: "Forbidden" });
  }
  await item.destroy();
  res.status(204).end();
});

// ---------------------------------------------------------------------------
// App factory
// ---------------------------------------------------------------------------

async function createApp() {
  const app = express();
  app.use(express.json());

  app.get("/health", (req, res) =>
    res.json({ status: "ok", timestamp: new Date().toISOString() })
  );

  app.use("/auth",  authRouter);
  app.use("/users", usersRouter);
  app.use("/items", itemsRouter);

  app.use((req, res) => res.status(404).json({ error: "Not found" }));

  app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: "Internal server error" });
  });

  await sequelize.sync({ alter: config.isDev });
  return app;
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

if (require.main === module) {
  createApp().then(app => {
    app.listen(config.port, () => {
      console.log(`Express API running on http://localhost:${config.port}`);
      console.log(`  POST /auth/login    {"email": "user@example.com", "password": "password"}`);
      console.log(`  GET  /auth/me       (requires Bearer token)`);
      console.log(`  GET  /users/        (requires Bearer token)`);
      console.log(`  GET  /items/        (requires Bearer token)`);
      console.log(`  POST /items/        (requires Bearer token)`);
      console.log(`  GET  /health`);
    });
  });
}

module.exports = { createApp, User, Item, sequelize };
