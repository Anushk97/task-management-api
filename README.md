# Task Management API

A RESTful API for managing tasks built with FastAPI, SQLite, and Redis. This API provides a simple and efficient way to manage tasks with full CRUD operations and caching.

## Features

- ✨ Create, read, update, and delete tasks
- 🎯 SQLite for simple and reliable data persistence
- 🚀 Redis caching for faster task retrieval
- 🔄 Automatic timestamp management (created_at, updated_at)
- ✅ Task status management (PENDING, IN_PROGRESS, COMPLETE)
- 🛡️ Input validation and error handling
- 📝 OpenAPI documentation (Swagger UI and ReDoc)
- 🐳 Docker and Docker Compose support

## Technology Stack

- FastAPI (modern, fast web framework)
- SQLAlchemy (SQL toolkit and ORM)
- SQLite (database)
- Pydantic (data validation)
- Uvicorn (ASGI server)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | Get all tasks |
| GET | `/tasks/{id}` | Get a specific task |
| PUT | `/tasks/{id}` | Update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Setup and Installation

### Using Docker (Recommended)

1. Make sure Docker Desktop is running:
   - Open Docker Desktop application
   - Wait for the whale icon in the menu bar to stop animating

2. First time setup - Build and start services:
   ```bash
   docker compose up --build
   ```

3. For subsequent runs:
   ```bash
   # Start the services
   docker compose up

   # Start in detached mode (run in background)
   docker compose up -d

   # Stop the services
   docker compose down

   # View logs when running in detached mode
   docker compose logs -f
   ```

4. Access the services:
   - API and Swagger UI: http://localhost:8000/docs
   - ReDoc documentation: http://localhost:8000/redoc
   - Direct API access: http://localhost:8000

5. Container Management:
   ```bash
   # List running containers
   docker ps

   # Stop all containers
   docker compose down

   # Remove all containers and volumes (clean start)
   docker compose down -v

   # Rebuild and start (after code changes)
   docker compose up --build
   ```

6. Troubleshooting:
   - If the API is not responding, check container status: `docker ps`
   - View logs: `docker compose logs`
   - Restart services: `docker compose restart`
   - For a clean start: `docker compose down -v && docker compose up --build`

### Manual Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Redis (required for caching):
   ```bash
   docker run -d -p 6379:6379 redis
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API at http://localhost:8000

## Deployment

The API is deployed and accessible at:
- Base URL: https://task-management-api-925f.onrender.com
- API Documentation (Swagger UI): https://task-management-api-925f.onrender.com/docs
- Alternative Documentation (ReDoc): https://task-management-api-925f.onrender.com/redoc

Note: The free tier may take a few seconds to wake up on the first request.

## API Usage Examples

### Create a Task
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Complete Project", "description": "Finish the task management API", "status": "PENDING"}'
```

### List All Tasks
```bash
curl http://localhost:8000/tasks
```

### Get a Specific Task
```bash
curl http://localhost:8000/tasks/1
```

### Update a Task
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "IN_PROGRESS"}'
```

### Delete a Task
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Task Model

```json
{
    "id": 1,
    "title": "string",
    "description": "string",
    "status": "PENDING" | "IN_PROGRESS" | "COMPLETE",
    "created_at": "2025-02-07T04:30:32",
    "updated_at": "2025-02-07T04:30:32"
}
```

## API Documentation

Once the application is running, you can access:
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc

## Development

The application uses SQLite as the database, which is stored in `tasks.db` in the project root. The database schema is automatically created when the application starts.

## Error Handling

The API implements proper error handling with appropriate HTTP status codes:
- 404: Resource not found
- 400: Bad request (validation error)
- 201: Resource created successfully
- 204: Resource deleted successfully`
