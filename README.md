# Telegram Bot + Flask Web Panel + MySQL

A production-ready system that collects Telegram user data via a bot, stores it in MySQL, and displays it through a Flask web dashboard. Fully containerized with Docker and auto-deployed to AWS EC2 via GitHub Actions CI/CD.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Telegram    │     │   Flask Web  │     │    MySQL     │
│  Bot         │────>│   Panel      │────>│   Database   │
│  (Python)    │     │  :5000       │     │   :3306      │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       └────────────────────┴────────────────────┘
                    Docker Compose
```

## Features

- **Telegram Bot** — saves user info on `/start`, reports user count with `/users_count`
- **Flask Web App** — HTML dashboard at `/` and JSON API at `/api/users`
- **MySQL 8.0** — persistent storage with auto-reconnect and connection pooling
- **Docker Compose** — three isolated containers on a shared network
- **CI/CD** — GitHub Actions auto-deploys to EC2 on every push to `main`

## Project Structure

```
├── bot/
│   ├── bot.py                 # Bot entry point and command handlers
│   ├── dockerfile
│   └── services/
│       └── user_service.py    # Database operations for the bot
├── web/
│   ├── app.py                 # Flask routes
│   ├── dockerfile
│   └── templates/
│       └── index.html         # Jinja2 dashboard template
├── shared/
│   ├── config.py              # Environment variable loader
│   ├── db.py                  # SQLAlchemy engine, session, init
│   └── models.py              # User model
├── docker-compose.yaml
├── requirements.txt
└── .github/
    └── workflows/
        └── main.yml           # CI/CD pipeline
```

## Tech Stack

| Layer        | Technology                          |
|--------------|-------------------------------------|
| Bot          | Python 3.11, pyTelegramBotAPI       |
| Web          | Flask 3.x, Jinja2                   |
| Database     | MySQL 8.0                           |
| ORM          | SQLAlchemy 2.0                      |
| Containers   | Docker, Docker Compose              |
| CI/CD        | GitHub Actions + SSH to EC2         |

## Database Schema

```sql
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username    VARCHAR(255),
    first_name  VARCHAR(255),
    last_name   VARCHAR(255),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Bot Commands

| Command        | Description                            |
|----------------|----------------------------------------|
| `/start`       | Saves or updates user info in database |
| `/users_count` | Returns total number of registered users |

## Web Routes

| Route         | Method | Description                     |
|---------------|--------|---------------------------------|
| `/`           | GET    | HTML table of all users         |
| `/api/users`  | GET    | JSON array of all users         |

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

### 1. Clone the repository

```bash
git clone https://github.com/AlbertZaqaryan/tb_web_sql_ci_cd.git
cd tb_web_sql_ci_cd
```

### 2. Create `.env` file

Edit `.env` with your values:

```env
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=your_db_name
BOT_TOKEN=bot_token
```

### 3. Run with Docker Compose

```bash
docker compose up --build -d
```

### 4. Verify

- Web panel: http://localhost:5000
- API endpoint: http://localhost:5000/api/users
- Send `/start` to your bot in Telegram

### Check container status

```bash
docker compose ps
docker compose logs -f
```

### Stop everything

```bash
docker compose down
```

## CI/CD Pipeline

The project auto-deploys to an AWS EC2 instance on every push to `main`.

### How it works

1. Push to `main` triggers the GitHub Actions workflow
2. Workflow SSHs into EC2
3. Installs Docker if not present (Ubuntu)
4. Pulls latest code from the repository
5. Creates `.env` from GitHub Secrets
6. Runs `docker compose down` then `docker compose up --build -d`
7. Waits for MySQL health check and verifies all containers are running

### Required GitHub Secrets

Go to **Settings > Secrets and variables > Actions** and add:

| Secret         | Description                      |
|----------------|----------------------------------|
| `EC2_HOST`     | EC2 public IP or hostname        |
| `EC2_USER`     | SSH username (e.g. `ubuntu`)     |
| `EC2_SSH_KEY`  | Private SSH key for EC2 access   |
| `DB_USER`      | MySQL username                   |
| `DB_PASSWORD`  | MySQL root password              |
| `DB_NAME`      | Database name                    |
| `BOT_TOKEN`    | Telegram bot token               |

## Environment Variables

| Variable      | Description              | Default     |
|---------------|--------------------------|-------------|
| `DB_HOST`     | MySQL hostname           | `localhost` |
| `DB_PORT`     | MySQL port               | `3306`      |
| `DB_USER`     | MySQL username           | `db_user`   |
| `DB_PASSWORD` | MySQL password           | —           |
| `DB_NAME`     | Database name            | `db_name`   |
| `BOT_TOKEN`   | Telegram bot token       | —           |

## License

This project is open source and available under the [MIT License](LICENSE).
