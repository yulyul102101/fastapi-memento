import smtplib
from email.message import EmailMessage
from ssl import create_default_context

from app.core.config import settings


def send_email(
        *, receiver_email: str, subject: str, content: str
) -> None:
    # 이메일 메시지 생성
    msg = EmailMessage()
    msg['Subject'] = subject  # 제목 설정
    msg['From'] = settings.SMTP_USER
    msg['To'] = receiver_email

    # HTML 본문 설정
    content = content

    # HTML 본문을 이메일 메시지에 추가
    msg.add_alternative(content, subtype='html')

    # 이메일 전송
    context = create_default_context()
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)  # 메시지 전송


async def send_verification_email(email: str, code: str) -> None:
    subject = "[Memento] 인증코드 발급 안내"
    content = f"""
            <html>
                <body>
                    <p style="font-size: 16px;">귀하의 인증코드는 다음과 같습니다.</p>
                    <p style="font-size: 20px;"><b>{code}</b></p>
                </body>
            </html>
            """

    send_email(
        receiver_email=email,
        subject=subject,
        content=content
    )