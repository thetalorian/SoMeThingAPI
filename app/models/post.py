from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.user import UserRead


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user: UserRead
    created_at: datetime
