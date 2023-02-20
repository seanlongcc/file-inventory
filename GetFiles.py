import os
import time
from PyQt5 import QtWidgets, QtCore

# Create a new PyQt5 application
app = QtWidgets.QApplication([])

# Create a new PyQt5 window
window = QtWidgets.QWidget()

# Set the size of the window using the setGeometry() method
# The first two arguments are the x and y coordinates of the top-left corner of the window
# The last two arguments are the width and height of the window
window.setGeometry(100, 100, 250, 100)

# Set the title of the window using the setWindowTitle() method
window.setWindowTitle('File Lister')

# Create a layout for the window
layout = QtWidgets.QVBoxLayout()


# Create a text field for entering the directory
directory_field = QtWidgets.QLineEdit()
directory_field.setPlaceholderText('Enter directory')
layout.addWidget(directory_field)


# Create a text field for entering the file name
file_name_field = QtWidgets.QLineEdit()
file_name_field.setPlaceholderText('Enter file name (optional)')
layout.addWidget(file_name_field)

# Create a button for starting the file listing
list_button = QtWidgets.QPushButton('List files')
layout.addWidget(list_button)

# Create a progress bar for displaying the progress percentage
progress_bar = QtWidgets.QProgressBar()

# Set the minimum and maximum values for the progress bar
progress_bar.setMinimum(0)
progress_bar.setMaximum(100)

# Set the text format for displaying the progress percentage
# The '%v' placeholder will be replaced with the current progress value
progress_bar.setFormat('%v%')
layout.addWidget(progress_bar)

# Set the text to be visible inside the progress bar
progress_bar.setAlignment(QtCore.Qt.AlignCenter)

# Set progress bar to 0%
progress_bar.setValue(int(0))


def progressBar():
    # Reset progress bar
    progress_bar.setValue(int(0))
    # Gets the total number of files
    directory = directory_field.text()
    count = 0
    for root, dirs, files in os.walk(directory):
        # Write the file paths to the file
        for file in files:
            # excludes hidden files
            if not file.startswith('.'):
                count += 1
    return count


def list_files():
    # Get the directory and file name from the text fields
    directory = directory_field.text()
    file_name = file_name_field.text()
    if os.path.exists(directory) == True:
        # If no file name was entered, generate a unique file name using the current timestamp
        if not file_name:
            timestamp = int(time.time())
            file_name = f'file_list_{timestamp}.txt'
        else:
            # Append '.txt' to the file name if it is not already present
            if not file_name.endswith('.txt'):
                file_name += '.txt'

        # Get the total number of files
        total_entries = progressBar()
        # Counter for progress bar
        count = 0

        # Open the file for writing, using the utf-8 character encoding
        with open(file_name, 'w', encoding='utf-8') as f:
            # Use os.walk to traverse the directory tree and get a list of all files
            for root, dirs, files in os.walk(directory):
                # Write the file paths to the file
                for file in files:
                    # Excludes hidden files
                    # if not file.startswith('.'):
                    # Write the entry path to the file
                    f.write(os.path.join(root, file) + '\n')

                    # Increase counted file by one
                    count += 1

                    # Calculate the current progress as a percentage
                    progress = (count + 1) / total_entries * 100

                    # Convert the progress value to an integer before setting it on the progress bar
                    progress_bar.setValue(int(progress))

        # Print total number of files
        print(f"There are {total_entries} files.")

    else:
        # Handle the error
        print("The directory does not exist or you do not have permission to access it.")


# Connect the 'returnPressed' signal of the directory_field to the list_files function
directory_field.returnPressed.connect(list_files)

# Connect the 'returnPressed' signal of the file_name_field to the list_files function
file_name_field.returnPressed.connect(list_files)

# Connect the 'clicked' signal of the list_button to the list_files function
list_button.clicked.connect(list_files)

# Set the layout of the window
window.setLayout(layout)

# Show the window
window.show()

# Run the application
app.exec_()
