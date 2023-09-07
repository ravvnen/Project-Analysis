
from tree_sitter import Language, Parser
import pygraphviz as pgv
import os

folder_path = 'C:\\Users\\phill\\GitHub\\Project-Analysis'

FILE = "./languages.so"  # the ./ is important
Language.build_library(FILE, ["tree-sitter-java"])
JAVA_LANGUAGE = Language(FILE, "java")
parser = Parser()
parser.set_language(JAVA_LANGUAGE)

with open("simple/Example.java", "rb") as f:
    tree = parser.parse(f.read())
# the tree is now ready for analysing
# print(tree.root_node.sexp())
G = pgv.AGraph(strict=False, directed=True)


def traverse(node, parent_class=None):

    if node.type == 'class_declaration':
        class_name = node.children[1].text
        G.add_node(class_name)

    if node.type == 'method_declaration':
        method_name = node.children[2].text
        G.add_node(method_name)
        G.add_edge(parent_class, method_name, label="has method")

    if node.type == 'field_declaration':
        field_name = node.children[1].text
        G.add_node(field_name)
        G.add_edge(parent_class, field_name, label="has field")

    for child in node.children:
        traverse(child, parent_class=class_name if node.type ==
                 'class_declaration' else parent_class)


# traverse(tree.root_node, parent_class=None)
# G.draw("imgettingpizzatonight.png", prog="dot")


def main():
    G = pgv.AGraph(strict=False, directed=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # checking only java files
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                traverse(tree.root_node, parent_class=None)

    # the visualization
    G.draw("imgettingpizzatonight.png", prog="dot")
