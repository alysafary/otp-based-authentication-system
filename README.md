# Secure OTP-Based Authentication System

This project implements a secure, rate-limited login and registration system using Django. Users can authenticate via one-time passwords (OTPs) or a traditional password-based login. The system includes protections against brute-force attacks by limiting suspicious attempts based on IP and phone number.

---

## 🔧 Features

- Phone number login using OTP
- Password-based login for registered users
- Rate limiting for failed login attempts by IP and phone number
- OTP generation, caching, and validation
- RESTful API endpoints
- Secure registration flow
- Clear feedback on blocked attempts
- Postman collection included for easy testing

## 📦 Installation

### 1. Clone the repository

### 2. Install dependencies using Poetry

```bash
poetry install
```

### 3. Set up environment variables

Create a `.env` file or use environment variable management as needed.

### 4. Run the application with Docker

Make sure Docker and Docker Compose are installed on your system.

```bash
docker-compose up --build
```

This will start the Django app and Redis server.

---

## 🧪 Running Tests

This project uses **Pytest** for testing. To run tests locally:

```bash
poetry run pytest
```

You can also run tests inside the Docker container:

```bash
docker-compose run web poetry run pytest
```

---

## 📬 API Testing

A **Postman Collection** is available at the root of the project (`Ubaar.postman_collection.json`) to help you test the available endpoints.

Steps:

1. Open Postman.
2. Import the collection file from the root directory.
3. Use the predefined requests to test OTP sending, verification, login, and signup completion.

---

## 📂 Project Structure

```
├── project/                            # Django project source code
├── users/                            # Django app
├── tests/                          # Pytest test cases
├── docker-compose.yml             # Docker Compose setup
├── Dockerfile                     # Dockerfile for web app
├── pyproject.toml                 # Poetry configuration
└── Ubaar.postman_collection.json  # Postman API collection
```

---

## 🚀 Endpoints Overview

| Method | Endpoint                   | Description                            |
|--------|----------------------------|----------------------------------------|
| POST   | `/login/request/`          | Request OTP for phone number           |
| POST   | `/login/password/`         | Login using phone number and password  |
| POST   | `/login/verify/`           | Verify OTP code                        |
| POST   | `/signup/complete/`        | Complete registration after OTP        |

