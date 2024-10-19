# File Inventory CLI Tool

## Download the Script

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/seanlongcc/file-inventory.git
   ```

2. **Navigate to the Directory**:

   ```bash
   cd file-inventory
   ```

3. **Alternatively**, you can download the `list_files_cli.py` script directly from the repository.

## Usage

### Basic Usage

To list all files in a single directory with default settings:

```bash
python3 list_files_cli.py /path/to/directory
```

This command will generate an output file named `file_list_{timestamp}.txt` in the current directory, containing all files found in the specified directory and its subdirectories, sorted by name in ascending order.

### Advanced Options

- **Specify Multiple Directories**:

  ```bash
  python3 list_files_cli.py /path/to/dir1 /path/to/dir2
  ```
  
- **Define a Custom Output File**:

  ```bash
  python3 list_files_cli.py /path/to/directory -o my_files.txt
  ```

- **Choose Output Format (Plain Text or HTML with Clickable Links)**:

  - **Plain Text**:

    ```bash
    python3 list_files_cli.py /path/to/directory --format txt
    ```

  - **HTML**:

    ```bash
    python3 list_files_cli.py /path/to/directory --format html -o my_files.html
    ```
  
- **Filter by File Extensions**:

  ```bash
  python3 list_files_cli.py /path/to/directory -e .py .txt .md
  ```
  
- **Sort by Size in Descending Order**:

  ```bash
  python3 list_files_cli.py /path/to/directory --sort size --order desc
  ```
  
- **Limit Directory Traversal Depth**:

  ```bash
  python3 list_files_cli.py /path/to/directory --depth 2
  ```
  
- **Skip Hidden Files and Directories**:

  ```bash
  python3 list_files_cli.py /path/to/directory --skip-hidden
  ```
  
- **Combine Multiple Options**:

  ```bash
  python3 list_files_cli.py /path/to/dir1 /path/to/dir2 -e .jpg .png --sort date --order asc --depth 1 --skip-hidden --format html -o images_list.html
  ```

### Command-Line Arguments

| Argument             | Short Option | Description                                                                                                                                       | Default                       |
|----------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| `directories`        | N/A          | One or more directory paths to list files from.                                                                                                | **Required**                  |
| `-o`, `--output`     | `-o`         | Specify a custom name for the output file. If not provided, defaults to `file_list_{timestamp}.txt` or `.html` based on the `--format` argument. | `file_list_{timestamp}.txt` or `.html` |
| `-f`, `--format`           | N/A          | Output file format: `txt` for plain text or `html` for HTML with clickable links.                                                                 | `txt`                         |
| `-e`, `--extensions` | `-e`         | Filter files by extensions. Provide one or more extensions (e.g., `.txt`, `.py`).                                                              | `None` (includes all files)    |
| `--sort`             | N/A          | Sort files by criteria: `none` for no sorting, `name`, `size`, or `date`.                                                                          | `none`                        |
| `--order`            | N/A          | Order of sorting: `asc` for ascending or `desc` for descending.                                                                                   | `asc`                         |
| `--depth`            | N/A          | Maximum depth for directory traversal. `0` means only the specified directories, `1` includes immediate subdirectories, etc. `-1` for unlimited.| `-1` (unlimited)              |
| `--skip-hidden`      | N/A          | Skip hidden files and directories (those starting with a dot `.`).                                                                                | `False`                       |
| `--contains`         | N/A          | Filter files to include only those whose names contain the specified substring.                                                                   | `None`                        |

### Examples

1. **List All Files in a Single Directory**:

   ```bash
   python3 list_files_cli.py /home/user/Documents
   ```

   - **Output**: `file_list_1701234567.txt` containing all files in `/home/user/Documents` and its subdirectories.

2. **List `.py` and `.txt` Files in Multiple Directories, Sorted by Size Descending**:

   ```bash
   python3 list_files_cli.py /home/user/projects /home/user/scripts -e .py .txt --sort size --order desc
   ```

   - **Output**: `file_list_1701234567.txt` containing `.py` and `.txt` files from both directories, sorted from largest to smallest.

3. **List Files with a Maximum Depth of 2, Saving to a Custom File**:

   ```bash
   python3 list_files_cli.py /var/log --depth 2 -o logs_list.txt
   ```

   - **Output**: `logs_list.txt` containing files in `/var/log` and its immediate two levels of subdirectories.

4. **List All Files in Current Directory, Excluding Hidden Files**:

   ```bash
   python3 list_files_cli.py . --skip-hidden
   ```

   - **Output**: `file_list_1701234567.txt` containing all non-hidden files in the current directory and its subdirectories.

5. **Generate an HTML File with Clickable Links**:

   ```bash
   python3 list_files_cli.py /home/user/Documents --format html -o my_files.html
   ```

   - **Output**: `my_files.html` containing a list of files with clickable links that open the files in their default applications.

---
