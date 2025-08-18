from app.models.user import User
from app.services.notification_service import NotificationService


class EmailService:
	def __init__(self, notification_service: NotificationService):
		self.notification_service = notification_service

	async def send_welcome_email(self, user) -> None:
		subject = "Welcome to Platepal"

		await self.notification_service.send_email(user, subject, 'welcome_mail.html')
