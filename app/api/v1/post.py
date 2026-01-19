from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.post import PostCreate, PostRead
from app.services.post_service import PostService
from app.core.exceptions import NotFoundException, UnauthorizedException

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

def get_post_service() -> PostService:
    return PostService(session=SessionLocal()) # pragma: no cover


@router.post("/", response_model=PostRead)
def create_post(post: PostCreate, service: PostService = Depends(get_post_service)):
    return service.create_post(post, user_id=1)  # Assuming user_id=1 for simplicity


@router.get("/", response_model=list[PostRead])
def get_posts(service: PostService = Depends(get_post_service)):
    return service.list_posts()


@router.get("/{post_id}", response_model=PostRead)
def get_post(post_id: int, service: PostService = Depends(get_post_service)):
    try:
        post = service.get_post(post_id)
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}", response_model=PostRead)
def update_post(post_id: int, post: PostCreate, service: PostService = Depends(get_post_service)):
    try:
        updated_post = service.update_post(post_id, post, user_id=1)  # Assuming user_id=1 for simplicity
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    except UnauthorizedException:
        raise HTTPException(status_code=403, detail="Unauthorized to update this post")
    return updated_post


@router.delete("/{post_id}")
def delete_post(post_id: int, service: PostService = Depends(get_post_service)):
    try:
        service.delete_post(post_id, user_id=1)  # Assuming user_id=1 for simplicity
    except NotFoundException:
        raise HTTPException(status_code=404, detail="Post not found")
    except UnauthorizedException:
        raise HTTPException(status_code=403, detail="Unauthorized to update this post")
    return
