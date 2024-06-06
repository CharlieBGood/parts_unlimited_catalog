# Parts Unlimited Catalog

API allowing for CRUD operations on parts.

## Run Locally

Go to the project directory

```bash
  cd parts_unlimited_catalog
```

Create virtualenv

```bash
  python -m venv </path/to/new/virtual/environment>
```

Activate virtualenv

```bash
  source </path/to/new/virtual/environment>/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Create db and add records

```bash
  python manage.py start_db
```

Run migrations

```bash
  python manage.py migrate
```

Run server

```bash
  python manage.py runserver
```

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```
