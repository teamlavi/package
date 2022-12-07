---
id: backend-install
title: Install the backend
permalink: docs/backend/install.html
---

# Installation

```bash
sudo apt-get update -y
sudo apt-get install -y git
sudo git config --global credential.helper store
sudo git config --global pull.rebase false
sudo git clone https://para.cs.umd.edu/levi/package.git
```

When prompted, give any username. For the password, give a project access token [generated here](https://para.cs.umd.edu/levi/package/-/settings/access_tokens) with `Reporter` role and `read_repository` scope.

Before running the setup script, you have to get a Github Access token, [generated here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), to enable github advisories scraping. More information about using a GitHub access token with GraphQL can be found [here](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql). Then, run `export GH_ACCESS_TOKEN="<your token>"` to save it.

To use the GitHub advisories scraper request the following scopes :
```
repo
read:packages
read:org
read:public_key
read:repo_hook
user
read:discussion
read:enterprise
read:gpg_key
```

NOTE: The token will be stored in plaintext in the root user's crontab file.


```bash
cd package
sudo git pull
bash scripts/vm/setup.sh
```

When prompted with the `postfix` post-install configuration, just set it to local-only mail. This allows us to see logs from the cron job if it should fail.

The setup script will then install dependencies, then update your cron as necessary to keep this VM live with prod every minute or so.
