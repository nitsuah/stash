# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** fire  
**Description:** Lightweight FIRE Tracker & API Server for tracking financial independence, retire early goals.  
**Tech Stack:** JavaScript (Node.js), Database (e.g., SQLite, PostgreSQL for data persistence), Express.js (for API server).

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Maintain consistent naming conventions across the codebase (e.g., `camelCase` for variables/functions, `PascalCase` for classes/constructors).
- Write self-documenting code with clear variable and function names.
- Add comments only when the code's intent is not immediately clear or for complex business logic.

### Language-Specific Guidelines

- **JavaScript**:
    - Use modern ES6+ features (`const`, `let`, arrow functions, destructuring).
    - Prefer asynchronous patterns using `async/await` over callbacks or `.then().catch()`.
    - Follow a consistent linting style (e.g., StandardJS or Airbnb style, if not explicitly configured, lean towards readability and consistency with existing files).
    - Avoid global variables.
    - Handle errors gracefully using `try...catch` blocks for asynchronous operations.
- **Database**:
    - Use parameterized queries to prevent SQL injection.
    - Never use string concatenation for building SQL queries.
    - Prefer using an ORM or query builder (e.g., Knex.js, Sequelize) for complex database interactions.

### File Organization

- Keep files focused on a single responsibility.
- Group related functionality in feature-specific directories (e.g., `src/transactions`, `src/users`).
- Place utility functions in a `src/utils` directory.
- Database access logic should be separated from API route handlers (e.g., `src/models` or `src/db`).
- Middleware should be placed in `src/middleware`.

## Architecture Patterns

### Module Structure

- Organize modules by feature or domain (e.g., `src/transactions/transactionService.js`, `src/transactions/transactionController.js`).
- Keep modules small and focused on a single responsibility (e.g., a controller for handling requests, a service for business logic, a model for data access).
- Extract reusable utilities or middleware into dedicated files.

### Data Flow

- All incoming requests should pass through appropriate validation middleware.
- Business logic should reside in service layers, separate from controllers.
- Database interactions should be handled by dedicated data access modules (models).
- Implement proper error handling middleware to catch and format errors consistently.
- Handle loading states consistently (though less relevant for a pure API, consider client-side implications).

### API Design

- Design RESTful endpoints with consistent naming conventions (e.g., `/api/v1/transactions`, `/api/v1/users`).
- Validate all inputs at the API boundary using a validation library (e.g., Joi, express-validator).
- Return appropriate HTTP status codes (2xx for success, 4xx for client errors, 5xx for server errors).
- Include proper error messages and context in API responses for client-side debugging.

## Testing Strategy

- Write unit tests for utility functions, service layers, and data access modules.
- Write integration tests for API endpoints