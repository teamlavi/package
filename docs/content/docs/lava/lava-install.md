---
id: lava-install
title: Install LAVA
permalink: docs/lava/install.html
---

LAVA install

## Mac
1. Download LAVA binaries from http://vocation.cs.umd.edu/downloads/
2. Open terminal and `cd` into the downloaded folder
3. From the folder run the following commands:
   (Enter your password if prompted)
   ```bash
   sudo chmod +x lava
   sudo mv lava /usr/local/bin/lava
   ```
4. Run `lava` The result will be one of the following cases:
   - If the result is LAVA usage information then LAVA is successfully installed
   - If a popup window appears saying `"lava" can't be opened because Apple cannot check it for malicious software` then select the `open` button 
   - If the result of the command is `-bash: /usr/local/bin/lava: Permission denied` then complete the following steps:
      1. Run `open /usr/local/bin`
      2. Scroll to find the file named `lava`, right click on it and select `Open`. 
      3. When the popup window appears asking if you're sure you want to open it select `Open`
      4. Close the opened window

   
## Windows
1. Download LAVA binaries from http://vocation.cs.umd.edu/downloads/
2. Extract zip into a new folder of \<name\>
3. Inside \<name\>, if there is not already a `lava.exe`, rename `lavi` to `lavi.exe`  
4. Type in Windows menu `Edit the system environment variables`; click 
5. Click "environment variables" to obtain popup 
6. Double-click on `Path` in the top section 
7. Click "New" -> "Browse..." 
8. Locate and select \<name\>, which is the file you just created 
9. Go to powershell and run lava.exe
