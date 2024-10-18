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
        argparse.Namespace: Parsed arguments containing directory, optional output file name,
                            file extensions for filtering, sorting criteria, and order.
    """
    parser = argparse.ArgumentParser(
        description="List all files within a directory and save their paths to a text file."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="Path to the directory to list files from."
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
        help="Filter files by extensions. Provide one or more extensions (e.g., .txt .py). Not comma separated"
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

def list_files(directory, output_file, extensions=None, sort_by='name', order='asc'):
    """
    Traverse the directory, list all files with optional filtering and sorting, and write their paths to the output file.

    Args:
        directory (str): The directory to traverse.
        output_file (str): The file to write the list of file paths.
        extensions (list, optional): List of file extensions to filter by.
        sort_by (str): Criterion to sort by ('name', 'size', 'date').
        order (str): Order of sorting ('asc' or 'desc').

    Returns:
        int: Total number of files listed.
    """
    files_list = []
    file_count = 0

    # Normalize extensions if provided
    if extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' for ext in extensions]

    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extensions:
                    file_ext = os.path.splitext(file)[1].lower()
                    if file_ext not in extensions:
                        continue
                file_path = os.path.join(root, file)
                file_info = get_file_info(file_path)
                if file_info:
                    files_list.append((file_path, file_info))
    except Exception as e:
        print(f"Error traversing directory '{directory}': {e}", file=sys.stderr)
        sys.exit(1)

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
    directory = args.directory
    provided_output = args.output
    extensions = args.extensions
    sort_by = args.sort
    order = args.order

    # Check if the provided directory exists and is accessible
    if not os.path.isdir(directory):
        print(f"Error: The directory '{directory}' does not exist or is not accessible.", file=sys.stderr)
        sys.exit(1)

    # Generate the output file name
    output_file = generate_output_filename(provided_output)

    # List files with filtering and sorting, then write to the output file
    total_files = list_files(directory, output_file, extensions, sort_by, order)

    print(f"File list has been written to '{output_file}'.")
    print(f"Total number of files: {total_files}")

if __name__ == "__main__":
        main()
