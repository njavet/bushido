# bushido (武士道)
Bushido is a discipline-driven personal logging and analytics app. It helps you capture structured data about training, recovery, and daily activities.

## Setup postgresql on Arch Linux
install postgresql
 
`sudo pacman -S postgresql`

initialize the cluster
```
sudo -iu postgres 
initdb --locale=C.UTF-8 --encoding=UTF8 -D /var/lib/postgresql/data
exit
 ```

start and check
```aiignore
sudo systemctl enable --now postgresql
systemctl status postgresql
ss -lntp | grep 5432
```

create a database/user

`sudo -iu postgres psql`

```aiignore
CREATE USER bushido WITH PASSWORD 'bushido-dev';
CREATE DATABASE bushido OWNER bushido;
\q
```

test

`psql -h localhost -U bushido -d bushido`

### alembic
```aiignore
uv run alembic revision --autogenerate -m "initial migration"
uv run alembic history
uv run alembic heads
uv run alembic upgrade head
```

## elm frontend
```aiignore
cd frontend
elm make src/Main.elm --output=elm.js
```
deploy
```
az storage blob upload \
  --account-name "$WEB" \
  --container-name '$web' \
  --name index.html \
  --file index.html \
  --auth-mode login \
  --overwrite

az storage blob upload \
  --account-name "$WEB" \
  --container-name '$web' \
  --name elm.js \
  --file elm.js \
  --auth-mode login \
  --overwrite
  
az storage blob upload \
  --account-name "$WEB" \
  --container-name '$web' \
  --name styles.css \
  --file styles.css \
  --auth-mode login \
  --overwrite
```
* purge frontdoor cache
```aiignore
az afd endpoint purge \
  -g "$RG" \
  --profile-name "$AFD_PROFILE" \
  --endpoint-name "$AFD_ENDPOINT" \
  --content-paths "/*"
```


## terraform
-> wip

### Installation for usage
* download tarball 
* install pipx
```aiignore
pipx install bushido-major.minor.patch.tar.gz
```

### Installation for dev 

#### Prerequisites
* Python 3.14+
```
curl -Ls https://astral.sh/uv/install.sh | sh
git clone https://github.com/njavet/bushido.git
cd bushido
uv sync
uv run bushido
```
