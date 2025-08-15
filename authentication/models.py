from django.db import models

HASH_LENGTH = 64  # SHA-256 hex representation
MAX_KEY_SIZE = 1024  # Maximum encrypted key size in bytes

class JuraUser(models.Model):
    """User model for zero-knowledge authentication system."""

    auth_hash = models.CharField(
        max_length=HASH_LENGTH, primary_key=True
    )  #  Hash of username and passcode
    recover_hash = models.CharField(
        max_length=HASH_LENGTH, unique=True, blank=True, null=True
    )  #  Hash of email + security questions
    encrypted_secret_key = models.BinaryField(blank=True, null=True)
    # The user's secret encryption key encrypted with the recovery key
    # derived from security questions and email. Only stored for recovery users.
    recovery_enabled = models.BooleanField(default=False)  #  Did the user set up recovery?

    def __str__(self):
        return self.auth_hash[:8]  #  First 8 chars for readability
