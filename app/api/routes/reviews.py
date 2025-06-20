from typing import Annotated, Any, List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.crud.review import review_crud
from app.crud.code_snippet import snippet_crud
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from app.agents.pr_reviewer import process_review

router = APIRouter()


@router.get("/", response_model=List[ReviewResponse])
async def read_reviews(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    snippet_id: Optional[int] = None
) -> Any:
    """
    Retrieve reviews by snippet or all reviews for the current user.
    """
    if snippet_id:
        reviews = review_crud.get_multi_by_snippet(
            db=db, snippet_id=snippet_id, skip=skip, limit=limit
        )
    else:
        reviews = review_crud.get_multi_by_user(
            db=db, user_id=current_user.id, skip=skip, limit=limit
        )
    return reviews


@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    *,
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
    review_in: ReviewCreate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Create new code review. This will trigger an AI analysis.
    """
    # Check if the snippet exists and user has access
    snippet = snippet_crud.get(db=db, id=review_in.snippet_id)
    if not snippet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Snippet not found"
        )
        
    # Create initial review
    review = review_crud.create_with_user(
        db=db, obj_in=review_in, user_id=current_user.id
    )
    
    # Process the review in the background with AI
    background_tasks.add_task(
        process_review, review_id=review.id, snippet_content=snippet.content
    )
    
    return review


@router.get("/{review_id}", response_model=ReviewResponse)
async def read_review(
    *,
    db: Annotated[Session, Depends(get_db)],
    review_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Get code review by ID.
    """
    review = review_crud.get(db=db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if user owns the snippet or the review
    snippet = snippet_crud.get(db=db, id=review.snippet_id)
    if (
        review.user_id != current_user.id
        and snippet.owner_id != current_user.id
        and not current_user.is_superuser
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return review


@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(
    *,
    db: Annotated[Session, Depends(get_db)],
    review_id: int,
    review_in: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Update a code review. Only the owner of the review can update it.
    """
    review = review_crud.get(db=db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    if review.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    review = review_crud.update(db=db, db_obj=review, obj_in=review_in)
    return review


@router.delete("/{review_id}", response_model=ReviewResponse)
async def delete_review(
    *,
    db: Annotated[Session, Depends(get_db)],
    review_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> Any:
    """
    Delete a code review.
    """
    review = review_crud.get(db=db, id=review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    if review.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    review = review_crud.remove(db=db, id=review_id)
    return review