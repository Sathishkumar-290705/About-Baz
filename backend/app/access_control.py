from app.config import settings


def check_access(
    metadata: dict,
    password: str | None = None
) -> bool:
    """
    Check whether a user can access a fact.

    Public facts:
        No password required.

    Private facts:
        Require the password assigned to their tier.

    No session state is stored.
    Every private request must provide its password again.
    """

    access = metadata.get("access")

    # Public fact → always allowed
    if access == "public":
        return True

    # Unknown access type → deny
    if access != "private":
        return False

    # Private fact must have a tier and password
    tier = metadata.get("tier")

    if not tier or not password:
        return False

    tier_passwords = {
        "tier_1": settings.tier_1_password,
        "tier_2": settings.tier_2_password,
        "tier_3": settings.tier_3_password,
        "tier_4": settings.tier_4_password,
    }

    expected_password = tier_passwords.get(tier)

    # Unknown tier → deny
    if expected_password is None:
        return False

    return password == expected_password