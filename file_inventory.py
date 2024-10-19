#!/usr/bin/env python3

import os
import time
import argparse
import sys
import html  # For escaping HTML characters
from urllib.parse import quote  # For URL encoding

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments containing directories, optional output file name,
                            file extensions for filtering, sorting criteria, order, depth control,
                            output format, an option to skip hidden files, and a substring to filter by.
    """
    parser = argparse.ArgumentParser(
        description="List all files within specified directories and save their paths to a text or HTML file."
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
        help="Optional output file name. Defaults to 'file_list_{timestamp}.txt' or '.html' based on the '--format' argument."
    )
    parser.add_argument(
        "-f","--format",
        type=str,
        choices=['txt', 'html'],
        default='txt',
        help="Output file format: 'txt' for plain text or 'html' for HTML with clickable links. Default is 'txt'."
    )
    parser.add_argument(
        "-e", "--extensions",
        type=str,
        nargs='*',
        default=None,
        help="Filter files by extensions. Provide one or more extensions, not comma separated (e.g., .txt .py)."
    )
    parser.add_argument(
        "--sort",
        type=str,
        choices=['none', 'name', 'size', 'date'],
        default='none',
        help="Sort files by criteria: 'none' for no sorting, 'name', 'size', or 'date'. Default is 'none'."
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
    parser.add_argument(
        "--skip-hidden",
        action='store_true',
        help="Skip hidden files and directories (those starting with a dot '.')."
    )
    
    parser.add_argument(
        "--contains",
        type=str,
        default=None,
        help="Filter files to include only those whose names contain the specified substring."
    )
    return parser.parse_args()

def generate_output_filename(provided_name=None, output_format='txt'):
    """
    Generate the output file name.

    Args:
        provided_name (str, optional): The user-provided file name.
        output_format (str): The desired output format ('txt' or 'html').

    Returns:
        str: The output file name with the appropriate extension.
    """
    if provided_name:
        _, ext = os.path.splitext(provided_name)
        if ext.lower() not in ['.txt', '.html']:
            provided_name += f'.{output_format}'
        return provided_name
    else:
        timestamp = int(time.time())
        return f'file_list_{timestamp}.{output_format}'

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

def path_to_file_url(path):
    """
    Convert a file system path to a properly formatted file URL.

    Args:
        path (str): The file system path.

    Returns:
        str: The file URL.
    """
    if os.name == 'nt':
        # Replace backslashes with forward slashes for Windows paths
        path = path.replace('\\', '/')
        # Remove any leading slashes to prevent 'file:////' URLs
        path = path.lstrip('/')
        # URL-encode the path to handle spaces and special characters
        return f'file:///{quote(path)}'
    else:
        # For Unix-like systems, prepend 'file://'
        return f'file://{quote(path)}'

def traverse_directory(directory, max_depth, skip_hidden, current_depth=0):
    """
    Traverse the directory up to the specified depth.

    Args:
        directory (str): The directory to traverse.
        max_depth (int): Maximum depth to traverse. -1 for unlimited.
        skip_hidden (bool): Whether to skip hidden files and directories.
        current_depth (int, optional): Current depth level. Defaults to 0.

    Yields:
        str: File path.
    """
    if max_depth != -1 and current_depth > max_depth:
        return

    try:
        with os.scandir(directory) as it:
            for entry in it:
                if skip_hidden and entry.name.startswith('.'):
                    continue  # Skip hidden files and directories
                if entry.is_file():
                    yield entry.path
                elif entry.is_dir(follow_symlinks=False):
                    yield from traverse_directory(entry.path, max_depth, skip_hidden, current_depth + 1)
    except PermissionError:
        print(f"Permission denied: '{directory}'. Skipping...", file=sys.stderr)
    except Exception as e:
        print(f"Error accessing directory '{directory}': {e}", file=sys.stderr)

def list_files(directories, output_file, extensions=None, sort_by='name', order='asc',
              depth=-1, skip_hidden=False, output_format='txt', contains=None):
    """
    Traverse the directories, list all files with optional filtering and sorting, and write their paths to the output file.

    Args:
        directories (list): List of directories to traverse.
        output_file (str): The file to write the list of file paths.
        extensions (list, optional): List of file extensions to filter by.
        sort_by (str): Criterion to sort by ('none', 'name', 'size', 'date').
        order (str): Order of sorting ('asc' or 'desc').
        depth (int): Maximum depth for directory traversal. -1 for unlimited.
        skip_hidden (bool): Whether to skip hidden files and directories.
        output_format (str): The desired output format ('txt' or 'html').
        contains (str, optional): Substring to filter file names.

    Returns:
        int: Total number of files listed.
    """
    files_list = []
    total_files = 0

    # Normalize extensions if provided
    if extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

    for directory in directories:
        if not os.path.isdir(directory):
            print(f"Warning: The directory '{directory}' does not exist or is not accessible. Skipping...", file=sys.stderr)
            continue

        for file_path in traverse_directory(directory, depth, skip_hidden):
            file_name = os.path.basename(file_path)
            
            # Apply --contains filter if specified
            if contains and contains.lower() not in file_name.lower():
                continue  # Skip files that do not contain the specified substring
            
            if extensions:
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext not in extensions:
                    continue  # Skip files that do not match the extensions
            file_info = get_file_info(file_path)
            if file_info:
                files_list.append((file_path, file_info))
                total_files += 1

    # Sorting
    if sort_by != 'none':
        reverse_order = True if order == 'desc' else False
        if sort_by == 'name':
            files_list.sort(key=lambda x: x[1]['name'].lower(), reverse=reverse_order)
        elif sort_by == 'size':
            files_list.sort(key=lambda x: x[1]['size'], reverse=reverse_order)
        elif sort_by == 'date':
            files_list.sort(key=lambda x: x[1]['date'], reverse=reverse_order)
    # If sort_by is 'none', retain the original traversal order

    # Write to output file based on the chosen format
    try:
        if output_format == 'html':
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('<!DOCTYPE html>\n<html lang="en">\n<head>\n')
                f.write('<meta charset="UTF-8">\n')
                f.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                f.write(f'<title>File List - {time.strftime("%Y-%m-%d %H:%M:%S")}</title>\n')
                f.write('</head>\n<body>\n')
                f.write(f'<h1>Total number of files: {total_files}</h1>\n')
                f.write('<ul>\n')
                for file_path, _ in files_list:
                    # Escape HTML characters and convert Windows paths to file URLs
                    escaped_path = html.escape(file_path)
                    file_url = path_to_file_url(file_path)
                    f.write(f'  <li><a href="{file_url}">{escaped_path}</a></li>\n')
                f.write('</ul>\n')
                f.write('</body>\n</html>')
        else:
            with open(output_file, 'w', encoding='utf-8') as f:
                # Write total number of files as the first line
                f.write(f"Total number of files: {total_files}\n")
                # Write each file path on a new line
                for file_path, _ in files_list:
                    f.write(file_path + '\n')
    except Exception as e:
        print(f"Error writing to file '{output_file}': {e}", file=sys.stderr)
        sys.exit(1)

    return total_files

def main():
    args = parse_arguments()
    directories = args.directories
    provided_output = args.output
    extensions = args.extensions
    sort_by = args.sort
    order = args.order
    depth = args.depth
    skip_hidden = args.skip_hidden
    output_format = args.format
    contains = args.contains  # Capture the --contains argument

    # Generate the output file name with appropriate extension
    output_file = generate_output_filename(provided_output, output_format)

    # List files with filtering, sorting, depth control, hidden files option, and --contains filter, then write to the output file
    total_files = list_files(directories, output_file, extensions, sort_by, order, depth, skip_hidden, output_format, contains)

    print(f"File list has been written to '{output_file}'.")
    print(f"Total number of files: {total_files}")

if __name__ == "__main__":
    main()
