# MOBA Team Management

## Overview

This repository contains the MOBA program, which can be run in two ways:

1. By using the pre-built executable file available in the `dist` folder.
2. By running the Python source code (`MOBA.py`) with Python installed on your system.

### **Option 1: Using the Pre-Built Executable**

* A Windows-compatible executable is provided in the `dist` folder.
* The executable was built using [PyInstaller](https://pyinstaller.org).

#### **Steps to Run the Executable**

1. Navigate to the `dist` folder in this repository.
2. Download the executable file (`MOBA.exe`).
3. Double-click on the executable to run the program.

> **Note:** If you prefer to build the executable yourself, you can follow the instructions in Option 2.

### **Option 2: Running the Source Code**

If you would rather run the program directly from the source code, follow these steps:

#### **Step 1: Install Python**

1. Visit the official [Python website](https://www.python.org/downloads/).
2. Download the latest version of Python for your operating system (Windows).
3. Run the installer and ensure that you check the option to add Python to your system PATH.
4. Complete the installation process.

#### **Step 2: Install Required Dependencies**

Open a terminal (Command Prompt or PowerShell) and install the required dependencies by running:

```bash
pip install tkinter json
```

#### **Step 3: Download the MOBA Source Code**

1. Navigate to this repository and locate the `MOBA.py` file.
2. Download the file to a folder on your computer.

#### **Step 4: Run the Program**

1. Double-click on the `MOBA.py` file to run it, or open a terminal in the folder containing `MOBA.py` and run:

   ```bash
   python MOBA.py
   ```

### Additional Notes

* The `dist` folder contains a pre-built executable for Windows users who prefer not to install Python or dependencies.
* The program relies on the following Python modules:
  * `tkinter`
  * `json`
  * `itertools`
* MacOS and Linux users can only use the source code as the executable is only available for Windows.

For any questions or issues, please create an issue in this repository. Thank you for feedback!
