### [_Index_](../README.md)
### _Next_

We have a basic flask app setup that has the following features -

- Authentication
- Celery with Redis
- Postgres storage
- A worker server for celery tasks
- A Hashicorp vault server in a separate network

Before proceeding , have a look at how to get the infra up and running:

```sh
cd services\baseimage_secretstore
docker build -t baseimage_secretstore .
```

----------------------------------------------------
**Buiding the vault server**
```sh
cd /services/vault
docker compose build
docker compose up -d
```
Vault will be initialised in the first bootup.

Now go to /vault/logs/startup/init_out.log
Copy the value of the unseal keys and root token to vault.env in config folder.

```sh
docker compose stop
docker compose start
```

This will unseal the vault. Vault will start everytime unsealed until you rebuild the container.

---------------------------------------------------

**Building the project**

**Important**: Make sure all the .sh scripts are using LF encoding instead of CRLF else you will get an error in app and worker sevices that init scripts are not found.

Before proceeding make sure the variables in .env files mentioned in docker compose are set to your acceptance.

At the project root level where .env file is located,run the following:

```sh
docker compose build
docker compose up -d
```

To restart the containers:
```sh
docker compose stop
docker compose start
```

Now go to the browser at 127.0.0.1/5000/ and your basic app should be up.