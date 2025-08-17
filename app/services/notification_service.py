from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic import EmailStr

from app.config.env_config import notification_setting

class NotificationService:
    def __init__(self):
        self.fast_mail = FastMail(
            ConnectionConfig(
                **notification_setting.model_dump()
            )
        )

    async def send_email(self, recipients: list[EmailStr], subject: str, body: str):
        message = MessageSchema(
            recipients=recipients,
            subject=subject,
            body=body,
            subtype=MessageType.plain
        )
        await self.fast_mail.send_message(message)

