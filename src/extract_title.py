def extract_title(markdown: str) -> str:
    """
    Extracts the first H1 (# ...) line from markdown and returns its text.
    Raises ValueError if no H1 is found.
    """
    for line in markdown.splitlines():
        if line.startswith("# "):  # Only a single leading '#'
            return line.lstrip("#").strip()
    raise ValueError("No H1 title found in markdown")
