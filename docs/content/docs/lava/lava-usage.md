---
id: lava-usage
title: LAVA Usage
permalink: docs/lava/usage.html
---

LAVA is a tool that developers and researchers can use to query the backend databases in order to find trends and statistics about dependencies and vulnerabilities in package repositories.

Each command may have different options. Be sure to use `lava [command] --help` to see what options are available before running.

## Usage Notes

### API Key
To get an api key, speak to your LAVI system administrator. If they don't know the api key, please direct them to [this](/docs/backend/architecture.html#lavi-worker) documentation.

### In progress view

Some queries can take a long time to process. The CLI provides a helpful status output during query execution that lets you know the execution is still in progress. There is a spinner that updates every 200ms to denote inprogress and a time that updates every 5 seconds during execution which indicates the last time the API was polled for results.
```bash
Polling job ceabdbcd-a208-4901-99ac-26a52b3a7955
/ status: pending as of Wed, 07 Dec 2022 19:21:02 EST
```
200 ms later
``` bash
Polling job ceabdbcd-a208-4901-99ac-26a52b3a7955
- status: pending as of Wed, 07 Dec 2022 19:21:02 EST
```
200 ms later
``` bash
Polling job ceabdbcd-a208-4901-99ac-26a52b3a7955
\ status: pending as of Wed, 07 Dec 2022 19:21:02 EST
```

After next poll
```bash
Polling job ceabdbcd-a208-4901-99ac-26a52b3a7955
/ status: pending as of Wed, 07 Dec 2022 19:21:07 EST
```

### Failover Protection

Occasionally, things may fail. Unfortunately, some queries may take so long that a failure on the part of the CLI preventing users from getting the data is unacceptable. Should the query sent fail, the CLI will attempt to write any response back from the api to a text file for user inspection. A message detailing this operation is shown to the user whenever an error occurs, so that they still have the results, and can inspect the results themselves for debugging and/or further analysis purposes. Occasionally, these results written to a file may show package IDs, which are not human readable, however there is documentation detailing the spec for package IDs and how to decode them [here](/docs/getting-started/data.html#package-ids)

## Persistent Flags

These flags can be applied across all commands
```bash
      --api-key string     Lava backend api key
      --csv string         Save to csv file (default "lava-response.csv")
  -h, --help               help for lava
      --packages strings   Packages to look at
      --remote string      Remote api url. Must start with http:// or https://, and not end with a slash (default "http://vocation.cs.umd.edu/api")
  -r, --repo string        Repo to run analysis on
```

The flags `--repo` and `--api-key` are used in every command. **To get an api key, speak to your LAVI system administrator.**

## Commands

Each command has a specific way of showing results. They will also all write to a csv file, specifically the one provided by the `--csv` flag. Should that flag not be provided, the CLI will write to `lavi-response-####.csv`, where #### is a random 4 digit number. This helps prevent overwriting results.

Quicklinks
* [affectedCount](#affectedcount)
* [allPackages](#allpackages)
* [count](#count)
* [countDependencies](#countdependencies)
* [countVul](#countvul)
* [dependencyStats](#dependencystats)
* [depth](#depth)
* [numDownloads](#numdownloads)
* [packageDependencies](#packagedependencies)
* [severities](#severities)
* [treeBreadth](#treebreadth)
* [treeDepth](#treedepth)
* [types](#types)
* [vulnerabilityPaths](#vulnerabilitypaths)
* [vulnerablePackages](#vulnerablepackages)

### affectedCount

`affectedCount` returns the number of packages affected by any vulnerability found in the packages provided by the `--packages` flag.
```bash
lava -r [REPO] affectedCount --packages="package1==version1,package2==version2,..."
```

### allPackages

`allPackages` returns all packages in the repository for which lava has a dependency tree.
```bash
lava -r [REPO] allPackages
```

### count

`count` returns the number of packages in the repository for which lava has a dependency tree.
```bash
lava -r [REPO] count
```

### countDependencies

`countDependencies` counts the number of dependencies for each package provided by the `--packages` flag.
```bash
lava -r [REPO] countDependencies --packages="package1==version1,package2==version2,..."
```

### countVul

`countVul` returns the number of vulnerable packages in the database.
```bash
lava -r [REPO] countVul
```

### dependencyStats

`dependencyStats` returns global dependency stats for the given repository. Currently returns mean, median, mode, and standard deviation of the number of dependencies a package has in a single repository.
```bash
lava -r [REPO] dependencyStats
```

### depth

`depth` returns list of how deep each vulnerability was from the top level package (how many dependencies deep) for each package given in the `--packages` flag.
```bash
lava -r [REPO] depth --packages="package1==version1,package2==version2,..."
```

### numDownloads

`numDownloads` returns the number of downloads for the packages specified by the `--packages` flag. Currently only works for pip.
```bash
lava -r [REPO] numDownloads --packages="package1==version1,package2==version2,..."
```

### packageDependencies

`packageDependencies` returns the dependency tree for packages provided by the `--packages` flag.
```bash
lava -r [REPO] packageDependencies --packages="package1==version1,package2==version2,..."
```

### severities

`severities` returns a list of packages and the severity for each vulnerability found in the packages provided by the `--packages` flag.
```bash
lava -r [REPO] severities --packages="package1==version1,package2==version2,..."
```

### treeBreadth

`treeBreadth` returns the breadth of the dependency tree found for packages provided by the `--packages` flag.
```bash
lava -r [REPO] treeBreadth --packages="package1==version1,package2==version2,..."
```

### treeDepth

`treeDepth` returns the breadth of the dependency tree found for packages provided by the `--packages` flag.
```bash
lava -r [REPO] treeDepth --packages="package1==version1,package2==version2,..."
```

### types

`types` returns CWEs and a count of how many vulnerabilities for each CWE found in the packages provided by the `--packages` flag.
```bash
lava -r [REPO] types --packages="package1==version1,package2==version2,..."
```

### vulnerabilityPaths

`vulnerabilityPaths` returns the path from the root package to vulnerable sub dependency for the packages provided by the `--packages` flag.
```bash
lava -r [REPO] vulnerabilityPaths --packages="package1==version1,package2==version2,..."
```

### vulnerablePackages

`vulnerablePackages` returns a list of all vulnerable packages found in the database for a given package repository.
```bash
lava -r [REPO] vulnerablePackages
```
