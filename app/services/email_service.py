from app.models.user import User
from app.services.notification_service import NotificationService


class EmailService:
	def __init__(self, notification_service: NotificationService):
		self.notification_service = notification_service

	async def send_welcome_email(self, user) -> None:
		subject = "Welcome to Platepal"
		body = {
			"user_name": user.first_name,
			"user_email": user.email,
		}
		await self.notification_service.send_email(user, subject, body,'welcome_mail.html')

	async def send_forgot_password_email(self, user: User) -> None:
		subject = "Password Reset Request"
		body = {
			"name": user.first_name,
			"otp_code": user.email_token,
		}
		await self.notification_service.send_email(user, subject, body,'forgot_password_mail.html')
