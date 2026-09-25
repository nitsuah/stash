# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Farm 3J Website
**Description:** A website for Farm 3J, a local farm.
**Tech Stack:** Next.js, TypeScript, Tailwind CSS

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Use Prettier for code formatting. Run `npm run format` before committing.
- Write clear and concise comments only when necessary.
- Prefer descriptive variable and function names.

### TypeScript Guidelines

- Use strict mode.
- Prefer interfaces over types for object shapes unless a union or intersection type is needed.
- Explicitly define types for all variables and function parameters.
- Leverage TypeScript's type system to catch errors early.

**Example (Good):**

```typescript
interface User {
  id: string;
  name: string;
  email: string;
}

const fetchUser = async (id: string): Promise => {
  // ...
};
```

**Example (Bad):**

```typescript
const fetchUser = async id => {
  // ...
};
```

### React Guidelines

- Use functional components with hooks.
- Keep components small and focused on a single responsibility.
- Use `React.FC` for functional components with type definitions for props.
- Avoid inline styles; use Tailwind CSS classes.

**Example (Good):**

```typescript
import React from 'react';

interface Props {
  name: string;
}

const MyComponent: React.FC<Props> = ({ name }) => {
  return <div className="text-blue-500">{name}</div>;
};
```

**Example (Bad):**

```typescript
const MyComponent = (props) => {
  return <div style={{ color: 'blue' }}>{props.name}</div>;
};
```

### File Organization

- Components should be placed in the `components/` directory.
- Pages should be placed in the `pages/` directory.
- Utility functions should be placed in the `utils/` directory.
- Styles should be defined using Tailwind CSS. Custom styles can be added in `styles/globals.css`.
- Types should be placed in `types/` or within the component directory if only used by that component.

## Architecture Patterns

- Use server components for data fetching where possible.
- Handle loading states and errors gracefully.

## Testing Strategy

- Write unit tests using Jest and React Testing Library.
- Place tests in a `__tests__` directory alongside the component or module being tested.
- Aim for high test coverage.

**Example:**

```javascript
// components/MyComponent.test.tsx
import { render, screen } from '@testing-library/react';
import MyComponent from './MyComponent';

test('renders the component with the correct name', () => {
  render(<MyComponent name="Test Name" />);
  const nameElement = screen.getByText(/Test Name/i);
  expect(nameElement).toBeInTheDocument();
});
```

## Security Considerations

- Never commit secrets, API keys, or credentials to the repository.
- Use environment variables for sensitive configuration.
- Validate all user inputs to prevent XSS and other vulnerabilities.

## Performance Guidelines

- Optimize images using tools like `next/image`.
- Use code splitting to reduce initial load time.

## Documentation Requirements

- Update the README.md file with any significant changes to the project.

## Common Pitfalls to Avoid

- Avoid using `any` type in TypeScript.
- Don't bypass TypeScript errors without a valid reason. If you must, add a comment explaining why.
- Don't commit `console.log` statements. Use a debugger instead.
- Don't hardcode configuration values.
- Don't skip error handling.

## Preferred Libraries & Tools

- Next.js: For building the website.
- TypeScript: For type safety and improved code quality.
- Tailwind CSS: For styling.
- Jest & React Testing Library: For testing.

## Commit Conventions

- Use conventional commits: `feat: add new feature`, `fix: resolve bug`, `docs: update documentation`, `chore: update dependencies`.

## Additional Context

- The project aims to be easily maintainable and scalable.
- Focus on providing a good user experience.
- TODO: Add link to ADRs (Architecture Decision Records) if any exist.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.
