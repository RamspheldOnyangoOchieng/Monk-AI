from typing import Optional
from pydantic import BaseModel
from app.models.review import ReviewType


# Shared properties
class ReviewBase(BaseModel):
    snippet_id: int
    type: ReviewType = ReviewType.COMMENT
    comment: Optional[str] = None
    suggested_code: Optional[str] = None


# Properties to receive on item creation
class ReviewCreate(ReviewBase):
    pass


# Properties to receive on item update
class ReviewUpdate(BaseModel):
    type: Optional[ReviewType] = None
    comment: Optional[str] = None
    suggested_code: Optional[str] = None


# Properties shared by models stored in DB
class ReviewInDBBase(ReviewBase):
    id: int
    user_id: int
    type: ReviewType = ReviewType.COMMENT

    class Config:
        from_attributes = True


# Properties to return to client
class ReviewResponse(ReviewInDBBase):
    pass 