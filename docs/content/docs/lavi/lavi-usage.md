---
id: lavi-usage
title: LAVI Usage
permalink: docs/lavi/usage.html
---

LAVI is a tool built to help uncover hidden vulnerabilities that can be nested deeply inside a project's dependency tree.

## General Usage:

    lavi [command] --Flags

## Example commands:
    
    # Simple command to run Lavi on an node project. Make sure in the directory with the package-lock.json file
    # In this example the npm command tells lavi you are working in npm
    # The flag -s tells lavi to open up the UI element after running lavi
    
    lavi npm --show

    # This is an example with multiple flags lavi will only flag severities that it gets from the cve database
    # that are filtered under critical or high danger
    
    lavi npm --critical --high

    # This example is using the pip command if you would like to run lavi on a python project
    # The severity tags work as usual so only low severity  vulnerabilities ignored and show pops the UI 
    # write will write a tree to a file that will be available for the user to use and since write-with-vulns is used with 
    # write command, lavi will also include vulnerabilities in the written tree file
    
    lavi pip --critical --high --medium -show -write -write-with-vulns
<br><br>

Available Commands:
 | Commands: | Description: |
 | ----------- | - | 
 | completion | Generate the autocompletion script for the specified shell | 
| help |       Help about any command and get description of what each command does|
| npm  |       Run LAVI against an npm project by running the command when in the project directory|
| pip  |       Run LAVI against a python project (using pip) by running the command when in the project directory|
| poetry   |   Run LAVI against a python project (using poetry) to build the package-lock.json if your project doesn't have one by running the command when in the project directory |


<br><br>

Available Flags:
| Flags: | Description: |
| ---------------------------    |----------------------------------------------------------- |
| `--critical`  |  Only show critical severity vulnerabilities that have been found using GitHub Advisories. Can be used alongside [--high, --medium, --low] to also show vulnerabilities based on severity. |
| `-h, --help` |               If you need help with LAVI documentation, run the command to view all possible Flags.     |
| `--high`     |          Only show high-severity vulnerabilities that have been found using GitHub Advisories. Can be used alongside [--critical, --medium, --low] as other filters for vulnerabilities.|
| `--medium `   |         Only show medium severity vulnerabilities that have been found using GitHub Advisories. Can be used alongside [--critical, --high, --low] as other filters for vulnerabilities.|
| `--low`       |         Only show low severity vulnerabilities that have been found using GitHub Advisories. Can be used alongside [--critical, --high, --medium] as other filters for vulnerabilities.|
| `--no-scan`   |         Ignore scanning the tree for vulnerabilities and only create the dependency tree  |
| `--package string`   |   Run lavi on a single package. If provided along with the version, will default to running in a single package mode. This will also disable the UI if the flag is provided. |
| `-s, --show`     |          Show a UI representation of the vulnerabilities that have been found. Using this UI the user will be able to experiment with different combinations of package versions to try and eliminate the vulnerabilities that were found in the packages they are currently using. These changes to package versions can also be deployed immediately locally by running update packages.  |
| `--version string`   |  Run lavi on a single package. If provided along with the package, will default to running in a single package mode. This will also disable the UI if the flag is provided. |
| `-w, --write`        |       Write tree to a file that will be available for the user to use. |
| `--write-with-vulns`  |  When used with write, will also include vulnerabilities in the written tree file that will be available for the user.|
