from sqlmodel import select

from app.config.database import sessionDep
from app.models.user import User
from app.schemas.auth_schema import CreateUser


class UserRepository:
    def __init__(self, session: sessionDep):
        self.session = session

    async def create_user(self, payload: CreateUser):
        try:
            user = User(
                first_name=payload.first_name,
                last_name=payload.last_name,
                email=payload.email,
                user_type=payload.user_type,
                password=payload.password,
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get_user(self, where: dict):
        try:
            user = await self.session.execute(
                select(User).filter_by(**where)
            )
            return user.scalars().first()
        except Exception as e:
            raise e
