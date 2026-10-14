# InteriorFlow — Interior Design Project Management

InteriorFlow is a full-stack web application designed to help an interior design company manage projects from creation through completion. It provides a central place to track project details, timelines, budgets, site updates, team assignments, and expenses.

## Features

- **Dashboard:** Summary cards for total, ongoing, completed, and overdue projects.
- **Project management:** Create, view, and edit projects with client details, location, description, dates, estimated budget, status, and progress.
- **Search and filtering:** Find projects and filter or sort the project list.
- **Project details:** View project information, timeline, progress, budget, site updates, and assigned workers.
- **Site updates:** Record dated updates with notes, author, and progress percentage.
- **Worker management:** Add team members, assign them to projects, and remove assignments.
- **Expense tracking:** Record project expenses and view actual spending and remaining budget.
- **Validation:** Validate project details, dates, budget, and progress.
- **Responsive interface:** Django templates styled with Tailwind CSS.

## Technology Stack

- **Backend:** Python and Django
- **Database:** MySQL
- **Frontend:** Django Templates, HTML, and Tailwind CSS
- **Configuration:** Environment variables loaded from `.env`

## Prerequisites

Install the following before running the application:

- Python 3.13 or a compatible Python version
- MySQL Server
- Git
- pip

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd InteriorFlow
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Create the MySQL database

Log in to MySQL and create a database:

```sql
CREATE DATABASE interiorflow_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Configure a MySQL user with the necessary permissions to access this database. Use your own secure password.

### 5. Configure environment variables

Create a `.env` file in the project root, in the same directory as `manage.py`.

Add the following values and replace the password with your own:

```dotenv
DB_NAME=interiorflow_db
DB_USER=interiorflow_user
DB_PASSWORD=your_local_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

Never commit `.env` or real database credentials to version control. The repository includes `.env.example` as a template.

### 6. Apply database migrations

```powershell
python manage.py migrate
```

### 7. Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Demo Data

The application can be populated through its project and team management forms.

For a useful demonstration:

1. Create projects with different statuses, budgets, and deadlines.
2. Open a project and add site updates.
3. Add workers and assign them to projects.
4. Record expenses and check the remaining budget.
5. Return to the dashboard to review project summaries.

All sample names, clients, and amounts should be fictional.

## Django Admin (Optional)

To create an administrator account:

```powershell
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.

The admin panel is optional; the primary project workflows are available through the InteriorFlow interface.

## Project Statuses

- **Planning:** Work has not yet started.
- **Ongoing:** Work is in progress.
- **On Hold:** Work is temporarily paused.
- **Completed:** Work has been completed; progress should be 100%.

## Assumptions and Limitations

- The application is intended as an assessment project and local demonstration.
- Authentication is optional; a Django administrator account can be created for the admin panel.
- Demo data is fictional and should not be treated as real client information.
- The application should be tested and configured appropriately before production deployment.
- Tailwind CSS is loaded through its CDN in the development interface, so an internet connection may be required for styling.

## AI Assistance

AI tools were used to support development, explain implementation decisions, and help troubleshoot issues. The implementation should be reviewed and understood by the developer before submission.
