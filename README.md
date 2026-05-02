# Team Task Manager

A full-stack web app where users can create projects, assign tasks, and track progress with role-based access (Admin / Member).

## Features

- 🔐 Authentication (Signup / Login) with JWT
- 👥 Role-based access control (Admin & Member)
- 📁 Project management (Admins create, all see)
- ✅ Task creation, assignment, status tracking (To Do / In Progress / Done)
- 📊 Dashboard with task counts and overdue alerts
- 🗂️ Filter tasks by status and project

## Tech Stack

- **Backend:** FastAPI (Python), SQLAlchemy, JWT auth
- **Database:** SQLite (local) / PostgreSQL (production)
- **Frontend:** HTML + Tailwind CSS + Vanilla JS (single-page)
- **Deployment:** Railway

## Folder Structure

```
team-task-manager/
├── backend/
│   ├── main.py             # FastAPI app entry
│   ├── database.py         # DB config
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # JWT + password hashing
│   ├── routes/
│   │   ├── users.py        # signup/login
│   │   ├── projects.py     # project CRUD
│   │   └── tasks.py        # task CRUD + dashboard
│   ├── requirements.txt
│   ├── Procfile
│   └── .env
└── frontend/
    └── index.html          # Single-page UI
```

## Local Setup

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `http://localhost:8000` — frontend loads from there.

API docs available at `http://localhost:8000/docs`.

## Deployment on Railway

1. Push this repo to GitHub.
2. Go to [Railway](https://railway.app) → New Project → Deploy from GitHub.
3. Select the repo. Set the **Root Directory** to `backend`.
4. Add a **PostgreSQL** plugin (Railway auto-creates `DATABASE_URL`).
5. Add environment variables:
   - `SECRET_KEY` = (some long random string)
   - `ALGORITHM` = `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES` = `120`
6. Deploy. Railway uses the `Procfile` automatically.
7. Once deployed, click "Generate Domain" to get the live URL.

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/users/signup` | No | Create account |
| POST | `/api/users/login` | No | Login, returns JWT |
| GET | `/api/users/me` | Yes | Current user info |
| GET | `/api/users/` | Yes | List users |
| POST | `/api/projects/` | Admin | Create project |
| GET | `/api/projects/` | Yes | List projects |
| DELETE | `/api/projects/{id}` | Admin | Delete project |
| POST | `/api/tasks/` | Admin | Create task |
| GET | `/api/tasks/` | Yes | List tasks (filtered) |
| GET | `/api/tasks/dashboard` | Yes | Task stats |
| PUT | `/api/tasks/{id}` | Yes | Update task (members: own status only) |
| DELETE | `/api/tasks/{id}` | Admin | Delete task |

## Role Permissions

| Action | Admin | Member |
|---|---|---|
| Signup / Login | ✅ | ✅ |
| View projects & tasks | All | Own assigned tasks only |
| Create / delete projects | ✅ | ❌ |
| Create / delete / reassign tasks | ✅ | ❌ |
| Update own task status | ✅ | ✅ |

## Default Test Users

After deploying, sign up with role `admin` to test full functionality, then create a `member` account to test restricted access.
