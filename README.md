# File Inventory CLI Tool

### Download the Script

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/filelister.git
   ```

   *(Replace `yourusername` with your actual GitHub username if applicable.)*

2. **Navigate to the Directory**:

   ```bash
   cd filelister
   ```

3. **Alternatively**, you can download the `list_files_cli.py` script directly from the repository.

## Usage

FileLister is designed to be straightforward and flexible. Below are guidelines on how to use the tool effectively.

### Basic Usage

To list all files in a single directory with default settings:

```bash
python3 list_files_cli.py /path/to/directory
```

This command will generate an output file named `file_list_{timestamp}.txt` in the current directory, containing all files found in the specified directory and its subdirectories, sorted by name in ascending order.

### Advanced Options

FileLister offers a range of command-line options to customize its behavior:

- **Specify Multiple Directories**:

  ```bash
  python3 list_files_cli.py /path/to/dir1 /path/to/dir2
  ```
  
- **Define a Custom Output File**:

  ```bash
  python3 list_files_cli.py /path/to/directory -o my_files.txt
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
  
- **Combine Multiple Options**:

  ```bash
  python3 list_files_cli.py /path/to/dir1 /path/to/dir2 -e .jpg .png --sort date --order asc --depth 1 -o images_list.txt
  ```

### Command-Line Arguments

| Argument            | Short Option | Description                                                                                                                                       | Default                       |
|---------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| `directories`       | N/A          | One or more directory paths to list files from.                                                                                                | **Required**                  |
| `-o`, `--output`    | `-o`         | Specify a custom name for the output file. If not provided, defaults to `file_list_{timestamp}.txt`.                                            | `file_list_{timestamp}.txt`   |
| `-e`, `--extensions`| `-e`         | Filter files by extensions. Provide one or more extensions (e.g., `.txt`, `.py`).                                                              | `None` (includes all files)    |
| `--sort`            | N/A          | Sort files by criteria: `name`, `size`, or `date`.                                                                                                | `name`                        |
| `--order`           | N/A          | Order of sorting: `asc` for ascending or `desc` for descending.                                                                                   | `asc`                         |
| `--depth`           | N/A          | Maximum depth for directory traversal. `0` means only the specified directories, `1` includes immediate subdirectories, etc. `-1` for unlimited.| `-1` (unlimited)              |

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
   python3 list_files_cli.py . -e .*
   ```

   - **Note**: To exclude hidden files, you can modify the script to skip files starting with a dot or adjust the extension filters accordingly.

## Output

The output is a plain text file containing the list of file paths that match the specified criteria. Each file path is on a separate line. At the end of the execution, the script prints a summary indicating the location of the output file and the total number of files listed.

**Example Output**:

```
File list has been written to 'file_list_1701234567.txt'.
Total number of files: 123
```

---
