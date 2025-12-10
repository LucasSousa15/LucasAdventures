import os
import re

def remove_comments(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    in_string = False
    string_char = None

    for line in lines:
        cleaned_line = ""
        i = 0
        while i < len(line):
            char = line[i]

            if not in_string:
                if char in ('"', "'"):
                    in_string = True
                    string_char = char
                    cleaned_line += char
                elif char == '#':
                    break
                else:
                    cleaned_line += char
            else:
                cleaned_line += char
                if char == string_char and (i == 0 or line[i-1] != '\\'):
                    in_string = False
            i += 1

        cleaned_lines.append(cleaned_line.rstrip() + '\n' if cleaned_line.strip() else '\n')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                remove_comments(file_path)
                print(f"Cleaned: {file_path}")

process_directory("game")
process_directory(".")

for file in ["main.py", "clean.py", "text_proportions.py"]:
    if os.path.exists(file):
        remove_comments(file)
        print(f"Cleaned: {file}")

print("All comments removed!")
