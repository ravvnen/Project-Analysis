import os
import re

# phil
folder_path = 'C:\\Users\\phill\\GitHub\\Project-Analysis'

#luchas
#folder path = 'Luchas-path'

regex_comment = r'(?:/\*(?:[^*]|(?:\*+[^*/]))*\*+/)|(?://.*)'
regex_import = r'import\s+([a-zA-Z0-9_.]+);'
regex_import_solo = r'(?<=import\s)[a-zA-Z0-9_.*]+;'


def remove_comments(text):
    return re.sub(regex_comment, '', text)


def find_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        content_cleaned = remove_comments(content)
        for match in re.finditer(regex_import_solo, content_cleaned):
            if match:
                print(f"File: {file_path}, Import: {match.group()}")


def main():
    # Replace with your folder path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                remove_comments(file_path)
                find_imports(file_path)


if __name__ == '__main__':
    main()
