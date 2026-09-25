# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Arcade Machine
**Description:** Arcade machine with 2D & 3D game examples. This project showcases various game implementations using JavaScript and aims to provide a platform for playing and exploring different game concepts.
**Tech Stack:** JavaScript, HTML5 Canvas, (Potentially WebGL - check individual game implementations)

## Code Style & Conventions

### General Guidelines

- Follow existing code patterns and file structure.
- Prioritize readability and maintainability.
- Write clean, modular code.
- Comment complex logic, but aim for self-documenting code.

### Language-Specific Guidelines

- **JavaScript:** Use ES6+ features.
- Avoid global variables; encapsulate code within modules or classes.
- Use strict mode (`"use strict";`) where appropriate.

### File Organization

- Each game should reside in its own directory within the `games/` directory.
- Each game directory should contain:
    - `index.html`:  HTML entry point for the game.
    - `script.js`:  Main JavaScript file for the game logic.
    - `assets/`: (Optional) Directory for game assets (images, sounds, etc.).
- Shared utility functions should be placed in a `utils/` directory at the root.

## Architecture Patterns

- Favor object-oriented programming for game entities and logic.
- Decouple game logic from rendering.
- Use a game loop for consistent updates and rendering.

### Example: Good vs. Bad

**Good:** Modular game code

```javascript
// games/mygame/script.js
import { drawRect } from '../../utils/drawing.js';

class Player {
  constructor(x, y) {
    this.x = x;
    this.y = y;
  }

  render(context) {
    drawRect(context, this.x, this.y, 20, 20, 'red');
  }
}

// Game loop (simplified)
function gameLoop() {
  // ... update logic
  player.render(context);
  requestAnimationFrame(gameLoop);
}
```

**Bad:** Global variables and tightly coupled logic

```javascript
// games/mygame/script.js
let playerX = 10; // Global variable - BAD

function drawPlayer() {
  // Directly drawing without abstraction - BAD
  ctx.fillStyle = "red";
  ctx.fillRect(playerX, 20, 20, 20);
}

function gameLoop() {
  // ... update logic
  drawPlayer();
  requestAnimationFrame(gameLoop);
}
```

## Testing Strategy

- No specific testing framework is mandated at this time.
- Consider implementing basic unit tests for utility functions if they become complex.

## Security Considerations

- Be mindful of user input, especially if implementing features like saving game states.
- Sanitize any data loaded from external sources.

## Performance Guidelines

- Optimize rendering logic for smooth frame rates.
- Use requestAnimationFrame for animation.
- Minimize unnecessary DOM manipulations.

## Documentation Requirements

- Each game directory should have a `README.md` explaining the game's rules, controls, and any unique implementation details.
- Document any shared utility functions in the `utils/` directory.

## Common Pitfalls to Avoid

- Avoid using `eval()` or other potentially unsafe functions.
- Don't hardcode asset paths; use relative paths or a configuration file.
- Don't block the main thread with long-running operations.

## Preferred Libraries & Tools

- No specific libraries are mandated, but consider using libraries for:
    - Input handling
    - Sound effects
    - Animation

## Additional Context

- The goal is to create a diverse collection of games demonstrating different concepts and techniques.
- Focus on creating fun and engaging experiences.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.