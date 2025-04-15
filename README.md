Sure! Here's a `README.md` file tailored for your project, based on the information you've provided:

---

```markdown
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

---

## 🐍 Tech Stack

- Python 3.10+
- Django
- Django REST Framework
- Redis (for caching)
- Poetry (for dependency management)
- Docker + Docker Compose (for containerized development)
- Pytest (for testing)

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/otp-auth-system.git
cd otp-auth-system
```

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

A **Postman Collection** is available at the root of the project (`otp-auth.postman_collection.json`) to help you test the available endpoints.

Steps:

1. Open Postman.
2. Import the collection file from the root directory.
3. Use the predefined requests to test OTP sending, verification, login, and signup completion.

---

## 📂 Project Structure

```
├── app/                            # Django project source code
├── tests/                          # Pytest test cases
├── docker-compose.yml             # Docker Compose setup
├── Dockerfile                     # Dockerfile for web app
├── pyproject.toml                 # Poetry configuration
├── otp-auth.postman_collection.json  # Postman API collection
└── README.md                      # This file
```

---

## 🚀 Endpoints Overview

| Method | Endpoint                   | Description                            |
|--------|----------------------------|----------------------------------------|
| POST   | `/login/request/`          | Request OTP for phone number           |
| POST   | `/login/password/`         | Login using phone number and password  |
| POST   | `/login/verify/`           | Verify OTP code                        |
| POST   | `/signup/complete/`        | Complete registration after OTP        |

---

## 🛡 Security Notes

- All OTPs are stored temporarily in Redis with a short expiration time.
- Login attempts are tracked and blocked if they exceed a safe threshold.
- Designed to prevent brute-force attacks and abuse of the login system.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🙌 Contribution

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

```

---

Let me know if you'd like me to tailor this even further — like adding example requests or setup instructions for a specific environment.