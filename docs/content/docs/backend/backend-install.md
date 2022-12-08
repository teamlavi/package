---
id: backend-install
title: Install the backend
permalink: docs/backend/install.html
---

Installing the backend currently only works on Linux based machines

## Install 

```bash
sudo apt-get update -y
sudo apt-get install -y git
sudo git config --global credential.helper store
sudo git config --global pull.rebase false
sudo git clone https://para.cs.umd.edu/levi/package.git
```

When prompted, give any username. For the password, give a project access token [generated here](https://para.cs.umd.edu/levi/package/-/settings/access_tokens) with `Reporter` role and `read_repository` scope.

Before running the setup script, you have to get a Github Access token, [generated here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), to enable github advisories scraping. Then, run `export GH_ACCESS_TOKEN="<your token>"` to save it.

> The Github Access Token will be stored in plaintext in the root user's crontab file.

This script will install all dependencies (golang, npm, docker, etc) and setup the cronjob for updating based on changes to main.

```bash
cd package
sudo git pull
bash scripts/vm/setup.sh
```

When prompted with the `postfix` post-install configuration, just set it to local-only mail. This allows us to see logs from the cron job if it should fail.

The setup script will then install dependencies, then update your cron to update from main every 5 minutes. This can be disabled in favor of manual updates by running

```bash
sudo crontab -e
```
And then comenting out the line for the `sync.sh` script


## Troubleshooting

Sometimes, you may run into some undefined issues. In order to get more information, there are a couple of steps you can try

* Manually trigger sync script
```bash
sudo crontab -l
```
Copy the command shown there (except the stars) and run it using sudo to manually trigger the sync script, which can reveal some errors

* See cronjob output
```bash
sudo tail /var/mail/root
```