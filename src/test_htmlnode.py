import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph.")
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>This is a paragraph.</p>")
        self.assertEqual(
            node1.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


class TestParentNode(unittest.TestCase):
    # Test nesting ParentNode objects inside one another
    def test_to_html(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a paragraph."),
                ParentNode(
                    "a",
                    [LeafNode("span", "Click me!")],
                    {"href": "https://www.google.com"},
                ),
            ],
        )
        expected_output = (
            '<div><p>This is a paragraph.</p><a href="https://www.google.com">'
            "<span>Click me!</span></a></div>"
        )
        self.assertEqual(node.to_html(), expected_output)

    # Creating multiple levels of nesting
    def test_to_html_multiple_levels(self):
        node = ParentNode(
            "div",
            [
                LeafNode("p", "This is a paragraph."),
                ParentNode(
                    "a",
                    [
                        LeafNode("span", "Click me!"),
                        ParentNode(
                            "div",
                            [LeafNode("p", "This is another paragraph.")],
                            {"class": "container"},
                        ),
                    ],
                    {"href": "https://www.google.com"},
                ),
            ],
        )
        expected_output = (
            '<div><p>This is a paragraph.</p><a href="https://www.google.com">'
            '<span>Click me!</span><div class="container"><p>This is another paragraph.</p>'
            "</div></a></div>"
        )
        self.assertEqual(node.to_html(), expected_output)

    # Testing for invalid HTML: no tag
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "This is a paragraph.")])
        with self.assertRaises(ValueError):
            node.to_html()

    # Testing for invalid HTML: no children
    def test_to_html_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    # Test multiple siblings ParentNode objects inside another ParentNode
    def test_to_html_multiple_siblings(self):
        node = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode("span", "This is a span.")]),
                ParentNode("p", [LeafNode("span", "This is another span.")]),
            ],
        )
        expected_output = "<div><p><span>This is a span.</span></p><p><span>This is another span.</span></p></div>"
        self.assertEqual(node.to_html(), expected_output)

    # Test if props_to_html converts properties correctly
    def test_props_to_html(self):
        node = ParentNode(
            "div", [LeafNode("p", "This is a paragraph.")], {"class": "container"}
        )
        self.assertEqual(node.props_to_html(), ' class="container"')


if __name__ == "__main__":
    unittest.main()
