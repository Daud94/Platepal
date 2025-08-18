from pathlib import Path

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr
from app.config.env_config import notification_setting
from app.models.user import User

TEMPLATE_DIR = Path('app', 'templates')


class NotificationService:
	def __init__(self):
		self.fast_mail = FastMail(
			ConnectionConfig(
				**notification_setting.model_dump(),
				TEMPLATE_FOLDER=TEMPLATE_DIR,
			)
		)

	async def send_email(self, user: User, subject: str, template_name: str) -> None:
		message = MessageSchema(
			recipients=[user.email],
			subject=subject,
			subtype=MessageType.html,
			template_body={
				"user_name": user.first_name,
				"user_email": user.email,
			}
		)
		await self.fast_mail.send_message(message, template_name=template_name)
