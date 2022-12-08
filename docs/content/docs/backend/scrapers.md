---
id: scrapers
title: Scrapers
permalink: docs/backend/scrapers.html
---

The backend scrapers are what administrators use to fill in the database. Knowing how to trigger them is important to managing your LAVI instance.

## CVE Scraper

The CVE Scraper pulls from cves sources defined in the backend for a specific language. To trigger:

```bash
curl -X 'POST' 'http://vocation.cs.umd.edu/api/scrapers/trigger/get_cves?repo=REPO' -H 'Authorization: Bearer $API_TOKEN'
```

The `repo` query parameter denotes which repo to use. Should you add a new repo, you can call that repo by filling in the parameter.

For more documentation, see [here](/api/docs#/scrapers/trigger_get_cves_scrapers_trigger_get_cves_post)

## Packages Scraper

The Packages Scraper pulls from package repository sources defined in the backend for a specific language. To trigger:

```bash
curl -X 'POST' 'http://vocation.cs.umd.edu/api/scrapers/trigger/list_packages?repo=REPO&partial=true' -H 'Authorization: Bearer $API_TOKEN'
```

The `repo` query parameter denotes which repo to use. Should you add a new repo, you can call that repo by filling in the parameter.
For more documentation, see [here](/api/docs#/scrapers/trigger_list_packages_scrapers_trigger_list_packages_post)
