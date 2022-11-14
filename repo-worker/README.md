# Package Repository Worker

A single codebase to serve multiple functions:
* Given a repository, scrape its package list
* Given a repository and a package, enumerate its available versions
* Given a repository, package, and version, generate a conflict-free dependency tree (post-CDR)

Each of these is called via different subcommands.
