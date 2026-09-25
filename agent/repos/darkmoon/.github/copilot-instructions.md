# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Darkmoon
**Description:** Real-time multiplayer 3D tag game and storefront
**Tech Stack:** TypeScript, React, Three.js, Socket.IO, Node.js, Zustand

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Maintain consistent naming conventions across the codebase.
- Write self-documenting code with clear variable and function names.
- Add comments only when the code's intent is not immediately clear.
- Use Prettier for code formatting. Run `npm run format` before committing.

### Language-Specific Guidelines

- **TypeScript**: Use strict mode. Prefer interfaces over types for object shapes unless a union or intersection type is required. Use explicit types, especially for function parameters and return values.
- **React**: Use functional components with hooks. Avoid class components unless absolutely necessary. Favor composition over inheritance.
- **Three.js**: Follow Three.js best practices for performance. Reuse geometries and materials where possible.
- **Socket.IO**: Handle socket events robustly, including error cases and disconnections.
- **Zustand**: Use Zustand for global state management. Keep stores small and focused.

### File Organization

- Keep files focused on a single responsibility.
- Use index files for barrel exports where appropriate (e.g., in component directories).
- Place types in dedicated `types/` directory or co-located with implementation in `[component].types.ts` files.
- Group related functionality in feature-specific directories (e.g., `src/components/Player`).

## Architecture Patterns

### Component Structure

- Follow atomic design principles (atoms, molecules, organisms).
- Keep components small and composable.
- Extract shared logic into custom hooks.
- Use composition over prop drilling. Prefer context or Zustand for deeply nested props.

### Data Flow

- Use server components for data fetching when possible.
- Implement proper error boundaries.
- Handle loading states consistently.
- Use optimistic updates for better UX where appropriate.

### API Design

- RESTful endpoints with consistent naming (if applicable). Most real-time communication happens over websockets.
- Validate all inputs at the API boundary.
- Return appropriate HTTP status codes.
- Include proper error messages and context.

## Testing Strategy

- Write unit tests for utility functions and helpers using Jest.
- Write integration tests for API endpoints using Jest and Supertest (if applicable).
- Write end-to-end (E2E) tests for critical user flows using Playwright.
- Aim for >80% code coverage.

## Security Considerations

- Never commit secrets, API keys, or credentials.
- Validate and sanitize all user inputs.
- Use environment variables for configuration.
- Implement proper authentication and authorization.
- Follow OWASP security best practices.

## Performance Guidelines

- Optimize Three.js scene rendering (reduce draw calls, use efficient shaders).
- Implement proper caching strategies (e.g., memoization).
- Use code splitting and lazy loading.
- Optimize images and assets.
- Monitor bundle size and runtime performance.

## Documentation Requirements

- Update README.md when adding new features or changing setup.
- Document complex algorithms or business logic.
- Keep API documentation in sync with implementation (if applicable).
- Update docs/CHANGELOG.md for notable changes.

## Common Pitfalls to Avoid

- Don't use `any` type in TypeScript. Use `unknown` if the type is truly unknown.
- Don't bypass TypeScript errors with `@ts-ignore` without a very good reason and a comment explaining why.
- Don't commit `console.log` statements. Use a proper logging library instead (TODO: SPECIFY LOGGING LIBRARY).
- Don't hardcode configuration values. Use environment variables.
- Don't skip error handling.
- Don't mix async/await with promise chains unnecessarily.
- Avoid premature optimization.

## Preferred Libraries & Tools

- **React**: For UI development.
- **Three.js**: For 3D rendering.
- **Socket.IO**: For real-time communication.
- **Zustand**: For global state management.
- **Jest**: For unit and integration testing.
- **Playwright**: For end-to-end testing.
- **Prettier**: For code formatting.
- **ESLint**: For linting.

## Additional Context

- The project uses a monorepo structure (TODO: CONFIRM MONOREPO).
- Game logic is primarily handled on the server for authoritative gameplay.
- Client-side prediction and reconciliation are used to improve responsiveness.
- The storefront is a separate application (TODO: PROVIDE MORE DETAILS).

## Examples

### Good Change

```typescript
// src/components/Player/Player.tsx
import React from 'react';
import { usePlayerStore } from '../../store/playerStore';

interface PlayerProps {
  playerId: string;
}

const Player: React.FC<PlayerProps> = ({ playerId }) => {
  const player = usePlayerStore((state) => state.players[playerId]);

  if (!player) {
    return null; // Or display a loading state
  }

  return (
    <div>
      {player.name} (Score: {player.score})
    </div>
  );
};

export default Player;
```

### Bad Change

```typescript
// src/components/Player/Player.tsx
import React from 'react';

const Player = (props: any) => { // Avoid 'any' type
  const player = window.store.getState().players[props.playerId]; // Avoid accessing global state directly

  return (
    <div>
      {player.name} (Score: {player.score})
    </div>
  );
};

export default Player;
```

## Commit Conventions

- Use conventional commits: `feat: Added player movement`, `fix: Resolved issue with score calculation`, `docs: Updated README`.
- Keep commit messages concise and descriptive.
- Reference issue numbers in commit messages (e.g., `fix: Resolved issue with score calculation #123`).

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.
