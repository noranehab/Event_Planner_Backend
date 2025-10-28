project structure 
```
Event_Planner_Project/
│
├── alembic/ # Database migration directory
│
├── api/ # API layer (routes and helpers)
│ ├── auth.py # Authentication routes (login, signup, etc.)
│ ├── utils.py # Utility functions (JWT, password hashing, etc.)
│
├── db/ # Database layer
│ ├── database.py # Database connection and session management
│ ├── models.py # SQLAlchemy models (User, etc.)
│ ├── schemas.py # Pydantic schemas for request/response validation
│
├── tests/ # Unit and integration tests
│
├── test_main.http # HTTP request tests (manual API testing)
│
├── alembic.ini # Alembic configuration file
├── config.py # Application configuration (env variables, settings)
├── main.py # FastAPI entry point
└── .venv/ # Virtual environment (ignored by Git)/
│
├── alembic/ # Database migration directory
│
├── api/ # API layer (routes and helpers)
│ ├── auth.py # Authentication routes (login, signup, etc.)
│ ├── utils.py # Utility functions (JWT, password hashing, etc.)
│
├── db/ # Database layer
│ ├── database.py # Database connection and session management
│ ├── models.py # SQLAlchemy models (User, etc.)
│ ├── schemas.py # Pydantic schemas for request/response validation
│
├── tests/ # Unit and integration tests
│ ├── test_main.http # HTTP request tests (manual API testing)
│
├── alembic.ini # Alembic configuration file
├── config.py # Application configuration (env variables, settings)
├── main.py # FastAPI entry point
└── .venv/ # Virtual environment (ignored by Git)
