# GitHub Copilot Instructions

This file provides custom instructions to GitHub Copilot when working in this repository.

## Project Context

**Project Name:** Google Drive Folder Copy Utility
**Description:** Python script to copy/paste folder contents using the Google Drive API.
**Tech Stack:** Python, Google Drive API

## Code Style & Conventions

### General Guidelines

- Follow PEP 8 style guidelines.
- Prioritize readability and maintainability.
- Use descriptive variable and function names.
- Comment complex logic.

### Python-Specific Guidelines

- Use type hints.
- Use `logging` module for logging, not `print`.
- Handle exceptions gracefully.

### File Organization

- Place credentials in a separate, non-committed file (e.g., `credentials.json`). Use environment variables or a configuration file for sensitive information.
- Group related functions within classes or modules.

**Example - Good:**

```python
def copy_folder(source_folder_id: str, destination_folder_id: str) -> None:
    """Copies the contents of a source folder to a destination folder.

    Args:
        source_folder_id: The ID of the source folder.
        destination_folder_id: The ID of the destination folder.
    """
    # Implementation details...
```

**Example - Bad:**

```python
def copy(x, y):
    # Copies stuff
    # Implementation details...
```

## Architecture Patterns

- Modular design: Break down the script into reusable functions and classes.
- Use the Google Drive API efficiently to minimize API calls.

## Testing Strategy

- Write unit tests using `unittest` or `pytest` to verify core functionality.
- Mock Google Drive API calls during testing.
- Test edge cases and error handling.

**Example:**

```python
import unittest
from unittest.mock import patch

# Example test using mock
class TestCopyFolder(unittest.TestCase):
    @patch('your_module.drive_service')  # Replace your_module and drive_service
    def test_copy_folder_success(self, mock_drive_service):
        # Setup mock return values
        # Call the function being tested
        # Assert expected behavior
        pass
```

## Security Considerations

- **Never commit `credentials.json` or any other files containing sensitive information.**
- Use environment variables or secure configuration management for API keys.
- Limit the scope of the Google Drive API credentials to only the necessary permissions.

## Performance Guidelines

- Batch API calls where possible to improve performance.
- Optimize file transfers for large folders.

## Documentation Requirements

- Document all functions and classes with docstrings.
- Update the README.md with instructions on how to set up and run the script.

## Common Pitfalls to Avoid

- Hardcoding API keys or credentials.
- Not handling API rate limits.
- Ignoring error conditions from the Google Drive API.
- Committing sensitive information to the repository.

## Preferred Libraries & Tools

- `google-api-python-client`: For interacting with the Google Drive API.
- `google-auth-httplib2`: For authenticating with Google services.
- `pytest`: For unit testing.
- `logging`: For logging.

## Additional Context

- Before running the script, ensure you have enabled the Google Drive API and created a service account with the necessary permissions.
- The script assumes that the destination folder exists.

---

**Note:** These instructions help GitHub Copilot provide more relevant and consistent suggestions. Update this file as project conventions evolve.