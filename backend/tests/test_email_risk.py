from app.services.email_risk_service import (
    email_risk_service
)

print(
    email_risk_service.analyze_email(
        "hr@microsoft.com"
    )
)

print(
    email_risk_service.analyze_email(
        "fake@mailinator.com"
    )
)

print(
    email_risk_service.analyze_email(
        "user@random-domain.com"
    )
)

print(
    email_risk_service.analyze_email(
        "invalid-email"
    )
)