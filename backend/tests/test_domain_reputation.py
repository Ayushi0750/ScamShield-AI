from app.services.domain_reputation_service import (
    domain_reputation_service
)

print(
    domain_reputation_service.get_reputation(
        "microsoft.com"
    )
)

print(
    domain_reputation_service.get_reputation(
        "mailinator.com"
    )
)

print(
    domain_reputation_service.get_reputation(
        "random-domain.com"
    )
)