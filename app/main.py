from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.config import create_db_and_tables
from app.api.task import router as tasks_router


app = FastAPI(
    title="Task Management API",
    description="API for managing tasks with FastAPI, SQLModel, and Pydantic",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",  # For React/Vue/Angular frontend
    "http://localhost:4200",
    "https://your-frontend-domain.com",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Allowed origins
    allow_credentials=True,          # Allows cookies / auth headers
    allow_methods=["*"],             # Allow all HTTP methods: GET, POST, etc.
    allow_headers=["*"],             # Allow all headers (or specify)
)

app.include_router(tasks_router)

@app.get("/")
async def root():
    """Health check endpoint for the API."""
    return {"message": "Welcome to the Task Management API"}

@app.on_event("startup")
def on_startup():
   create_db_and_tables()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
