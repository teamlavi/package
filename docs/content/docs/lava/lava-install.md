---
id: lava-install
title: Install LAVA
permalink: docs/lava/install.html
---

LAVA install

## Mac
1. Download LAVA binaries
   - ARM if M1
   - AMD if non-M1
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


---
id: lava-install
title: Install LAVA
permalink: docs/lava/install.html
---

Windows <br />
1. Download lava-cli-windows-amd64.zip and extract files in a new folder of \<name\> <br />
2. Inside \<name\>, if there is not already a lava.exe, rename lavi to lavi.exe <br />   
3. Type in Windows menu "Edit the system environment variables"; click <br /> 
4. Click "environment variables" to obtain popup <br />
5. Double click on "Path" in the top section <br />
6. Click "New" -> "Browse..." <br />
7. Locate and select \<name\>, which is the file you just created <br />
8. Go to powershell and run lava.exe <br />
