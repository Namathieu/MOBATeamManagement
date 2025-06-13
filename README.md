# MOBA Team Management

## Overview

This repository contains the MOBA program, which can be run in two ways:

1. By using the pre-built executable file available in the `dist` folder.  
2. By running the Python source code (`MOBA.py`) with Python installed on your system.

---

## Option 1: Using the Pre-Built Executable

- A Windows-compatible executable is provided in the `dist` folder.  
- The executable was built using [PyInstaller](https://pyinstaller.org).

### Steps to Run the Executable

1. Navigate to the `dist` folder in this repository.  
2. Download the executable file (`MOBA.exe`).  
3. Verify the SHA256 checksum of the downloaded executable (instructions below).  
4. Double-click on the executable to run the program.

> **Note:** If you encounter warnings from your antivirus software, this can happen with PyInstaller executables. You may need to whitelist the file or run it with administrator privileges.

---

## Option 2: Running the Source Code

If you prefer to run the program from the source code, follow these steps:

### Step 1: Install Python

1. Visit the official [Python website](https://www.python.org/downloads/).  
2. Download the latest version of Python for your operating system (Windows, macOS, or Linux).  
3. Run the installer:  
   - **Windows:** Make sure to check **Add Python to PATH** during installation.  
   - **macOS/Linux:** Python is often pre-installed, but install or update it if necessary.  
4. Complete the installation.

### Step 2: Install Required Dependencies

Open a terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
pip install tkinter
```

> **Note:**  
> - The `json` and `itertools` modules are included in Python's standard library; no installation needed.  
> - On some Linux distributions, you may need to install `tkinter` separately via your package manager, e.g.,  
>   ```bash
>   sudo apt-get install python3-tk
>   ```

### Step 3: Download the MOBA Source Code

1. Navigate to this repository and download the `MOBA.py` file.  
2. Save it to a folder on your computer.

### Step 4: Run the Program

- Double-click on `MOBA.py` (if your OS is configured to run `.py` files), or  
- Open a terminal in the folder containing `MOBA.py` and run:

```bash
python MOBA.py
```

---

## Verifying File Integrity with SHA256 Checksum

To ensure the executable or source code file has not been tampered with, verify the SHA256 checksum against the published checksum value:

**Windows (PowerShell):**

```powershell
Get-FileHash -Algorithm SHA256 path\to\MOBA.exe
```

**macOS/Linux (Terminal):**

```bash
shasum -a 256 path/to/MOBA.exe
```

Compare the output hash with the checksum provided in the repository’s release notes or documentation.

---

## Troubleshooting & FAQs

**Q: The executable won’t run or shows an error?**  
- Make sure you downloaded the full executable file from the `dist` folder.  
- Temporarily disable antivirus or add an exception if it blocks the executable.  
- Run the executable as administrator.

**Q: I get a `ModuleNotFoundError` running the source code?**  
- Check that you installed all required Python modules (`tkinter`).  
- On Linux, install `tkinter` using your distro’s package manager.

**Q: Does this program work on macOS or Linux?**  
- The pre-built executable is only available for Windows.  
- macOS and Linux users must run from source code.

**Q: How do I build the executable myself?**  
- Install [PyInstaller](https://pyinstaller.org).  
- Run:  

```bash
pyinstaller --onefile MOBA.py
```

- The output executable will be in the `dist` folder.

---

## Supported Platforms

| Platform | Executable Available | Run from Source Code |
| -------- | -------------------- | -------------------- |
| Windows  | Yes                  | Yes                  |
| macOS    | No                   | Yes                  |
| Linux    | No                   | Yes                  |

---

## Contact & Support

If you encounter any issues or have questions, please open an issue in this repository. Your feedback is appreciated!

---