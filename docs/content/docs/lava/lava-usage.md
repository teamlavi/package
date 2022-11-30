---
id: lava-usage
title: LAVA Usage
permalink: docs/lava/usage.html
---

LAVA is a tool that developers and researchers can use to query our CVE databases in order to find trends and 
statistics about vulnerabilities inside repos such as npm.

Each command may have different options. Be sure to use "lava [command] --help to see what options are available before running.

NOTE: the --repo flag is REQUIRED for every LAVA command

Usage:

    lava [command] --Flags

Available Commands:
 | Commands | Description |
 | - | - | 
 | affectedCount | For vulnerabilities found in queried packages return a list with the number of packages affected by each vulnerability. | 
| completion | Generate the auto-completion script for the specified shell. |
| count  |     Returns the number of packages inside the specified repository. Ex: lava count --repo "pip" returns the total number of packages stored in the pip repository|
| countDependencies  | Returns list of how many other packages each package relies on. This command requires the user to pass in a list of packages using the --packages flag documented in the Flags table below.|
| countVul   |  Returns the number of vulnerable packages inside the specified repository. Ex: lava countVul --repo "npm" returns the total number of packages that are vulnerable inside of the npm repository.|
| depth   |   Returns a list of how deep each vulnerability was from the top level package (How many dependencies deep each vulnerability is). Ex: a depth vulnerability with a depth of 0, would indicate that the vulnerability is in the base package level, meaning that it is located in one of the dependencies passed in by te user. This command requires the user to pass in a list of packages using the --packages flag documented in the Flags table below. |
| help | Help about any command for LAVA.  |
| numDownloads | Returns a list with number of downloads for each package included. This command requires the user to pass in a list of packages using the --packages flag documented in the Flags table below.|
| severities | Returns a list of vulnerable packages and severitites for each vulnerability. The severity types are: None, Low, Medium, High, and Critical. This command requires the user to pass in a list of packages using the --packages flag documented in the Flags table below.|
| types | Returns CWEs and a count of how many vulnerabilities are linked with each CWE. This command requires the user to pass in a list of packages using the --packages flag documented in the Flags table below.|
| vulnerablePackages | Returns a list of vulnerable packages inside the chosen repository. Ex: lava vulnerablePackages --repo "pip" returns a list of all the vulnerable packages in the pip repository.|

<br><br><br><br>


| Flags: | Description: |
| -    |    - |
| `--csv string`  |   Save the results of LAVA query to a csv file. |
| `-h, --help` |               help for lava.     |
| `--level string`     |    Vulnerability depth levels to look at (direct, indirect, or all). |
| `--packages strings`   |  A list of packages that will be queried with specified command. |
| `-r, --repo string`       |   Repository to run the analysis on (Options: pip, npm or go)|
| `--status string`   |     Vulnerability status that will be filtered upon. (Options: active, patched, or all). Active vulnerabilities are vulnerabilities that have not been patched and still exist. Patched vulnerabilities are vulnerabilities that have been patched and are no longer active.  |

