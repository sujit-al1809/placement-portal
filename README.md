# Placement Portal

A full-stack placement portal for students, company HR teams, and admins. The backend uses Flask, SQLAlchemy, Flask-Security-Too, Celery, and Redis. The frontend uses Vue 3, Vue Router, and Axios.

## Project Overview

This portal covers the full placement workflow:

- Students register, complete a profile, browse jobs, apply, and track application status.
- Company HR users post jobs, review applicants, and shortlist candidates.
- Admins manage users and companies.
- The AI match-score endpoint compares student skills and job descriptions on the fly using TF-IDF and cosine similarity.
- A Celery background job can notify students whose skills match a new job posting.

## Folder Structure

- `backend/` Flask API, database models, auth, Celery tasks, and services.
- `frontend/` Vue 3 app with pages for student, HR, admin, and match scoring.

## Backend Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
cd backend
pip install -r requirements.txt
```

3. Run the Flask API:

```bash
python app.py
```

The API runs on `http://localhost:5000` by default.

### Useful Environment Variables

- `SECRET_KEY`
- `SECURITY_PASSWORD_SALT`
- `DATABASE_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `MAIL_SERVER`
- `MAIL_PORT`
- `MAIL_USERNAME`
- `MAIL_PASSWORD`
- `MAIL_DEFAULT_SENDER`
- `MAIL_SUPPRESS_SEND`

The default database is SQLite at `backend/instance/placement_portal.db`.

## Frontend Setup

1. Install dependencies:

```bash
cd frontend
npm install
```

2. Start the dev server:

```bash
npm run dev
```

The Vue app runs on `http://localhost:5173` and proxies `/api` requests to the Flask backend.

## Celery Worker Setup

Start Redis first, then run the worker from the `backend/` directory:

```bash
celery -A app.celery worker --loglevel=info
```

The worker handles `notify_matching_students(job_id)`, which scans student profiles, computes match scores, and sends email alerts for strong matches.

## API Documentation

All authenticated endpoints expect the token in the `Authentication-Token` header.

### 1. Register

`POST /api/auth/register`

Example:

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "Passw0rd!",
    "role": "Student",
    "name": "Asha",
    "skills": "python, flask, sql",
    "cgpa": 8.4,
    "branch": "CSE"
  }'
```

### 2. Login

`POST /api/auth/login`

Example response:

```json
{
  "token": "<auth-token>",
  "user": {
    "id": 1,
    "email": "student@example.com",
    "role": "Student"
  }
}
```

### 3. Profile

`GET /api/profile`

`PUT /api/profile`

Example:

```bash
curl -X PUT http://localhost:5000/api/profile \
  -H "Content-Type: application/json" \
  -H "Authentication-Token: <auth-token>" \
  -d '{
    "name": "Asha Kumar",
    "skills": "python, flask, sql, machine learning",
    "cgpa": 8.7,
    "branch": "CSE"
  }'
```

### 4. Jobs

`GET /api/jobs`

`POST /api/jobs`

`GET /api/jobs/<id>`

`PUT /api/jobs/<id>`

`DELETE /api/jobs/<id>`

Example job create request:

```bash
curl -X POST http://localhost:5000/api/jobs \
  -H "Content-Type: application/json" \
  -H "Authentication-Token: <hr-token>" \
  -d '{
    "title": "Backend Developer",
    "description": "Need a Python engineer with Flask and SQL skills",
    "required_skills": "python, flask, sql",
    "package": "12 LPA",
    "deadline": "2026-06-01T18:00:00"
  }'
```

### 5. Apply to a Job

`POST /api/jobs/<id>/apply`

Example:

```bash
curl -X POST http://localhost:5000/api/jobs/1/apply \
  -H "Authentication-Token: <student-token>"
```

### 6. Applications

`GET /api/applications`

`PUT /api/applications/<id>/status`

Example:

```bash
curl -X PUT http://localhost:5000/api/applications/4/status \
  -H "Content-Type: application/json" \
  -H "Authentication-Token: <hr-token>" \
  -d '{"status": "Shortlisted"}'
```

### 7. AI Match Score

`POST /api/match-score`

Input:

```json
{
  "student_skills": "python, machine learning, flask",
  "job_description": "We need a python developer with ML experience"
}
```

Example response:

```json
{
  "match_score": 87.4,
  "matched_skills": ["python", "machine learning"]
}
```

### 8. Admin APIs

`GET /api/admin/users`

`PUT /api/admin/users/<id>`

`GET /api/admin/companies`

`POST /api/admin/companies`

## Roles

- `Student` cannot post jobs.
- `CompanyHR` cannot apply to jobs.
- `Admin` can manage users and companies.

## Notes

- Celery and Redis are optional for local demo mode, but the job notifier is wired into the backend.
- The AI match score is computed on demand; no saved model file is needed.
