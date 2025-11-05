## Running this one service

You can run this in one of two ways:

- In directory services/auth/src

```bash
flask run
```

- In directory services/auth

```bash
python3 -m src.app
```

## Flask-Migrate commands

Create a new migration based on unmigrated changes in models:

```bash
flask db migrate -m "changes description"
```

Commit migration to database

```bash
flask db upgrade
```
