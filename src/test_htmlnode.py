import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_none(self):
        node = HTMLNode()
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)

    def test_props_to_html_empty(self):
        node = HTMLNode(props={})
        expected_output = ""
        self.assertEqual(node.props_to_html(), expected_output)