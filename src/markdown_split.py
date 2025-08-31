from dataclasses import dataclass
from enum import Enum, auto
from typing import List


class TextType(Enum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()


@dataclass(frozen=True)
class TextNode:
    """A very small representation of a piece of inline text."""
    content: str
    type: TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode],
    delimiter: str,
    new_type: TextType,
) -> List[TextNode]:
    """
    Split any TEXT nodes in *old_nodes* on the given *delimiter* and wrap the
    resulting pieces in a node of type *new_type*.

    Parameters
    ----------
    old_nodes:
        The list of nodes to process.
    delimiter:
        A string that marks the start and end of the inline element
        (e.g. '**', '_' or '`').
    new_type:
        The TextType to use for the newly created nodes.

    Returns
    -------
    List[TextNode]
        A new list where each original TEXT node has been replaced by a
        sequence of alternating TEXT / *new_type* nodes.
    """
    if not delimiter:
        raise ValueError("delimiter must be non‑empty")

    result: List[TextNode] = []

    for node in old_nodes:
        # Only split TEXT nodes – other types are left untouched.
        if node.type != TextType.TEXT or delimiter not in node.content:
            result.append(node)
            continue

        parts = node.content.split(delimiter)

        # If the number of parts is odd, there was an unmatched delimiter
        # (e.g. "**bold") – treat it as plain text.
        if len(parts) % 2 == 1:
            result.append(TextNode(node.content, TextType.TEXT))
            continue

        # Re‑interleave the parts: part[0] TEXT,
        # part[1] NEW_TYPE, part[2] TEXT, ...
        for i, part in enumerate(parts):
            if part:                     # skip empty fragments
                result.append(TextNode(part, TextType.TEXT))

            if i < len(parts) - 1:
                # The next fragment is wrapped with the new type.
                inner = parts[i + 1]
                if inner:                 # skip empty fragments
                    result.append(TextNode(inner, new_type))

    return result
