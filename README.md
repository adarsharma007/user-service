# User Service

The **User Service** is a microservice responsible for managing user authentication, authorization, and user-related operations in the application. It interacts with MongoDB for data storage and uses JWT for secure authentication.

---

## Features
- User registration and login.
- JWT-based authentication.
- Secure password hashing with `bcrypt`.
- MongoDB integration for data storage.
- Protected routes for authenticated users.

---

## Requirements
- Python 3.10 or higher
- MongoDB 6.0
- Docker (for containerization)

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd backend/user-service
```

### 2. Install Dependencies
If you're not using Docker, create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 3. Environment Variables
Create a .env file in the user-service directory with the following:
```env
FLASK_ENV=development
MONGO_URI=mongodb://mongo:27017/userdb
JWT_SECRET_KEY=your_secret_key
```

### 4. Run the Service Locally
```bash
python app.py
```

### 5.Using Docker
To run the service with Docker:

1. Build the Docker image:
```bash
docker build -t user-service .
```
2. Run the Docker container:
```bash
docker run -d -p 8081:8081 --env-file .env user-service
```
---
## API Endpoints
### Authentication
- POST /api/auth/signup: Register a new user.
- POST /api/auth/login: Login an existing user.
### Protected Routes
- GET /api/auth/protected: Access protected content with a valid JWT token.
---
## Testing
Run unit tests with:

```bash
pytest
```

## Logging
Logs are saved in ```user-service.log```. Update ```docker-compose.yml``` to persist logs.
