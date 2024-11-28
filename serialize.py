import os
import pathspec
from typing import List


def load_gitignore_patterns(gitignore_path):
    with open(gitignore_path, "r") as gitignore_file:
        gitignore_patterns = gitignore_file.read().splitlines()
    return pathspec.PathSpec.from_lines("gitwildmatch", gitignore_patterns)


def print_tree(root_dir: str, spec: pathspec.PathSpec, files_to_ignore: set, dirs_to_ignore: set, prefix: str = "") -> List[str]:
    """Generate a tree-like structure of the project directory."""
    tree_output = []
    
    # Get all items in directory
    items = os.listdir(root_dir)
    items = sorted(items)  # Sort items alphabetically
    
    # Filter items based on ignore rules
    items = [item for item in items 
            if not item.startswith(".") 
            and item not in files_to_ignore 
            and item not in dirs_to_ignore
            and (not spec or not spec.match_file(item))]
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        item_path = os.path.join(root_dir, item)
        relative_path = os.path.relpath(item_path, root_dir)
        
        # Choose the appropriate prefix characters
        current_prefix = "└── " if is_last else "├── "
        next_level_prefix = "    " if is_last else "│   "
        
        tree_output.append(f"{prefix}{current_prefix}{item}")
        
        if os.path.isdir(item_path):
            # Recursively process subdirectories
            tree_output.extend(
                print_tree(
                    item_path, 
                    spec, 
                    files_to_ignore, 
                    dirs_to_ignore, 
                    prefix + next_level_prefix
                )
            )
    
    return tree_output


def serialize_project_files(root_dir):
    gitignore_path = os.path.join(root_dir, ".gitignore")

    if os.path.exists(gitignore_path):
        spec = load_gitignore_patterns(gitignore_path)
    else:
        spec = None

    # Additional files and directories to ignore
    files_to_ignore = {
        "poetry.lock",
        "requirements.txt",
        "serialize.py",
        "openapi.yaml"
    }
    dirs_to_ignore = {"misc", "tests"}

    # Generate tree structure
    tree_output = print_tree(root_dir, spec, files_to_ignore, dirs_to_ignore)
    
    serialized_output = []
    
    # Add tree structure to output
    serialized_output.append("Project Tree:\n")
    serialized_output.append(".\n")  # Root directory marker
    serialized_output.extend(tree_output)
    serialized_output.append("\n\nFile Contents:\n")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_dir = os.path.relpath(dirpath, root_dir)

        # Skip hidden directories (starting with a dot) and directories to ignore
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in dirs_to_ignore]

        # Check if the directory is ignored
        if spec and spec.match_file(relative_dir):
            continue

        for filename in filenames:
            # Skip hidden files and specific files to ignore
            if filename.startswith(".") or filename in files_to_ignore:
                continue

            relative_file_path = os.path.join(relative_dir, filename)

            # Check if the file is ignored by .gitignore
            if spec and spec.match_file(relative_file_path):
                continue

            file_path = os.path.join(dirpath, filename)

            with open(file_path, "r") as file:
                file_content = file.read()

                # Add the file path and its content to the serialized output
                serialized_output.append(f"{relative_file_path}:\n\n{file_content}\n")

    return "\n".join(serialized_output)


project_intro = """We are working on a project where we serve entire desktop virtual envs in the cloud alongside tools to control the desktop by AI Agents. This is the linux basic environment."""

root_directory = "./"
serialized_data = (
    project_intro
    + "\n\n<project_state>\n\n"
    + serialize_project_files(root_directory)
    + "</project_state>"
)
print(serialized_data)
