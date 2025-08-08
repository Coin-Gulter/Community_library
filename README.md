# Library Management Service

This project is an internal backend service for a community library to manage book lending, returns, and member notifications. It features a versioned REST API built with FastAPI, containerized with Docker, and uses Celery for handling asynchronous tasks like email notifications.

---

## Features

- **User Management**: Public registration for members and secure, script-based creation for staff.
- **Authentication**: Secure JWT-based authentication for all users.
- **Book Management**: Staff-only endpoints to register new books.
- **Lending System**: Borrow and return books, with automatic tracking of available copies.
- **API Versioning**: Supports multiple API versions (`v1`, `latest`) via the `X-API-Version` header.
- **Asynchronous Email Notifications**:
    - Real-time email notifications for borrowing and returning a book (supported only by the `latest` API version).
    - Automatic, daily email notifications for members with overdue books, handled by a scheduled task.

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Asynchronous Tasks**: Celery with a Redis broker and Celery Beat for scheduling
- **Code Quality**: `flake8` for linting and `pytest` for unit tests

---

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### 1. Clone the Repository

First, clone the project to your local machine.

```bash
git clone <your-repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables

Create your local environment file by copying the example.

```bash
cp .env.example .env
```

Next, **open the `.env` file and fill in your credentials.**

**Important Note on Email Testing:**
For the `SMTP_*` variables, it is recommended to use a dedicated email testing service like **Mailtrap.io** for test.

1.  Sign up for a free Mailtrap account.
2.  Go to your inbox and find your SMTP credentials.
3.  Copy and paste the `Host`, `Port`, `Username`, and `Password` into the corresponding `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, and `SMTP_PASSWORD` fields in your `.env` file.

### 3. Build and Run the Services

This single command will build the Docker images and start all services (API, database, worker, and beat scheduler) in the background.

```bash
docker-compose up --build -d
```

### 4. Initialize the Database

After the containers have started, you must run the database initialization script. This creates all the necessary tables (`users`, `books`, etc.).

```bash
docker-compose exec api python -m app.scripts.init_db
```

### 5. Create an Initial Staff User (Recommended)

To use the administrative features, you need at least one staff account. Run the following script to create one.

```bash
docker-compose exec api python -m app.scripts.create_staff --email staff@example.com --password admin123
```

Your application is now fully set up and ready to use.

---

## API Usage

### Interactive Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) at:
**`http://localhost:8000/docs`**

This interface allows you to explore and test all the API endpoints directly from your browser. Remember to use the **Authorize** button after getting a token from the `/auth/token` endpoint.

### API Versioning

The service supports versioning via the `X-API-Version` header.
- **`v1`**: The legacy version.
- **`latest`**: Includes all the newest features, like real-time email notifications.

If no header is provided, the API defaults to `v1`.

---

## Running Tests

To run the full suite of unit tests inside the Docker container, execute the following command:

```bash
docker-compose exec api pytest
```

## Code Linting

To check the code for style and quality issues with `flake8`, run:

```bash
docker-compose exec api flake8 .
