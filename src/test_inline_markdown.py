import unittest
from re import T

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bold** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with a *italic* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_italic_multiword(self):
        node = TextNode(
            "This is text with a *italicized word* and *another*", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("italicized word", text_type_italic),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_extract_images(self):
        text = "This is a text with an ![image](path/to/image)"
        images = extract_markdown_images(text)
        self.assertListEqual([("image", "path/to/image")], images)

    def test_extract_links(self):
        text = "This is a text with a [link](http://example.com)"
        links = extract_markdown_links(text)
        self.assertListEqual([("link", "http://example.com")], links)

    def test_simple_text_with_one_image(self):
        node = TextNode(
            "This is text with an ![image](https://example.com/image1.png) and some more text.",
            text_type_text,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://example.com/image1.png"),
                TextNode(" and some more text.", text_type_text),
            ],
            result,
        )

    def test_with_multiple_images(self):
        node = TextNode(
            "This is text with an ![image1](https://example.com/image1.png) and another ![image2](https://example.com/image2.png)",
            text_type_text,
        )
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image1", text_type_image, "https://example.com/image1.png"),
                TextNode(" and another ", text_type_text),
                TextNode("image2", text_type_image, "https://example.com/image2.png"),
            ],
            result,
        )

    def test_with_no_images(self):
        node = TextNode("This is text with no images", text_type_text)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", text_type_text),
            ],
            result,
        )

    def test_simple_text_with_one_link(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and some more text.",
            text_type_text,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://example.com"),
                TextNode(" and some more text.", text_type_text),
            ],
            result,
        )

    def test_with_multiple_links(self):
        node = TextNode(
            "This is text with a [link1](https://example.com) and another [link2](https://example.com)",
            text_type_text,
        )
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link1", text_type_link, "https://example.com"),
                TextNode(" and another ", text_type_text),
                TextNode("link2", text_type_link, "https://example.com"),
            ],
            result,
        )

    def test_with_no_links(self):
        node = TextNode("This is text with no links", text_type_text)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", text_type_text),
            ],
            result,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
