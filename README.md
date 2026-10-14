# InteriorFlow

InteriorFlow is a Django web application for managing interior-design projects. It helps track project details, tasks, weighted progress, site updates, workers, and expenses.

## Features

- Create, view, and edit projects with client, location, dates, budget, and status.
- Create and edit project tasks with weights, due dates, and completion percentages.
- Calculate overall project progress using a weighted average of task completion.
- Record dated site updates with a snapshot of the current project progress.
- Manage workers and project assignments.
- Record project expenses.
- Validate form input using Django forms and model validators.
- Automated tests for weighted progress calculation.

## Technology

- Python and Django
- MySQL
- Django Templates, HTML, and Tailwind CSS
- Git and GitHub

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/farhan-d3v/InteriorFlow.git
cd InteriorFlow
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create a MySQL database and user

Log into MySQL with an administrator account and create a database and dedicated user. Replace the example password with a strong password of your own choosing.

```sql
CREATE DATABASE interiorflow_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'interiorflow_user'@'localhost' IDENTIFIED BY 'replace_with_a_strong_password';
GRANT ALL PRIVILEGES ON interiorflow_db.* TO 'interiorflow_user'@'localhost';
FLUSH PRIVILEGES;
```

If you already have this database and user, keep using your existing credentials rather than recreating them.

### 5. Configure environment variables

Create a `.env` file in the project root (the same directory as `manage.py`). Use your own secret key and database password. Do not commit this file.

```dotenv
DJANGO_SECRET_KEY=replace_with_a_new_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=
DB_NAME=interiorflow_db
DB_USER=interiorflow_user
DB_PASSWORD=replace_with_your_database_password
DB_HOST=localhost
DB_PORT=3306
```

The Django settings must read `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`, and `DJANGO_CSRF_TRUSTED_ORIGINS` from environment variables. The `.env` file should remain local and must not be pushed to GitHub.

### 6. Apply migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

Open <http://127.0.0.1:8000/>.

## Automated tests

```bash
python manage.py test projects
```

The current tests check that a project with no tasks calculates to 0% progress, that weighted task progress is calculated correctly, and that calculated progress is saved to the project. MySQL test runs require the database user to have permission to create a temporary test database.

## Project progress rules

Each task has a weight and a completion percentage. Overall project progress is calculated as:

```text
round(sum(task weight * task progress) / sum(task weights))
```

Weights do not need to add up to 100 because the calculation divides by the sum of all task weights. A project with no tasks calculates to 0%. For example, a task weighted 60 at 100% and another weighted 40 at 25% produce 70% overall progress.

Site updates are historical records. Each update saves a snapshot of the project's current progress; adding a site update does not itself change the current progress. A project should only be marked Completed when its task-based calculated progress reaches 100%.

## Deployment notes

For a hosted demo, deploy the Django application to a Python-compatible web host and use a separate hosted MySQL database. Configure the following environment variables in the host's dashboard, never in source control:

- `DJANGO_SECRET_KEY`: a newly generated secret key
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS`: the deployed hostname, without `https://`
- `DJANGO_CSRF_TRUSTED_ORIGINS`: the full HTTPS origin, such as `https://your-app.example.com`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`: hosted MySQL connection details

Use the host's documented TLS/SSL settings for the hosted MySQL service. Configure static files with WhiteNoise and run `python manage.py collectstatic --no-input` during deployment. Apply migrations to the hosted database before using the live site. Do not use the Django development server for production.

## Security

- Never commit `.env`, database passwords, or secret keys.
- Use a new production secret key; do not reuse a key exposed in development code or chat.
- Keep `DEBUG=False` in production and configure the exact allowed host and CSRF trusted origin.
- Use a dedicated database account with only the permissions needed by the app.

## Current test coverage and limitations

Automated coverage currently focuses on task-based progress calculation. Before production use, also test project creation and editing, date validation, task workflows, site updates, worker assignments, expenses, dashboard filters, and responsive layouts. Deployment instructions may need small adjustments depending on the selected hosting provider.

## Author

Mohammed Farhan M I — [GitHub: farhan-d3v](https://github.com/farhan-d3v)
