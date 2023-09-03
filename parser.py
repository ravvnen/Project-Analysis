import os
import re

regex_comment = r'(?:/\*(?:[^*]|(?:\*+[^*/]))*\*+/)|(?://.*)'
regex_comment_test = r'//.*'
regex_import = r'import\s+([a-zA-Z0-9_.]+);'
regex_import_solo = r'(?<=import\s)[a-zA-Z0-9_.*]+;'


def remove_comments(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        for line in content:
            match = re.search(regex_comment_test, line)
            if match:
                print(f"File: {file_path}, Import: {match.group()}")


def find_imports(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()
        for line in content:
            match = re.search(regex_import_solo, line)
            if match:
                print(f"File: {file_path}, Import: {match.group()}")


def main():
    # Replace with your folder path
    folder_path = '/Users/phillipravn/course-02242-examples'
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                # remove_comments(file_path)
                find_imports(file_path)


if __name__ == '__main__':
    main()
