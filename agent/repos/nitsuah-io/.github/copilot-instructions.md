# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Nitsuah.io
**Description:** Personal portfolio built on Next.js. Showcases projects, skills, and contact information.
**Tech Stack:** Next.js, TypeScript, Tailwind CSS, Vercel

## Code Style & Conventions

### General Guidelines

- Follow the existing code style.  Consistency is key.
- Prioritize readability. Code should be easy to understand and maintain.
- Keep components small and focused.
- Use descriptive variable and function names.

### Language-Specific Guidelines

- **TypeScript:** Use types extensively. Avoid `any`. Prefer `interface` over `type` when defining object shapes. Enable `strict` mode in `tsconfig.json`.
- **Next.js:** Leverage server components where possible for data fetching and performance. Follow Next.js conventions for routing and data handling.
- **Tailwind CSS:** Utilize Tailwind's utility classes for styling. Avoid writing custom CSS unless absolutely necessary.  Maintain a consistent design language using the `tailwind.config.js` file.

### File Organization

- `components/`: Reusable UI components.
- `pages/`: Next.js pages for routing.
- `public/`: Static assets (images, fonts, etc.).
- `styles/`: Global styles and Tailwind configuration.
- `lib/`: Utility functions and helper modules.

## Architecture Patterns

### Component Structure

- Atomic Design principles: Structure components as Atoms, Molecules, Organisms, and Templates.
- Favor composition over inheritance.
- Use custom hooks to extract reusable logic.

### Data Flow

- Fetch data using server components whenever possible.
- Use `try...catch` blocks and error boundaries to handle errors gracefully.
- Implement loading states to improve user experience.

## Testing Strategy

- Write unit tests for utility functions and components.
- Use Jest and React Testing Library for testing.

## Security Considerations

- Never commit API keys or sensitive information. Use environment variables.
- Sanitize user inputs to prevent XSS vulnerabilities.

## Performance Guidelines

- Optimize images using Next.js's Image component.
- Use code splitting to reduce initial bundle size.
- Leverage browser caching.

## Documentation Requirements

- Document any complex logic or algorithms.
- Keep the README.md file up-to-date.
- Use JSDoc-style comments for documenting functions and components.

## Common Pitfalls to Avoid

- Using `any` type in TypeScript.
- Ignoring TypeScript errors.
- Committing `console.log` statements.
- Hardcoding values. Use environment variables or configuration files.
- Skipping error handling.
- Over-engineering solutions.

## Preferred Libraries & Tools

- **Next.js:** For the React framework.
- **TypeScript:** For type safety.
- **Tailwind CSS:** For styling.
- **Vercel:** For deployment.
- **React Testing Library and Jest:** For testing.

## Additional Context

- This project is deployed on Vercel.
- The goal is to maintain a clean, performant, and accessible portfolio website.

## Examples

### Good Change:

```typescript
// lib/utils.ts
export const formatDate = (date: Date): string => {
  return new Intl.DateTimeFormat('en-US').format(date);
};
```

### Bad Change:

```typescript
// lib/utils.ts
export const formatDate = (date) => { // Missing type annotation
  return date.toLocaleDateString(); // Not using a specific locale
};
```

### Good Commit Message:

```
feat: Add contact form

Implements a contact form using server actions.  Includes validation and error handling.
```

### Bad Commit Message:

```
update
```

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.