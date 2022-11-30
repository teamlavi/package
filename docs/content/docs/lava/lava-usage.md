LAVA is a tool that developers and researchers can use to query our CVE databases in order to find trends and 
statistics about vulnerabilities inside repos such as npm.

Each command may have different options. Be sure to use "lava [command] --help to see what options are available before running.

Usage:

    lava [command] --Flags

Available Commands:
 | Commands | Description |
 | - | - | 
 | affectedCount | For vulnerabilities found in queried packages return a list with the number of packages affected by each vulnerability. | 
| cancel | A brief description of your command. | 
| completion | Generate teh autocompletion script for the specified shell. |
| count  |     Returns the number of packages inside the specified repository. |
| countDependencies  | Returns list of how many other packages each package relies on. |
| countVul   |  Returns the number of vulnerable packages inside the specified repository. |
| depth   |   Returns a list of how deep each vulnerability was from the top level package (How many dependencies deep each vulnerability is). |
| help | Help about any command for LAVA  |
| numDownloads | Returns a list with number of downloads for each package included. |
| severities | Returns a list of vulnerable packages and severitites for each vulnerability. |
| types | Returns CWEs and a count of how many vulnerabilities are linked with each CWE. |
| vulnerablePackages | Returns a list of vulnerable packages inside the chosen repository. |

<br><br><br><br>


| Flags: | Description: |
| -    |    - |
| `--csv string`  |   Save the results of LAVA query to a csv file. |
| `-h, --help` |               help for lava.     |
| `--level string`     |    Vulnerability depth levels to look at (direct, indirect, or all). |
| `--packages strings`   |  A list of packages that will be queried with specified command. |
| `-r, --repo string`       |   Repository to run the analysis on (Options: pip, nmp or go)|
| `--status string`   |     Vulnerability status to look at (options: active, patched, or all). Active vulnerabilities are vulnerabilities that have not been patched and still exist. Patched vulnerabilities are vulnerabilities that have been patched and are no longer active.  |

