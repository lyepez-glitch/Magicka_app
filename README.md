# 🧙‍♂️ Magicka Backend

This is the backend server for the **Magicka** application — a real-time magical dueling platform powered by Django, Django Channels, and WebSockets.

> Handles authentication, user profiles, attack events, real-time chat, and WebSocket-powered battles.

---

## 🚀 Features

- 🔐 JWT Authentication with Django Rest Framework + Simple JWT
- 🧑‍💻 User signup, login, and profile editing
- ⚔️ Real-time attacks and health updates over WebSockets using Django Channels + Redis
- 💬 Chat rooms between users
- 🗃️ SQLite for development database (PostgreSQL-ready)
- 🌐 CORS setup for frontend integration
- 🧪 Travis CI/CD ready

---

## ⚙️ Tech Stack

- **Django 5.1.1**
- **Django Channels**
- **Redis (for WebSocket channel layer)**
- **Django REST Framework (DRF)**
- **Simple JWT**
- **SQLite** (default) or **PostgreSQL**
- **CORS Headers**

---

## 🔧 Local Setup

### Prerequisites

- Python 3.11+
- Redis server (locally or hosted)
- Optional: PostgreSQL if switching from SQLite

### Clone the Repository

```bash
git clone https://github.com/your-username/magicka-backend.git
cd magicka-backend
Create Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

pip install -r requirements.txt
Environment Variables
Set up a .env file (or set manually):


FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
🛠 Running the Project
Migrations & Dev Server

python manage.py migrate
python manage.py runserver
Run ASGI Server (if applicable)
If using Channels in production:


daphne magicka_app.asgi:application
🔌 WebSockets
Configured with Channels + Redis

Uses channels_redis.core.RedisChannelLayer

Example WebSocket flow: attack commands and health updates sent in real time between users

🔐 Auth System
JWT-based auth (rest_framework_simplejwt)

Add Authorization: Bearer <token> to protected routes

Includes standard user registration & login

🗃️ Database
Default: SQLite (db.sqlite3)

PostgreSQL ready: Uncomment in settings.py to switch

🌍 CORS Support
Allows frontend running on:

http://localhost:5173

https://magicka-frontend-auth-git-feature1-lucas-projects-f61d5cb5.vercel.app/

Uses django-cors-headers

📂 Project Structure

magicka_app/
├── magicka/           # Core app (models, views, consumers)
├── magicka_app/       # Project config (settings, urls, ASGI)
├── manage.py
└── requirements.txt
📦 Deployment
CI/CD enabled via Travis CI

Redis required for WebSocket support

Use Render, Heroku, or Railway for quick Django + Channels hosting

📝 License
Open-source, free to use for educational or demo purposes.






