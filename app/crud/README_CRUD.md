# Monk AI CRUD Repository Layer Documentation

## Overview

The CRUD (Create, Read, Update, Delete) repository layer in Monk AI provides a clean, type-safe interface for database operations. This layer abstracts the data access logic from the business logic, making the codebase more maintainable and testable.

## Architecture

### Base Repository

The foundation of our CRUD layer is the `BaseRepository` class, which provides generic CRUD operations:

```python
class BaseRepository(Generic[ModelType]):
    def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType
    def get(self, db: Session, id: int) -> Optional[ModelType]
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]
    def update(self, db: Session, *, db_obj: ModelType, obj_in: Union[Dict[str, Any], BaseModel]) -> ModelType
    def delete(self, db: Session, *, id: int) -> Optional[ModelType]
```

### Model-Specific Repositories

Each model has its own repository class that extends `BaseRepository` with specialized methods:

1. **UserRepository**
   - `get_by_email`: Find user by email
   - `get_by_username`: Find user by username
   - `get_active_users`: Get all active users
   - `get_by_github_username`: Find user by GitHub username
   - `deactivate`: Deactivate a user account

2. **ProjectRepository**
   - `get_by_owner`: Get projects by owner
   - `get_active_projects`: Get all active projects
   - `get_by_repository_url`: Find project by repository URL
   - `archive_project`: Archive a project
   - `restore_project`: Restore an archived project
   - `get_by_language`: Get projects by programming language

3. **CodeSnippetRepository**
   - `get_by_project`: Get code snippets by project
   - `get_by_pull_request`: Get code snippets by PR
   - `get_by_filename`: Get code snippets by filename
   - `get_by_language`: Get code snippets by language

4. **PullRequestRepository**
   - `get_by_project`: Get PRs by project
   - `get_by_author`: Get PRs by author
   - `get_by_status`: Get PRs by status
   - `get_by_github_pr_id`: Find PR by GitHub ID
   - `merge_pull_request`: Mark PR as merged
   - `close_pull_request`: Mark PR as closed

5. **ReviewRepository**
   - `get_by_pull_request`: Get reviews by PR
   - `get_by_reviewer`: Get reviews by reviewer
   - `get_by_code_snippet`: Get reviews by code snippet
   - `get_by_type`: Get reviews by type
   - `get_suggestions`: Get review suggestions

6. **DocGenerationRepository**
   - `get_by_project`: Get docs by project
   - `get_by_doc_type`: Get docs by type
   - `get_published`: Get published docs
   - `publish`: Mark doc as published
   - `unpublish`: Mark doc as unpublished

7. **TestCaseRepository**
   - `get_by_project`: Get tests by project
   - `get_by_code_snippet`: Get tests by code snippet
   - `get_by_status`: Get tests by status
   - `get_by_test_type`: Get tests by type
   - `update_test_status`: Update test status
   - `get_failed_tests`: Get failed tests
   - `get_passed_tests`: Get passed tests

8. **AgentTaskRepository**
   - `get_by_project`: Get tasks by project
   - `get_by_agent_type`: Get tasks by agent type
   - `get_by_status`: Get tasks by status
   - `get_by_priority`: Get tasks by priority
   - `get_subtasks`: Get subtasks
   - `start_task`: Start a task
   - `complete_task`: Complete a task
   - `fail_task`: Mark task as failed
   - `cancel_task`: Cancel a task
   - `get_pending_tasks`: Get pending tasks

9. **AgentLogRepository**
   - `get_by_agent_task`: Get logs by task
   - `get_by_project`: Get logs by project
   - `get_by_agent_type`: Get logs by agent type
   - `get_by_level`: Get logs by level
   - `get_by_user`: Get logs by user
   - `get_errors`: Get error logs
   - `log_message`: Create a log entry

10. **NotificationRepository**
    - `get_by_recipient`: Get notifications by recipient
    - `get_by_sender`: Get notifications by sender
    - `get_by_project`: Get notifications by project
    - `get_by_pull_request`: Get notifications by PR
    - `get_unread`: Get unread notifications
    - `mark_as_read`: Mark notification as read
    - `mark_all_as_read`: Mark all notifications as read
    - `get_by_type`: Get notifications by type

11. **TeamRepository**
    - `get_by_name`: Find team by name
    - `get_teams_for_user`: Get user's teams
    - `add_project_to_team`: Add project to team
    - `remove_project_from_team`: Remove project from team

12. **TeamMembershipRepository**
    - `get_by_team_and_user`: Get membership by team and user
    - `get_team_members`: Get team members
    - `get_by_role`: Get members by role
    - `update_role`: Update member role
    - `deactivate`: Deactivate membership
    - `activate`: Activate membership

13. **FeedbackRepository**
    - `get_by_user`: Get feedback by user
    - `get_by_project`: Get feedback by project
    - `get_by_agent_task`: Get feedback by task
    - `get_by_pull_request`: Get feedback by PR
    - `get_by_code_snippet`: Get feedback by code snippet
    - `get_by_doc_generation`: Get feedback by doc
    - `get_by_test_case`: Get feedback by test
    - `get_by_feedback_type`: Get feedback by type
    - `get_by_rating_range`: Get feedback by rating range
    - `get_average_rating`: Get average rating

## Usage Examples

### Basic CRUD Operations

```python
from app.crud import user, project

# Create
new_user = user.create(db, obj_in={
    "username": "johndoe",
    "email": "john@example.com",
    "password_hash": "hashed_password"
})

# Read
user_obj = user.get(db, id=1)
users = user.get_multi(db, skip=0, limit=100)

# Update
updated_user = user.update(db, db_obj=user_obj, obj_in={"full_name": "John Doe"})

# Delete
deleted_user = user.delete(db, id=1)
```

### Specialized Operations

```python
# Get active projects
active_projects = project.get_active_projects(db)

# Get pull requests by status
open_prs = pull_request.get_by_status(db, project_id=1, status=PRStatus.OPEN)

# Get team members by role
admins = team_membership.get_by_role(db, team_id=1, role=TeamRole.ADMIN)

# Get average feedback rating
avg_rating = feedback.get_average_rating(db, project_id=1, feedback_type=FeedbackType.CODE_QUALITY)
```

## Best Practices

1. **Type Safety**
   - All methods are properly typed using Python type hints
   - Use Optional[] for nullable returns
   - Use Union[] for multiple possible types

2. **Error Handling**
   - Return None for not found cases
   - Raise exceptions for invalid operations
   - Use proper error messages

3. **Query Optimization**
   - Use appropriate indexes
   - Limit result sets
   - Use efficient joins

4. **Transaction Management**
   - Pass database session explicitly
   - Commit transactions at appropriate level
   - Handle rollbacks properly

## Security Considerations

1. **SQL Injection Prevention**
   - Use SQLAlchemy ORM
   - Parameterize all queries
   - Validate input data

2. **Access Control**
   - Implement at service layer
   - Validate permissions
   - Log security events

## Testing

Each repository should have corresponding tests:

```python
def test_user_repository():
    # Test create
    user = user_repo.create(db, obj_in=user_data)
    assert user.username == user_data["username"]
    
    # Test get
    found_user = user_repo.get(db, id=user.id)
    assert found_user == user
    
    # Test specialized methods
    user_by_email = user_repo.get_by_email(db, email=user.email)
    assert user_by_email == user
```

## Maintenance

1. **Adding New Methods**
   - Follow existing patterns
   - Add proper type hints
   - Document with docstrings
   - Add tests

2. **Modifying Existing Methods**
   - Maintain backward compatibility
   - Update tests
   - Update documentation

3. **Performance Optimization**
   - Monitor query performance
   - Add indexes as needed
   - Optimize joins
   - Use appropriate caching 