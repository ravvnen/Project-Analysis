import os
import re
import networkx as nx
import matplotlib.pyplot as plt

# phil
folder_path = 'C:\\Users\\phill\\GitHub\\Project-Analysis'

#luchas
#folder path = 'Luchas-path'


unique_imports = set()
regex_comment = r'(?:/\*(?:[^*]|(?:\*+[^*/]))*\*+/)|(?://.*)'
regex_import = r'(?<=import\s)[a-zA-Z0-9_.*]+;'
patterns = [r'\bString\b', r'\bSystem\b', r'\bObject\b', regex_import]

implicit_map = {
    
    'Object' : 'java.lang.Object',
    'String' : 'java.lang.String',
    'System' : 'java.lang.System',
}

def remove_comments(text):
    
    # utilizing in-memory modification to remove comments before looking for imports 
    return re.sub(regex_comment, '', text)
        
def find_imports(file_path, G):
    with open(file_path, 'r') as file:
        content = file.read()
        content_cleaned = remove_comments(content)
        
        # going through all the patterns in patterns list
        for pattern in patterns:
            for match in re.finditer(pattern, content_cleaned):
                imported_class = match.group().strip()
                
                # Qualify the import if it is an implicit one like System, String, Object
                imported_class = qualify_implicit_import(imported_class)
                
                # Create a tuple for the current file_path and imported_class
                current_tuple = (file_path, imported_class)
                
                parse_import = imported_class.split('.')
                
                # Go through a "dotted" import, and create edgs between each 
                for i in range(len(parse_import)):
                    parent_import = '.'.join(parse_import[:i])
                    child_import = '.'.join(parse_import[:i+1])
                    
                    if parent_import:
                        G.add_edge(parent_import, child_import)
                        
                # Check if the tuple is unique
                if current_tuple not in unique_imports:
                    
                    # If unique, we add it to the set
                    unique_imports.add(current_tuple)
                    
                    file_path = simplify_filepath(file_path)
                    G.add_edge(file_path, imported_class)
                    print(f"File: {file_path}, Import: {imported_class}")

# Removes the whole path for the file, and just keeps the file-name
def simplify_filepath(file_path):
    parse_filepath = file_path.split('\\')[-1]
    return parse_filepath
                  
# Checks if a import found qualifies as implicitly imported                                  
def qualify_implicit_import(imported_class):
    
    # find the value corresponding to the key in the implicit_map dictionary
    return implicit_map.get(imported_class, imported_class)

def setup_graph(G):
    pos = nx.spring_layout(G) 
    
    # with networkx, each index in the list is corresponding to the color of that node in the G.nodes 
    node_colors = []
    edge_colors = []
    for node in G.nodes:
        if node.endswith('.java'):
            node_colors.append("red")
        else:
            node_colors.append("blue")
            
    for edge in G.edges:
        source_node, _ = edge
        if source_node.endswith('.java'):
            edge_colors.append('green')
        else:
            edge_colors.append('black')
            
            
    nx.draw(G, pos, with_labels=True, font_size=8, node_size=50, arrows=True, arrowsize=10, node_color = node_colors, edge_color = edge_colors)
    plt.show()

    
def main():
    G = nx.DiGraph()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            
            # checking only java files
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                find_imports(file_path, G)
        
                
    # the visualization
    setup_graph(G)


if __name__ == '__main__':
    main()
