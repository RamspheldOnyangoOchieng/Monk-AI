# Monk AI Models Documentation

This directory contains the SQLAlchemy models used in the Monk AI application. These models represent the database schema and provide an ORM layer for interacting with the database.

## Model Structure

All models inherit from the `Base` class and `TimestampMixin` which provides common timestamp functionality.

### Base Model

- `base.py`: Contains the SQLAlchemy `Base` class and `TimestampMixin` that provides `created_at` and `updated_at` timestamps for all models.

### Core Models

- `user.py`: User model for storing user data and authentication information.
- `project.py`: Project model for storing project-level data and metadata.
- `code_snippet.py`: Model for storing code snippets that need review or analysis.
- `pull_request.py`: Model representing GitHub Pull Request structure.
- `review.py`: Model for storing review comments and suggestions on code snippets.

### AI Features Models

- `doc_generation.py`: Model for storing documentation generation metadata and content.
- `test_case.py`: Model for storing test case generation results.
- `agent_task.py`: Model for managing tasks in the multi-agent system.
- `agent_log.py`: Model for tracking agent activities, errors, and audit logs.
- `feedback.py`: Model for collecting user feedback on AI-generated outputs.

### Organization and Notification Models

- `team.py`: Models for team organization (Team and TeamMembership).
- `notification.py`: Model for user notifications and activity feed.

## Relationships

The models are interrelated in the following way:

- `User` can have many `Project`s, `PullRequest`s, `Review`s, and can be part of multiple `Team`s through `TeamMembership`.
- `Project` can have many `CodeSnippet`s, `PullRequest`s, `DocGeneration`s, `TestCase`s, and `AgentTask`s.
- `Project` can belong to one or more `Team`s.
- `PullRequest` has an `author` (User), belongs to a `Project`, and can have many `CodeSnippet`s and `Review`s.
- `CodeSnippet` belongs to a `Project`, optionally to a `PullRequest`, and can have many `Review`s and `TestCase`s.
- `Review` has a `reviewer` (User), belongs to a `PullRequest` and optionally to a `CodeSnippet`.
- `AgentTask` can have parent-child relationships with other `AgentTask`s and can generate `AgentLog` entries.
- `Notification` connects users to various entities like `Project`s, `PullRequest`s, etc.
- `Feedback` can be linked to various models like `AgentTask`s, `DocGeneration`s, etc.

## How to Use

To use these models in your code:

```python
from app.models import User, Project, CodeSnippet

# Create a new user
user = User(username="johndoe", email="john@example.com", password_hash="hashed_password")

# Create a new project
project = Project(
    name="My Project",
    description="A project description",
    repository_url="https://github.com/user/repo",
    owner=user
)

# Create a code snippet
snippet = CodeSnippet(
    filename="app.py",
    content="print('Hello World')",
    start_line=1,
    end_line=1,
    language="python",
    project=project
)

# Add to session and commit
db.session.add(user)
db.session.add(project)
db.session.add(snippet)
db.session.commit()
```

## Team and Organization Example

```python
from app.models import Team, TeamMembership, TeamRole, User

# Create a team
team = Team(name="Engineering", description="Engineering department")

# Add users to the team
membership1 = TeamMembership(team=team, user=user1, role=TeamRole.OWNER)
membership2 = TeamMembership(team=team, user=user2, role=TeamRole.MEMBER)

# Assign projects to the team
team.projects.extend([project1, project2])

# Add to session and commit
db.session.add(team)
db.session.add(membership1)
db.session.add(membership2)
db.session.commit()
```

## Database Migrations

When making changes to these models, remember to create a new migration:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Model Enums

Several models use Enum types to represent status and types:

- `ProjectStatus`: ACTIVE, ARCHIVED, DELETED
- `PRStatus`: OPEN, CLOSED, MERGED
- `ReviewType`: COMMENT, SUGGESTION, APPROVAL, REQUEST_CHANGES
- `DocType`: API, README, USAGE, ARCHITECTURE, INSTALLATION
- `TestStatus`: PENDING, GENERATED, EXECUTED, PASSED, FAILED
- `TestType`: UNIT, INTEGRATION, E2E, PERFORMANCE, SECURITY
- `TaskStatus`: PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
- `TaskPriority`: LOW, MEDIUM, HIGH, CRITICAL
- `LogLevel`: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `NotificationType`: SYSTEM, PR_CREATED, PR_UPDATED, PR_MERGED, etc.
- `TeamRole`: OWNER, ADMIN, MEMBER, VIEWER
- `FeedbackType`: CODE_QUALITY, DOC_QUALITY, TEST_QUALITY, etc. 