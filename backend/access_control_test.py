from app.access_control import check_access
from app.config import settings


public_fact = {
    "access": "public"
}

private_fact = {
    "access": "private",
    "tier": "tier_1"
}


print("Public fact:")
print(check_access(public_fact))

print("\nPrivate without password:")
print(check_access(private_fact))

print("\nPrivate with wrong password:")
print(check_access(private_fact, "wrong-password"))

print("\nPrivate with correct password:")
print(
    check_access(
        private_fact,
        settings.tier_1_password
    )
)