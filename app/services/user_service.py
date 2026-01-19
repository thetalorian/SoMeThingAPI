from sqlalchemy.orm import Session
from app.db.schema import User
from app.models.user import UserCreate

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def list_users(self) -> list[User]:
        return self.session.query(User).all()

    def create_user(self, user: UserCreate) -> User:
        new_user = User(name=user.name, email=user.email)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def get_user(self, user_id: int) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()

    def update_user(self, user_id: int, name: str) -> User | None:
        user = self.get_user(user_id)
        if user:
            user.name = name
            self.session.commit()
            self.session.refresh(user)
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
