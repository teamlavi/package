---
id: lavi-install
title: Install LAVI
permalink: docs/lavi/install.html
---

LAVI install

## Mac or Linux

### Installation Prerequisites

#### The directory `/usr/local/bin` must exist
This can be checked by trying to cd into it.
Run `cd /usr/local/bin`.
If the directory is changed successfully then the folder exists. 
If the output is `cd: /usr/local/bin: No such file or directory` then run `sudo mkdir -p -m 775 /usr/local/bin` to create the directory.

#### `usr/local/bin` must be referenced in $PATH
This can be checked manually with `echo $PATH`, `:/usr/local/bin` should appear somewhere in the output.

If it is not run `export PATH=$PATH:/usr/local/bin` to add `/usr/local/bin` to `$PATH`

### Installation
1. Download LAVI from http://vocation.cs.umd.edu/downloads/ and unzip the folder
2. Open terminal and `cd` into the downloaded folder
3. From the folder run the following command (enter your password if prompted):
   `sudo mv lavi /usr/local/bin/lavi`
4. Run `lavi` The result will be one of the following cases:
   - If the result is LAVI usage information then LAVI is successfully installed
   - If a popup window appears saying `"lavi" can't be opened because Apple cannot check it for malicious software` then run the following steps:
     1. close the pop-up window
     2. Run `open /usr/local/bin`
     3. Scroll to find the file named `lavi`, right click on it and select `Open`. 
     4. When the popup window appears asking if you're sure you want to open it select `Open`
     5. Close the opened window

## Windows
1. Download LAVI binaries from http://vocation.cs.umd.edu/downloads/
2. Create a `lavi` folder in your `C:\` directory
3. Extract the `lavi.exe` file from the zip to the `C:\lavi` folder
4. Add `C:\lavi` to your environment variables
   1. Search `Edit the system environment variables` in the Windows menu and click the first option
   2. In the window, click "environment variables" in the lower right
   3. In the new popup, double click `Path` in the top section
   4. Click `New` in the right side menu, and type in the folder you extracted `lavi.exe` to (in this case, `C:\lavi`)
   5. Click `Ok`, and close the popups
5. Open up powershell or command prompt, and run `lavi`