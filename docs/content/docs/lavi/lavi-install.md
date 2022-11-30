---
id: lavi-install
title: Install LAVI
permalink: docs/lavi/install.html
---

LAVI install

## Mac
1. Download LAVI binaries
   - ARM if M1
   - AMD if non-M1
2. Open terminal and `cd` into the downloaded folder
3. From the folder run the following commands:
   (Enter your password if prompted)
   ```bash
   sudo chmod +x lavi
   sudo mv lavi /usr/local/bin/lavi
   ```
4. Run `lavi` The result will be one of the following cases:
   - If the result is LAVI usage information then LAVI is successfully installed
   - If a popup window appears saying `"lavi" can't be opened because Apple cannot check it for malicious software` then select the `open` button 
   - If the result of the command is `-bash: /usr/local/bin/lavi: Permission denied` then complete the following steps:
      1. Run `open /usr/local/bin`
      2. Scroll to find the file named `lavi`, right click on it and select `Open`. 
      3. When the popup window appears asking if you're sure you want to open it select `Open`
      4. Close the opened window

