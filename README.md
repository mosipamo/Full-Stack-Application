# Full-Stack Todo Application

A full-stack web application built with **FastAPI**, serving dynamic HTML pages styled with **CSS and Bootstrap**. This application supports user authentication, role-based access (admin/user), and task management with persistent storage using **SQLite** and **Alembic** for migrations.

## Features

- 🔐 User authentication (Login, Signup, Session management)
- 👤 Admin and regular user roles
- ✅ CRUD operations on Todo items
- 📄 HTML templates rendered with Jinja2
- 🎨 CSS/Bootstrap for responsive UI
- 🗃️ SQLite database with Alembic migrations
- 🧪 Interactive API docs using Swagger (FastAPI's `/docs`)

## Project Structure

```
Full-Stack-Application-main/
│
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── TodoApp/
│   ├── main.py                   # FastAPI app entrypoint
│   ├── database.py               # DB connection
│   ├── models.py                 # ORM models
│   ├── alembic.ini               # Alembic config
│   ├── todosapp.db               # SQLite DB / I use PostgreSQL in this project
│   ├── routers/                  # Route definitions
│   │   ├── auth.py               # Auth routes
│   │   ├── admin.py              # Admin functionality
│   │   ├── users.py              # User endpoints
│   │   └── todos.py              # Todo logic
│   ├── static/css/               # Stylesheets
│   ├── templates/                # HTML templates
│   ├── alembic/                  # Alembic migration scripts
│   │   └── versions/
```

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/mosipamo/Full-Stack-Application.git
cd Full-Stack-Application/TodoApp
```

2. **Create a virtual environment and activate it:**

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate.bat`
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run database migrations (Alembic):**

```bash
alembic upgrade head
```

5. **Run the FastAPI server:**

```bash
cd ..
uvicorn TodoApp.main:app --reload
```

6. **Visit the app:**

- Web UI: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Swagger UI

FastAPI provides a built-in, interactive **Swagger UI** at `/docs`, where you can:

- Test all API routes (auth, user management, todos)
- Inspect request/response schemas
- View and debug endpoints easily during development

## Technologies Used

- **FastAPI**
- **Jinja2 Templates**
- **SQLite/PostgreSQL + SQLAlchemy**
- **Alembic** (DB migrations)
- **HTML, CSS, Bootstrap**
- **Uvicorn** (ASGI server)
