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

        # Open the file for writing, using the utf-8 character encoding
        with open(file_name, 'w', encoding='utf-8') as f:
            # Use os.walk to traverse the directory tree and get a list of all files
            for root, dirs, files in os.walk(directory):
                # Write the file paths to the file
                for file in files:
                    # excludes hidden files
                    if not file.startswith('.'):
                        f.write(os.path.join(root, file) + '\n')
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
