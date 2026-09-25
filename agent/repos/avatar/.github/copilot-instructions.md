# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Avatar
**Description:** This project likely involves creating and manipulating avatar representations using Jupyter Notebooks. Specific details are currently unavailable.
**Tech Stack:** Jupyter Notebook, potentially other Python libraries (e.g., NumPy, Pandas, Matplotlib, Pillow).

## Code Style & Conventions

### General Guidelines

- Follow PEP 8 style guidelines for Python.
- Prioritize readability and maintainability.
- Use descriptive variable and function names.
- Add comments to explain complex logic.
- Ensure notebooks are well-structured with clear headings and explanations.

### Jupyter Notebook Specifics

- Organize notebooks into logical sections with Markdown headings.
- Use Markdown cells to explain the purpose of code cells.
- Keep code cells concise and focused on a single task.
- Avoid large, monolithic notebooks; consider breaking them down into smaller, more manageable files.
- Restart kernel and run all cells before committing to ensure reproducibility.

### File Organization

- Organize notebooks into directories based on functionality (e.g., `data_processing/`, `visualization/`).
- Include a `README.md` file in each directory explaining its purpose and contents.
- Store data files in a dedicated `data/` directory.
- Keep supporting Python modules in a `src/` directory.

## Testing Strategy

- Although formal unit testing may not be common in Jupyter Notebook projects, strive for:
    - **Informal testing:** Include assertions or print statements to verify the correctness of code within notebooks.
    - **Reproducibility:** Ensure that running the notebook from start to finish produces the expected results.
    - **Input Validation:** Check the format and validity of input data.

## Commit Conventions

- Use clear and concise commit messages following the Conventional Commits format.
- Example: `feat: Add function to generate random avatars`
- Reference relevant issues in commit messages (e.g., `Fixes #123`).
- Keep commits small and focused on a single change.

## Common Pitfalls to Avoid

- Avoid hardcoding file paths or sensitive information.
- Don't commit large data files directly to the repository; use a data storage solution.
- Don't leave unused code or variables in notebooks.
- Don't neglect to comment and document your code.
- Avoid using global variables excessively.

## Examples

### Good Change

```python
# Calculate the average pixel value of an image
def calculate_average_pixel_value(image_path):
  """
  Calculates the average pixel value of a grayscale image.

  Args:
    image_path: The path to the image file.

  Returns:
    The average pixel value as a float.
  """
  from PIL import Image
  import numpy as np

  try:
    img = Image.open(image_path).convert('L') # Convert to grayscale
    img_array = np.array(img)
    average_pixel_value = np.mean(img_array)
    return average_pixel_value
  except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}")
    return None

# Example Usage
image_file = "data/example_avatar.png"
avg_pixel_value = calculate_average_pixel_value(image_file)

if avg_pixel_value is not None:
  print(f"Average pixel value: {avg_pixel_value}")
```

### Bad Change

```python
#calculate avg
def avg(x):
  i = Image.open(x).convert('L')
  a = np.array(i)
  return np.mean(a)
```

**Explanation of Bad Change:**

- Vague function and variable names (`avg`, `x`, `i`, `a`).
- Missing docstring explaining the function's purpose and arguments.
- No error handling for potential file not found errors.
- Lack of comments to explain the code's logic.

## Additional Context

- TODO: Link to relevant documentation or resources.
- TODO: Add any project-specific instructions or conventions.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.