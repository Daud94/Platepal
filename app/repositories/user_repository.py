from app.database import sessionDep
from app.models.user import User
from app.schemas.user_schema import CreateUser
from typing import Any


class UserRepository:
    def __init__(self, session: sessionDep):
        self.session = session

    def create_user(self, user: CreateUser) -> User:
            try:
                user = User(**user.model_dump(exclude_unset=True))
                self.session.add(user)
                self.session.commit()
                return user
            except Exception as e:
                self.session.rollback()
                print(f"Error rolled back as {e}")
            finally:
                self.session.close()
                print("Session closed")

    def get_user(self, where: dict[str, Any]) -> User | None:
        user = self.session.query(User).filter_by(**where).first()
        return user
