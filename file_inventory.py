#!/usr/bin/env python3

import os
import time
import argparse
import sys
from datetime import datetime

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments containing directories, optional output file name,
                            file extensions for filtering, sorting criteria, order, and depth control.
    """
    parser = argparse.ArgumentParser(
        description="List all files within specified directories and save their paths to a text file."
    )
    parser.add_argument(
        "directories",
        type=str,
        nargs='+',
        help="Path(s) to the directory/directories to list files from."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Optional output file name. Defaults to 'file_list_{timestamp}.txt'."
    )
    parser.add_argument(
        "-e", "--extensions",
        type=str,
        nargs='*',
        default=None,
        help="Filter files by extensions. Provide one or more extensions not comma separated (e.g., .txt .py)."
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=['name', 'size', 'date'],
        default='name',
        help="Sort files by 'name', 'size', or 'date'. Default is 'name'."
    )
    parser.add_argument(
        "--order",
        type=str,
        choices=['asc', 'desc'],
        default='asc',
        help="Order of sorting: 'asc' for ascending or 'desc' for descending. Default is 'asc'."
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=-1,
        help="Maximum depth for directory traversal. 0 means only the specified directories, 1 includes immediate subdirectories, etc. Default is -1 (unlimited)."
    )
    return parser.parse_args()

def generate_output_filename(provided_name=None):
    """
    Generate the output file name.

    Args:
        provided_name (str, optional): The user-provided file name.

    Returns:
        str: The output file name ending with '.txt'.
    """
    if provided_name:
        if not provided_name.lower().endswith('.txt'):
            provided_name += '.txt'
        return provided_name
    else:
        timestamp = int(time.time())
        return f'file_list_{timestamp}.txt'

def get_file_info(file_path):
    """
    Retrieve file information needed for sorting.

    Args:
        file_path (str): The full path to the file.

    Returns:
        dict: Dictionary containing file name, size, and modification date.
    """
    try:
        stats = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'size': stats.st_size,
            'date': stats.st_mtime
        }
    except Exception as e:
        print(f"Error accessing file '{file_path}': {e}", file=sys.stderr)
        return None

def traverse_directory(directory, max_depth, current_depth=0):
    """
    Traverse the directory up to the specified depth.

    Args:
        directory (str): The directory to traverse.
        max_depth (int): Maximum depth to traverse. -1 for unlimited.
        current_depth (int, optional): Current depth level. Defaults to 0.

    Yields:
        str: File path.
    """
    if max_depth != -1 and current_depth > max_depth:
        return

    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file():
                    yield entry.path
                elif entry.is_dir(follow_symlinks=False):
                    yield from traverse_directory(entry.path, max_depth, current_depth + 1)
    except PermissionError as e:
        print(f"Permission denied: '{directory}'. Skipping...", file=sys.stderr)
    except Exception as e:
        print(f"Error accessing directory '{directory}': {e}", file=sys.stderr)

def list_files(directories, output_file, extensions=None, sort_by='name', order='asc', depth=-1):
    """
    Traverse the directories, list all files with optional filtering and sorting, and write their paths to the output file.

    Args:
        directories (list): List of directories to traverse.
        output_file (str): The file to write the list of file paths.
        extensions (list, optional): List of file extensions to filter by.
        sort_by (str): Criterion to sort by ('name', 'size', 'date').
        order (str): Order of sorting ('asc' or 'desc').
        depth (int): Maximum depth for directory traversal. -1 for unlimited.

    Returns:
        int: Total number of files listed.
    """
    files_list = []
    file_count = 0

    # Normalize extensions if provided
    if extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: The directory '{directory}' does not exist or is not accessible. Skipping...", file=sys.stderr)
            continue

        for file_path in traverse_directory(directory, depth):
            if extensions:
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext not in extensions:
                    continue  # Skip files that do not match the extensions
            file_info = get_file_info(file_path)
            if file_info:
                files_list.append((file_path, file_info))

    # Sorting
    reverse_order = True if order == 'desc' else False
    if sort_by == 'name':
        files_list.sort(key=lambda x: x[1]['name'].lower(), reverse=reverse_order)
    elif sort_by == 'size':
        files_list.sort(key=lambda x: x[1]['size'], reverse=reverse_order)
    elif sort_by == 'date':
        files_list.sort(key=lambda x: x[1]['date'], reverse=reverse_order)

    # Write to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for file_path, _ in files_list:
                f.write(file_path + '\n')
                file_count += 1
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)

    return file_count

def main():
    args = parse_arguments()
    directories = args.directories
    provided_output = args.output
    extensions = args.extensions
    sort_by = args.sort
    order = args.order
    depth = args.depth

    # Generate the output file name
    output_file = generate_output_filename(provided_output)

    # List files with filtering, sorting, and depth control, then write to the output file
    total_files = list_files(directories, output_file, extensions, sort_by, order, depth)

    print(f"File list has been written to '{output_file}'.")
    print(f"Total number of files: {total_files}")

if __name__ == "__main__":
    main()
