# Website Preview Application

A full-stack web application that allows users to generate visual previews of websites by submitting URLs, extract website metadata, and manage saved website links through a personalized dashboard.

The application provides secure user authentication, automated website metadata extraction, and persistent URL management using React, FastAPI, and MySQL.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Key Features](#key-features)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Application Workflow](#application-workflow)
6. [Project Structure](#project-structure)
7. [Prerequisites](#prerequisites)
8. [Installation and Setup](#installation-and-setup)
9. [Environment Configuration](#environment-configuration)
10. [Database Configuration](#database-configuration)
11. [API Documentation](#api-documentation)
12. [Authentication and Security](#authentication-and-security)
13. [Testing](#testing)
14. [Error Handling](#error-handling)
15. [Future Enhancements](#future-enhancements)
16. [Author](#author)

---

## Project Overview

The Website Preview Application is designed to simplify the process of viewing and managing website links.

Users can register and log in securely, submit website URLs, and generate visual previews containing information extracted from the target websites.

The backend retrieves website HTML content and extracts available metadata, including:

- Website title
- Website description
- Preview image
- Website favicon
- Website name

Users can save generated previews and access their saved website collection whenever required.

Each user's saved URLs are associated with their account, ensuring that users can manage their own website collections independently.

### Project Objectives

- Build a complete full-stack web application.
- Implement secure user registration and authentication.
- Generate website previews dynamically from submitted URLs.
- Extract metadata from external websites.
- Store website information in a relational database.
- Provide CRUD operations for saved website URLs.
- Implement authenticated and user-specific API access.

---

## Key Features

### 1. User Authentication

- User registration.
- User login.
- Password hashing.
- JWT-based authentication.
- Protected API endpoints.
- Retrieve authenticated user information.

### 2. Website Preview Generation

- Accept website URLs from users.
- Fetch website HTML using HTTPX.
- Parse HTML using BeautifulSoup.
- Extract Open Graph metadata.
- Extract website title and description.
- Extract preview images and favicon information.
- Handle missing metadata using fallback values.

### 3. Saved Website Management

- Save website URLs and extracted metadata.
- Retrieve all saved URLs.
- Retrieve an individual saved URL.
- Delete saved URLs.
- Associate saved URLs with authenticated users.

### 4. Database Management

- MySQL relational database.
- SQLAlchemy ORM integration.
- User and saved URL data management.
- Automatic table creation during application startup.

### 5. API Security

- JWT access tokens.
- Password hashing with bcrypt.
- Protected endpoints.
- User-specific data access.
- Input validation using Pydantic.
- CORS configuration.

---

## Technology Stack

| Category | Technology |
|---|---|
| Frontend | React.js |
| Frontend Build Tool | Vite |
| Programming Language | JavaScript |
| Backend | Python |
| Backend Framework | FastAPI |
| API Architecture | REST API |
| Database | MySQL |
| ORM | SQLAlchemy |
| Database Driver | PyMySQL |
| Authentication | JSON Web Token (JWT) |
| Password Hashing | Passlib / bcrypt |
| Data Validation | Pydantic |
| HTTP Client | HTTPX |
| HTML Parsing | BeautifulSoup |
| ASGI Server | Uvicorn |
| Environment Management | Python dotenv |
| API Testing | Postman / Swagger UI |
| Version Control | Git |

---

## System Architecture

The application follows a client-server architecture.

```text
                  USER
                   |
                   |
                   v
          REACT FRONTEND
             (Vite)
                   |
                   |
              REST API
                   |
                   v
           FASTAPI BACKEND
                   |
          +--------+--------+
          |                 |
          v                 v
    AUTHENTICATION     PREVIEW SERVICE
       SERVICE              |
          |                 |
          |                 v
          |          EXTERNAL WEBSITE
          |                 |
          |                 v
          |          WEBSITE HTML
          |                 |
          |                 v
          |          BEAUTIFULSOUP
          |                 |
          +--------+--------+
                   |
                   v
              SQLALCHEMY
                   |
                   v
                MYSQL
```

### Architecture Explanation

**Frontend Layer**

React provides the user interface for registration, login, URL submission, website previews, and saved website management.

**Backend Layer**

FastAPI handles HTTP requests, authentication, URL processing, metadata extraction, and database operations.

**Preview Service**

The preview service sends HTTP requests to external websites and extracts available metadata from their HTML content.

**Database Layer**

MySQL stores registered users and their saved website URLs with extracted metadata.

SQLAlchemy manages database communication between Python and MySQL.

---

## Application Workflow

### Step 1: User Registration

The user creates an account by providing registration information.

The backend validates the information, hashes the password, and stores the user record in MySQL.

### Step 2: User Login

The user submits login credentials.

The backend verifies the credentials and generates a JWT access token.

### Step 3: URL Submission

The authenticated user enters a website URL through the React interface.

The frontend sends the URL to the FastAPI preview endpoint with the JWT access token.

### Step 4: Metadata Extraction

The backend:

1. Validates the submitted URL.
2. Sends an HTTP request to the external website.
3. Retrieves the HTML content.
4. Parses the HTML using BeautifulSoup.
5. Extracts available website metadata.

### Step 5: Preview Generation

The backend returns the extracted metadata to the frontend.

React uses this information to display a website preview card.

### Step 6: Save Website

The website URL and its extracted metadata are stored in MySQL and associated with the authenticated user.

### Step 7: Manage Saved Websites

Users can retrieve their saved website collection, view individual records, and delete saved URLs.

---

## Project Structure

```text
website-preview-app/
|
|-- backend/
|   |
|   |-- app/
|   |   |
|   |   |-- models/
|   |   |   |-- user.py
|   |   |   |-- saved_url.py
|   |   |
|   |   |-- schemas/
|   |   |   |-- auth.py
|   |   |   |-- saved_url.py
|   |   |
|   |   |-- routers/
|   |   |   |-- auth.py
|   |   |   |-- urls.py
|   |   |
|   |   |-- services/
|   |   |   |-- auth_service.py
|   |   |   |-- preview_service.py
|   |   |
|   |   |-- database.py
|   |   |-- security.py
|   |   |-- main.py
|   |
|   |-- .env
|   |-- .env.example
|   |-- requirements.txt
|   |
|   |-- .venv/
|
|-- frontend/
|   |
|   |-- src/
|   |   |-- components/
|   |   |-- pages/
|   |   |-- services/
|   |   |-- assets/
|   |   |-- App.jsx
|   |   |-- main.jsx
|   |
|   |-- public/
|   |-- package.json
|   |-- index.html
|
|-- README.md
|-- .gitignore
```

---

## Prerequisites

Install the following software before running the application:

| Software | Requirement |
|---|---|
| Python | 3.10 or later |
| Node.js | 18 or later |
| npm | Included with Node.js |
| MySQL Server | 8.0 recommended |
| Git | Latest stable version |
| Code Editor | Visual Studio Code recommended |

Verify the installations:

```bash
python --version
node --version
npm --version
git --version
```

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

Navigate into the project:

```bash
cd website-preview-app
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file inside the backend directory.

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Update the configuration with your local database credentials.

See the [Environment Configuration](#environment-configuration) section.

### 4. Create MySQL Database

Open MySQL Workbench or your MySQL command-line client.

Execute:

```sql
CREATE DATABASE IF NOT EXISTS website_preview_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. Start FastAPI Backend

From the backend directory, execute:

```bash
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Frontend Setup

Open a separate terminal.

Navigate to the frontend directory:

```bash
cd frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the React development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## Environment Configuration

Create the following configuration in `backend/.env`:

```env
APP_NAME=Website Preview Application

DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=website_preview_db
DB_USER=root
DB_PASSWORD=your_mysql_password

JWT_SECRET_KEY=replace_with_a_random_secret_of_at_least_32_characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

FRONTEND_ORIGIN=http://localhost:5173
```

### Environment Variable Description

| Variable | Description |
|---|---|
| APP_NAME | Application name |
| DB_HOST | MySQL server hostname |
| DB_PORT | MySQL server port |
| DB_NAME | Database name |
| DB_USER | MySQL username |
| DB_PASSWORD | MySQL password |
| JWT_SECRET_KEY | Secret used for JWT signing |
| JWT_ALGORITHM | JWT signing algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | JWT expiration duration |
| FRONTEND_ORIGIN | React frontend origin for CORS |

**Important:** Never commit your actual `.env` file, database password, or JWT secret to a public Git repository.

---

## Database Configuration

The application uses MySQL as its relational database.

### Main Database Tables

#### 1. users

Stores registered user information.

Typical fields:

| Field | Description |
|---|---|
| id | Primary key |
| full_name | User's full name |
| email | User's email address |
| hashed_password | Hashed user password |
| is_active | User account status |
| created_at | Account creation timestamp |

#### 2. saved_urls

Stores website URLs and extracted preview metadata.

Typical fields:

| Field | Description |
|---|---|
| id | Primary key |
| user_id | Reference to the user |
| url | Submitted website URL |
| title | Website title |
| description | Website description |
| image_url | Preview image URL |
| favicon_url | Website favicon URL |
| site_name | Website name |
| created_at | Record creation timestamp |

The `user_id` field associates saved website records with their respective users.

The exact database columns depend on the SQLAlchemy model definitions.

---

## API Documentation

The backend exposes REST APIs for authentication, website preview generation, and saved URL management.

Base URL:

```text
http://127.0.0.1:8000
```

### Authentication APIs

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/auth/signup` | Register a new user | Public |
| POST | `/api/auth/login` | Authenticate a user | Public |
| GET | `/api/auth/me` | Get authenticated user details | Protected |

### Website Preview APIs

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/urls/preview` | Generate and save website preview | Protected |
| GET | `/api/urls` | Retrieve all saved URLs | Protected |
| GET | `/api/urls/{id}` | Retrieve a saved URL by ID | Protected |
| DELETE | `/api/urls/{id}` | Delete a saved URL | Protected |

### Health Check API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health/db` | Check database connectivity |

### Example: User Signup

```http
POST /api/auth/signup
Content-Type: application/json
```

Request:

```json
{
  "full_name": "Abhishek Kumar",
  "email": "abhishek@gmail.com",
  "password": "Abhishek@123"
}
```

### Example: User Login

```http
POST /api/auth/login
Content-Type: application/json
```

Request:

```json
{
  "email": "abhishek@gmail.com",
  "password": "Abhishek@123"
}
```

The login endpoint returns an access token when authentication succeeds.

### Example: Generate Website Preview

```http
POST /api/urls/preview
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

Request:

```json
{
  "url": "https://www.justdial.com/Hyderabad/Dr-Sarita-Rao-Tx-Hospitals-Near-Masjid-Uppal-Bus-Stand-Bharath-Nagar-Colony-Uppal/040PXX40-XX40-231215200040-Y2E1_BZDET"
}
```

The backend processes the URL, extracts available metadata, and saves the resulting record.

### Example: Get Saved URLs

```http
GET /api/urls
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Example: Get URL by ID

```http
GET /api/urls/1
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Example: Delete URL

```http
DELETE /api/urls/1
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Authentication and Security

The application uses JWT-based authentication to protect private resources.

### Authentication Flow

1. The user submits login credentials.
2. FastAPI verifies the user's credentials.
3. The backend generates a JWT access token.
4. The frontend uses the token for authenticated requests.
5. Protected endpoints validate the token.
6. The backend identifies the authenticated user.
7. User-specific database operations are performed.

### Security Measures

- Passwords are hashed before database storage.
- JWT tokens are used for authenticated API access.
- Protected endpoints require valid authentication.
- User-specific records are accessed through the authenticated user.
- Request payloads are validated using Pydantic.
- CORS is configured to allow the frontend origin.
- Website preview requests include URL validation and restrictions against local or private network targets.

For production deployment, additional protections such as secure token storage, HTTPS, rate limiting, DNS rebinding protection, and stricter outbound network controls should be implemented.

---

## Testing

### Backend Testing

Start the backend:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI:

```text
http://127.0.0.1:8000/docs
```

Test the following operations:

1. Register a new user.
2. Log in with registered credentials.
3. Retrieve the authenticated user's information.
4. Generate a website preview.
5. Retrieve all saved URLs.
6. Retrieve a saved URL by ID.
7. Delete a saved URL.
8. Verify database connectivity.

### Frontend Testing

Start the frontend:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

Verify the complete user workflow:

- User registration.
- User login.
- URL submission.
- Website preview generation.
- Saving website URLs.
- Displaying saved URLs.
- Deleting saved URLs.

### Recommended Negative Test Cases

| Test Case | Expected Behavior |
|---|---|
| Register with an existing email | Reject duplicate registration |
| Login with incorrect credentials | Return authentication error |
| Access protected API without token | Reject unauthorized request |
| Submit an invalid URL | Return validation error |
| Request a nonexistent URL ID | Return not found response |
| Access another user's saved URL | Deny access |
| Delete another user's saved URL | Deny access |

---

## Error Handling

The application uses HTTP status codes to communicate request outcomes.

| Status Code | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Bad request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |

External websites may block automated requests, restrict access, or provide incomplete metadata.

In such cases, the preview service should handle the failure gracefully and return an appropriate error or fallback preview according to its implementation.

---

## Future Enhancements

Potential improvements for future versions include:

- Website screenshot generation.
- Browser-based website previews.
- URL categorization and tagging.
- Search and filtering of saved websites.
- Pagination for saved URL collections.
- Duplicate URL detection.
- User profile management.
- Password reset functionality.
- Docker-based deployment.
- Cloud deployment using AWS.
- Automated backend and frontend tests.
- CI/CD pipeline integration.

---

## Running the Complete Application

The application requires two development servers.

| Component | Command | Local URL |
|---|---|---|
| FastAPI Backend | `uvicorn app.main:app --reload` | `http://127.0.0.1:8000` |
| React Frontend | `npm run dev` | `http://localhost:5173` |
| Swagger Documentation | Open in browser | `http://127.0.0.1:8000/docs` |

Ensure MySQL is running before starting the backend.

---

## Author

**Abhishek Kumar**

Full Stack Development Project

**Project:** Website Preview Application

**Technologies:** React.js, FastAPI, Python, MySQL

---

## License

This project was developed for learning and full-stack development demonstration purposes.

Add an appropriate open-source license before distributing the project publicly.
