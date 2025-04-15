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
