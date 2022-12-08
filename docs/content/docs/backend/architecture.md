---
id: backend-architecture
title: Architecture
permalink: docs/backend/architecture.html
---

The LAVI backend is a complex system that all comes together to create an integrated system for identifying and analyzing vulnerabilities

The LAVI backend runs in Docker Compose, which allows the system to be brought to almost any system, as long as it can run Docker. Ideally, in the future this would shift to Kubernetes for better failover protection and automatic scaling.

## Components

### lavi-worker

LAVI worker is the centerpiece to the backend. The worker is built to handle all requests into the backend from the CLIs, and execute different business logic based on the query. It interfaces with the databases to find the right data, and returns it back to the user.
It also interfaces with the Redis queues to start analysis jobs for LAVA. Please note that in the `docker-compose.yml` file is where you specify the api key for LAVA queries.

### Redis and Redis queues

[Redis](https://redis.io/) is an open source in-memory database that LAVI uses to store jobs that are waiting to be sent to downstream workers, like the analysis worker. Each set of workers are assigned a queue in Redis, and they will pull jobs and execute them

### worker-analysis

This worker pulls jobs from the `analysis` queue and executes them. This is used to service LAVA queries. 

### worker-generate-tree

This worker pulls jobs from the `to_generate_tree` queue and executes them. This is used to fill the database with full dependency trees that are used for determining results to LAVA queries.

### worker-get-cves

This worker pulls jobs from the `to_get_cves` queue and executes them. This is used to fill the database with cve data to be used in LAVI and LAVA operations.

### worker-list-packages

This worker pulls jobs from the `to_list_packages` queue and executes them. This is executes package scrapers for different package repositories to add to the database to be used in both LAVI and LAVA.

### worker-list-versions

This worker pulls jobs from the `to_list_versions` queue and executes them. This is executes package scrapers for different package repositories, specifically looking for versions of packages LAVI already knows of to add to the database to be used in both LAVI and LAVA.

### docs

This is the docs site you are looking at right now! The site is built using [gatsby](https://www.gatsbyjs.com/) with some plugins to convert markdown files to the page you are reading right now.

### nginx

[nginx](https://www.nginx.com/) is the web server used by LAVI to wrap everything together, exposing both the lavi-worker and the docs site on port 80 for the open internet to see.

### rqmonitor

rqmonitor is a tool for users to see the status of the redis queues and debug any issues they may come across.