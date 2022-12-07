---
id: future-work
title: Future Work
permalink: docs/extension/future.html
---

LAVI has the potential to live on for a long time, in both client use and research use. Some possible future work ideas are listed below

1. Adding more languages
2. Non reliance on individual package managers for dependency tree generation
    * As in, not using npm to generate a cds for an npm project. Could LAVI do it on its own?
    * Could greatly save on computation time for building out the database
3. Adding new CVE sources
4. Utilizing the CDS as a language agnostic lock file
    * In theory, if the CDS enumerates the full dependency tree, what is stopping it being used as a single command for multiple language package installation
    * Instead of `pip install` a bunching a packages, why not `lavi install` and that uses a pregenerated CDS
    * Same for `npm install` or any other language
5. Adding more LAVA queries