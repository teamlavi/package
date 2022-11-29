# Installation

```bash
sudo apt-get update -y
sudo apt-get install -y git
sudo git config --global credential.helper store
sudo git config --global pull.rebase false
sudo git clone https://para.cs.umd.edu/levi/package.git
```

When prompted, give any username. For the password, give a project access token [generated here](https://para.cs.umd.edu/levi/package/-/settings/access_tokens) with `Reporter` role and `read_repository` scope.

Before running the setup script, you have to get a Github Access token, [generated here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token), to enable github advisories scraping. Then, run `export GH_ACCESS_TOKEN="<your token>"` to save it.

NOTE: The token will be stored in plaintext in the root user's crontab file.

TODO: any specific scopes necessary on the gh tok?

```bash
cd package
sudo git pull
bash scripts/vm/setup.sh
```

The setup script will then install dependencies, then update your cron as necessary to keep this VM live with prod every minute or so.
