import pytest

from markdown_split import (
    TextNode,
    TextType,
    split_nodes_delimiter,
)


def test_no_delimiters():
    node = TextNode("plain text", TextType.TEXT)
    assert split_nodes_delimiter([node], "**", TextType.BOLD) == [node]


def test_single_bold():
    node = TextNode("This is **bold** text.", TextType.TEXT)
    expected = [
        TextNode("This is ", TextType.TEXT),
        TextNode("bold", TextType.BOLD),
        TextNode(" text.", TextType.TEXT),
    ]
    assert split_nodes_delimiter([node], "**", TextType.BOLD) == expected


def test_multiple_bolds():
    node = TextNode("**a** **b** **c**", TextType.TEXT)
    expected = [
        TextNode("", TextType.TEXT),  # leading empty fragment
        TextNode("a", TextType.BOLD),
        TextNode(" ", TextType.TEXT),
        TextNode("b", TextType.BOLD),
        TextNode(" ", TextType.TEXT),
        TextNode("c", TextType.BOLD),
    ]
    assert split_nodes_delimiter([node], "**", TextType.BOLD) == expected


def test_italic():
    node = TextNode("_i_", TextType.TEXT)
    expected = [TextNode("", TextType.TEXT), TextNode("i", TextType.ITALIC)]
    assert split_nodes_delimiter([node], "_", TextType.ITALIC) == expected


def test_code_block():
    node = TextNode("code: `foo` bar", TextType.TEXT)
    expected = [
        TextNode("code: ", TextType.TEXT),
        TextNode("foo", TextType.CODE),
        TextNode(" bar", TextType.TEXT),
    ]
    assert split_nodes_delimiter([node], "`", TextType.CODE) == expected


def test_unmatched_delimiter():
    node = TextNode("unbalanced **bold", TextType.TEXT)
    # unmatched delimiters are treated as plain text
    assert split_nodes_delimiter([node], "**", TextType.BOLD) == [node]


def test_multiple_types():
    # run in order: bold first, then code – this mimics the “order matters” rule
    node = TextNode("**bold `code`** rest", TextType.TEXT)
    after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
    final = split_nodes_delimiter(after_bold, "`", TextType.CODE)

    expected = [
        TextNode("", TextType.TEXT),
        TextNode("bold ", TextType.ITALIC),   # because we didn't nest bold inside code
        TextNode("code", TextType.CODE),
        TextNode("", TextType.TEXT),
        TextNode(" rest", TextType.TEXT),
    ]
    assert final == expected


if __name__ == "__main__":
    pytest.main([__file__])