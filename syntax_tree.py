from tree_sitter import Language, Parser
import graphviz as pgv

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
        class_name = node.children[0].value
        print(parent_class)
        G.add_node(class_name)

    if node.type == 'method_declaration':
        method_name = node.children[1].value

    if node.type == 'field_declaration':
        field_name = node.children[1].value

    for child in node.children:
        traverse(child, parent_class=class_name if node.type ==
                 'class_declaration' else parent_class)


traverse(tree.root_node)
