# Monk AI CRUD Repository Layer

This directory contains the repository pattern implementation for database operations in the Monk AI application. The repository pattern abstracts the data access layer and provides a cleaner API for interacting with the database.

## Architecture

The CRUD layer follows a clean, modular architecture with:

- `BaseRepository`: A generic base class that provides common CRUD operations.
- Model-specific repositories: Extended classes for each model with specialized methods.

## Usage

Import repositories from the top level module:

```python
from app.crud import user, project, code_snippet
```

Each repository instance is pre-instantiated in `__init__.py` for convenience.

### Basic Operations

All repositories inherit standard CRUD methods:

```python
# Create
new_user = user.create(db, obj_in={"username": "johndoe", "email": "john@example.com", "password_hash": "hashed_password"})

# Read
user_obj = user.get(db, id=1)
users = user.get_multi(db, skip=0, limit=100)

# Update
updated_user = user.update(db, db_obj=user_obj, obj_in={"full_name": "John Doe"})

# Delete
deleted_user = user.delete(db, id=1)
```

### Specialized Methods

Each repository implements specialized methods for its entity. For example:

```python
# User repository specialized methods
user_by_email = user.get_by_email(db, email="john@example.com")
active_users = user.get_active_users(db)

# Project repository specialized methods
projects = project.get_by_owner(db, owner_id=1)
archived = project.archive_project(db, project_id=1)

# Pull request repository specialized methods
merged_pr = pull_request.merge_pull_request(db, pr_id=1)
```

## Security

All repositories handle SQL operations through SQLAlchemy's ORM to prevent SQL injection. The repositories do not perform authentication or authorization - that should be handled at the API layer.

## Transaction Management

The repositories accept a database session as an argument, allowing the caller to manage transactions:

```python
from sqlalchemy.orm import Session

def transfer_ownership(db: Session, project_id: int, new_owner_id: int):
    # Get the project
    project_obj = project.get(db, id=project_id)
    if not project_obj:
        raise ValueError("Project not found")
        
    # Update owner
    project.update(db, db_obj=project_obj, obj_in={"owner_id": new_owner_id})
    
    # Commit happens inside the update method
```

## Available Repositories

- `user`: User operations
- `project`: Project operations
- `code_snippet`: Code snippet operations
- `pull_request`: Pull request operations
- `review`: Review operations
- `doc_generation`: Documentation generation operations
- `test_case`: Test case operations
- `agent_task`: Agent task operations
- `agent_log`: Agent logging operations
- `notification`: Notification operations
- `team`: Team operations
- `team_membership`: Team membership operations
- `feedback`: Feedback operations 