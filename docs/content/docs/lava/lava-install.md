---
id: lava-install
title: Install LAVA
permalink: docs/lava/install.html
---

LAVA install

NOTE: Make sure that you recieved the email confriming your LAVA access and an attachment to install LAVA before attempting install LAVA

## Mac
1. Download LAVA binaries using the atttachment provided in the email
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
1. Download LAVA binaries using the atttachment provided in the email
2. Create a `lava` folder in your `C:\` directory
3. Extract the `lava.exe` file from the zip to the `C:\lava` folder
4. Add `C:\lava` to your environment variables
   1. Search `Edit the system environment variables` in the Windows menu and click the first option
   2. In the window, click "environment variables" in the lower right
   3. In the new popup, double click `Path` in the top section
   4. Click `New` in the right side menu, and type in the folder you extracted `lava.exe` to (in this case, `C:\lava`)
   5. Click `Ok`, and close the popups
5. Open up powershell or command prompt, and run `lava`
