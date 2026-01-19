from sqlalchemy.orm import Session
from app.db.schema import Post
from app.models.post import PostCreate
from app.core.exceptions import NotFoundException, UnauthorizedException


class PostService:
    def __init__(self, session: Session):
        self.session = session


    def create_post(self, post: PostCreate, user_id: int) -> Post:
        """Create a new post associated with a user."""
        new_post = Post(user_id=user_id, **post.model_dump())
        self.session.add(new_post)
        self.session.commit()
        self.session.refresh(new_post)
        return new_post


    def list_posts(self) -> list[Post]:
        """List all posts."""
        return self.session.query(Post).all()


    def get_post(self, post_id: int) -> Post:
        """Retrieve a post by its ID."""
        post = self.session.query(Post).filter(Post.id == post_id).first()
        if not post:
            raise NotFoundException()
        return post


    def update_post(self, post_id: int, post: PostCreate, user_id: int) -> Post | None:
        """Update a post if owned by the user."""
        existing = self.get_post(post_id)
        if existing.user_id != user_id:
            raise UnauthorizedException()
        query = self.session.query(Post).filter(Post.id == post_id)
        update_data = {getattr(Post, k): v for k, v in post.model_dump().items()}
        query.update(update_data)
        self.session.commit()
        return query.first()


    def delete_post(self, post_id: int, user_id: int) -> None:
        """Delete a post if owned by the user."""
        post = self.get_post(post_id)
        if post.user_id != user_id:
            raise UnauthorizedException()
        self.session.delete(post)
        self.session.commit()
        return