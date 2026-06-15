from app.services.email_risk_service import (
    email_risk_service
)

print(
    email_risk_service.analyze_email(
        email="hr@microsoft.com",
        company="Microsoft"
    )
)

print(
    email_risk_service.analyze_email(
        email="hr@gmail.com",
        company="Microsoft"
    )
)

print(
    email_risk_service.analyze_email(
        email="jobs@infosys.com",
        company="Infosys"
    )
)

print(
    email_risk_service.analyze_email(
        email="recruiter@yahoo.com",
        company="Amazon"
    )
)