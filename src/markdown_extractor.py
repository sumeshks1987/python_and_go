# markdown_extractor.py

import re
from typing import List, Tuple


def extract_markdown_links(txt: str) -> List[Tuple[str, str]]:
    """
    Return a list of all Markdown links in ``txt``.
    Each element is a tuple (link_text, url).

    Example
    -------
    >>> txt = "[Python site](https://python.org) and [Docs](/docs)"
    >>> extract_markdown_links(txt)
    [('Python site', 'https://python.org'), ('Docs', '/docs')]
    """
    #   $           : literal '['
    #   ([^$]+)     : capture group 1 – one or more chars that are NOT ']'
    #   $           : literal ']'
    #   $           : literal '('
    #   ([^)]+?)     : capture group 2 – non‑greedy, one or more chars that are NOT ')'
    #   $           : literal ')'
    link_pattern = r'$([^$]+)$$([^)]+?)$'
    return re.findall(link_pattern, txt, flags=re.DOTALL)


def extract_markdown_images(txt: str) -> List[Tuple[str, str]]:
    """
    Return a list of all Markdown images in ``txt``.
    Each element is a tuple (alt_text, url).

    Example
    -------
    >>> txt = "![logo](http://example.org/logo.svg)"
    >>> extract_markdown_images(txt)
    [('logo', 'http://example.org/logo.svg')]
    """
    #   !$          : literal '!['
    #   ([^$]+)     : capture group 1 – one or more chars that are NOT ']'
    #   $           : literal ']'
    #   $           : literal '('
    #   ([^)]+?)     : capture group 2 – non‑greedy, one or more chars that are NOT ')'
    #   $           : literal ')'
    image_pattern = r'!$([^$]+)$$([^)]+?)$'
    return re.findall(image_pattern, txt, flags=re.DOTALL)
