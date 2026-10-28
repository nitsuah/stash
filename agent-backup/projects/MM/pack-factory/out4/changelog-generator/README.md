# Changelog Generator
    git log --pretty=%s v1.0..HEAD | python changelog.py "v1.1.0" > entry.md
Turns conventional-commit subjects (`feat(api): add search`, `fix: crash on empty input`, `feat!: drop v1`) into grouped Markdown:
Breaking changes, Added, Fixed, Changed and more. Reads from stdin, so it also works with any list of lines. Plain Python 3.

Personal and commercial use. Do not resell or redistribute the files themselves.
