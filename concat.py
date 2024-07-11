import os

def load_gitignore(gitignore_path):
    ignored_paths = set()
    if os.path.isfile(gitignore_path):
        with open(gitignore_path, 'r') as gitignore:
            for line in gitignore:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignored_paths.add(line)
    return ignored_paths

def is_ignored(path, ignored_paths):
    for pattern in ignored_paths:
        if pattern.startswith('/'):
            pattern = pattern[1:]
        if pattern.endswith('/'):
            pattern = pattern[:-1]
        if pattern in path:
            return True
    return False

def concatenate_codebase_with_comments(src_directory, output_file, extensions, gitignore_path):
    ignored_paths = load_gitignore(gitignore_path)
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for subdir, _, files in os.walk(src_directory):
            for file in files:
                file_path = os.path.relpath(os.path.join(subdir, file), src_directory)
                if any(file.endswith(ext) for ext in extensions) and not is_ignored(file_path, ignored_paths):
                    full_file_path = os.path.join(src_directory, file_path)
                    with open(full_file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(f"\n\n# File: {file_path}\n\n")
                        outfile.write(infile.read())

src_directory = '/Users/aviz/flexibot'  # Replace with your codebase directory
output_file = 'all_code.txt'  # Replace with your desired output file path
extensions = ['.py', '.js', '.html', '.css']  # Add more extensions if needed

concatenate_codebase_with_comments(src_directory, output_file, extensions, '.gitignore')