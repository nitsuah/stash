# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** skyview
**Description:** No description available. This project appears to primarily use CSS.
**Tech Stack:** CSS

## Code Style & Conventions

### General Guidelines

- Follow the existing CSS style in the project.
- Use meaningful and descriptive class names.
- Prioritize readability and maintainability.

### CSS-Specific Guidelines

- Use consistent indentation (2 spaces).
- Order CSS properties alphabetically (within a block).
- Use lowercase for all CSS property names and values where applicable.
- Prefer shorthand properties where appropriate.
- Avoid overly specific selectors.
- Use CSS variables (custom properties) for reusable values like colors, fonts, and spacing.

### File Organization

- Keep CSS files focused on specific components or modules.
- Group related styles together.
- Consider using a BEM-like naming convention if the project scales.

## Architecture Patterns

- This project appears to be CSS-centric, focusing on styling. Apply CSS principles of reusability and maintainability.

## Testing Strategy

- While dedicated CSS testing frameworks might not be in place, visually inspect changes in different browsers and screen sizes.
- Consider using tools like browser developer tools to check for layout issues or performance bottlenecks.

## Security Considerations

- Be mindful of CSS injection vulnerabilities, especially when dealing with user-generated content or dynamic styling. Sanitize any data used in CSS expressions.

## Performance Guidelines

- Optimize CSS selectors for performance. Avoid deeply nested or overly complex selectors.
- Minify CSS for production.
- Consider using techniques like CSS sprites or icon fonts to reduce HTTP requests.

## Documentation Requirements

- Add comments to CSS files to explain complex styles or specific design choices.

## Common Pitfalls to Avoid

- Avoid using `!important` unless absolutely necessary.
- Don't hardcode colors, fonts, or spacing values directly in CSS. Use CSS variables instead.
- Don't create overly complex or specific selectors that are difficult to maintain.
- Don't duplicate CSS rules unnecessarily.

### Examples

**Good:**

```css
:root {
  --primary-color: #007bff;
  --font-size-base: 16px;
}

.button {
  background-color: var(--primary-color);
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: var(--font-size-base);
  padding: 10px 20px;
}
```

**Bad:**

```css
.btn {
  background: blue !important;
  border: none;
  border-radius: 5px;
  color: white;
  cursor: pointer;
  font-size: 16px;
  padding: 10px 20px;
}
```

## Preferred Libraries & Tools

- [TODO: List preferred CSS preprocessors (e.g., Sass, Less) or frameworks (e.g., Tailwind CSS, Bootstrap) if any]
- [TODO: Include reasoning for why certain libraries are preferred]

## Additional Context

- [TODO: Any project-specific quirks or special considerations.  For example, if a specific CSS methodology is employed.]
- [TODO: Links to relevant documentation or ADRs]
- [TODO: Team conventions or preferences, e.g. specific browser support matrix]

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.