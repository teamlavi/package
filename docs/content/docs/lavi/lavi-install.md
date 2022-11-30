---
id: lavi-install
title: Install LAVI
permalink: docs/lavi/install.html
---

Windows <br />
1. Download lavi-cli-windows-amd64.zip and extract files in a new folder of \<name\> <br />
2. Inside \<name\>, if there is not already a lavi.exe, rename lavi to lavi.exe <br />   
3. Type in Windows menu "Edit the system environment variables"; click <br /> 
4. Click "environment variables" to obtain popup <br />
5. Double click on "Path" in the top section <br />
6. Click "New" -> "Browse..." <br />
7. Locate and select \<name\>, which is the file you just created <br />
8. Go to powershell and run lavi.exe <br />

LAVI is a tool built to help uncover hidden vulnerabilities that can be nested deeply inside a project's dependency tree.

lavi [command]

| Command | Description |
| :---:   | :---:       |
  completion  Generate the autocompletion script for the specified shell
  go          Run LAVI against a go project
  help        Help about any command
  npm         Run LAVI against an npm project
  pip         Run LAVI against a python project (using pip)
  poetry      Run LAVI against a python project (using poetry)

Flags:
      --critical           Only show critical severity vulnerabilities. Can be used alongside [--high, --medium, --low]
  -h, --help               help for lavi
      --high               Only show high severity vulnerabilities. Can be used alongside [--critical, --medium, --low]
      --low                Only show low severity vulnerabilities. Can be used alongside [--critical, --high, --medium]
      --medium             Only show medium severity vulnerabilities. Can be used alongside [--critical, --high, --low]
      --no-scan            Ignore scanning the tree for vulnerabilities and only create the dependency tree
      --package string     Run lavi on a single package. If provided along with version, will default to running in single package mode. This will also disable the ui if flag is provided
  -s, --show               Show ui
      --version string     Run lavi on a single package. If provided along with package, will default to running in single package mode. This will also disable the ui if flag is provided
  -w, --write              Write tree to a file
      --write-with-vulns   When used with write, will include vulnerabilities in written tree