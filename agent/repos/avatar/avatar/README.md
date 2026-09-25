# Avatar Utils - Testing Jupyter Notebooks

This module provides testable Python utilities extracted from the DreamBooth Stable Diffusion notebook, enabling comprehensive test coverage while keeping the notebook workflow intact.

## Approach

Rather than refactoring the entire notebook, we:

1. **Extracted reusable functions** from the notebook into `avatar/utils.py`
2. **Created comprehensive tests** with 100% coverage (25 tests)
3. **Keep the notebook as-is** for Colab usage - no breaking changes

## Available Utilities

### Concepts Management

- `create_concepts_list()` - Generate training concepts configuration
- `save_concepts_json()` / `load_concepts_json()` - Persist concepts to disk
- `validate_concept_structure()` - Validate concept dictionaries

### Directory Management

- `create_instance_directories()` - Create training data directories
- `count_images_in_directory()` - Count training images
- `validate_image_count()` - Ensure optimal image count (3-10 images)

### Training Configuration

- `calculate_recommended_training_steps()` - Rule of thumb: 100 steps per image + 100 base
- `build_training_command()` - Generate accelerate launch command

## Usage in Notebook

You can now use these utilities in the Colab notebook:

```python
# Install the package (in Colab)
!pip install -e /content/gdrive/MyDrive/avatar

from avatar.utils import (
    create_concepts_list,
    save_concepts_json,
    calculate_recommended_training_steps,
    validate_image_count
)

# Create concepts automatically
concepts = create_concepts_list("nitsuah", "man")
save_concepts_json(concepts, "concepts_list.json")

# Validate your images
is_valid, count, msg = validate_image_count("/content/data/nitsuah")
print(msg)

# Calculate optimal training steps
steps = calculate_recommended_training_steps(count)
print(f"Recommended steps: {steps}")
```

## Testing

Run tests via Docker (recommended — no local Python required):

```bash
docker compose -f config/docker-compose.yml --profile test run --rm test
```

Or directly, from the **repo root** (the `tests/` directory is at the top level, not inside `avatar/`):

```bash
PYTHONPATH=. pytest tests/ --cov=avatar --cov-report=term-missing
```

All 25 tests pass with 100% coverage.

## Benefits

✅ **No notebook refactoring needed** - Keep using Colab  
✅ **100% test coverage** - Production-quality code  
✅ **Reusable utilities** - DRY principle  
✅ **CI/CD friendly** - Automated testing  
✅ **Future-proof** - Easy to extend or integrate into other tools

## Future Options

If you decide to refactor later:

1. Move more logic from notebook cells into utilities
2. Create a CLI tool using these utilities
3. Build a web interface with the same backend
4. Package for PyPI distribution

For now, enjoy the notebook workflow with enterprise-grade testing! 🚀
