# Library Management Service

This project is an internal backend service for a community library to manage book lending, returns, and member notifications. It features a versioned REST API built with FastAPI, containerized with Docker, and uses Celery for handling asynchronous tasks like email notifications.

---

## Features

* **Authentication**: Secure JWT-based authentication for members and staff.
* **Book Management**: Register new books in the library system.
* **Lending System**: Borrow and return books, with automatic tracking of available copies.
* **Member Dashboard**: View all books currently borrowed by a specific member.
* **API Versioning**: Supports multiple API versions to maintain compatibility with legacy clients.
* **Email Notifications**:
    * (Latest Version Only) Real-time email notifications for borrowing and returning a book.
    * Automatic notifications for members with overdue books.

---

## Tech Stack

* **Backend**: FastAPI
* **Database**: PostgreSQL
* **Containerization**: Docker & Docker Compose
* **Asynchronous Tasks**: Celery with a Redis broker
* **Code Quality**: `flake8` for linting and `pytest` for unit tests

---

## Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

You must have the following software installed:
* Docker
* Docker Compose

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create the environment file:**
    Copy the example environment file to create your own local version. This file will hold your secret credentials.
    ```bash
    cp .env.example .env
    ```

3.  **Configure environment variables:**
    Open the newly created `.env` file and fill in the required values (database credentials, JWT secret key, email server configuration, etc.). For development, you can use a service like [Mailtrap.io](https://mailtrap.io/) to test email functionality without sending real emails.

4.  **Build and run the containers:**
    This single command will build the Docker images, start all the services (API, database, worker, broker), and run them in the background.
    ```bash
    docker-compose up --build -d
    ```

The API service will now be running and accessible at `http://localhost:8000`.

---

## API Usage

### Interactive Documentation

Once the application is running, you can access the interactive API documentation (Swagger UI) provided by FastAPI at:
`http://localhost:8000/docs`

This interface allows you to explore and test all the API endpoints directly from your browser.

### API Versioning

The service supports multiple API versions for legacy clients. The desired API version must be specified in the request headers.

* **Header**: `X-API-Version`
* **Values**: `v1` (legacy), `latest` (includes all features)

If no header is provided, the system defaults to `v1`. The email notification feature on borrow/return events is only available on the `latest` version.

---

## Running Tests

To run the full suite of unit tests, execute the following command. This will run `pytest` inside the `api` container.

```bash
docker-compose exec api pytest