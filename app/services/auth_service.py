from datetime import timedelta, datetime
from fastapi import HTTPException, status

from app.config.env_config import settings
from app.core.utils import hash_password, verify_password, create_access_token, generate_unique_number
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import CreateUser


class AuthService:
	def __init__(
			self,
			user_repo: UserRepository):
		self.user_repo = user_repo

	async def signup(self, payload: CreateUser):
		existing_user = await self.user_repo.get({"email": payload.email})
		if existing_user:
			raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
		payload.password = hash_password(payload.password)
		payload.user_type = payload.user_type
		return await self.user_repo.create(payload)

	async def get_current_user(self, token_data: dict) -> User:
		user = await self.user_repo.get(where={"id": token_data["userId"]})
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
		return user

	async def login(self, username: str, password: str) -> str:
		user = await self.user_repo.get(where={"email": username})
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

		is_match = verify_password(password, user.password)
		if not is_match:
			raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials")

		access_token = create_access_token(data={"userId": str(user.id), "user_type": user.user_type},
										   expires_delta=timedelta(minutes=settings.JWT_EXPIRATION_MINUTES))
		return access_token

	async def forgot_password(self, email: str) -> User:
		user = await self.user_repo.get(where={"email": email})
		if not user:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

		token = generate_unique_number(6)

		return await self.user_repo.update(user.id,
										   {"email_token": token,
											"otp_expiration": datetime.now() + timedelta(minutes=2)})
