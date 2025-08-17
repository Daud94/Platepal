from app.models.user import User
from app.services.notification_service import NotificationService


class EmailService:
    def __init__(self, notification_service: NotificationService):
        self.notification_service = notification_service

    async def send_welcome_email(self, user) -> None:
        subject = "Welcome to Platepal"
        body = (
            f"Hello {user.first_name},\n\n"
            "Thank you for joining Platepal, your go-to food ordering app! "
            "We're excited to have you on board and look forward to serving you delicious meals.\n\n"
            "Best regards,\nThe Platepal Team"
        )
        await self.notification_service.send_email([user.email], subject, body)
