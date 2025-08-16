from django.db import models
from django.core.validators import RegexValidator
from .constants import HASH_LENGTH, MAX_KEY_SIZE

hex_validator = RegexValidator(
    regex=r'^[a-fA-F0-9]+$',
    message='Hash must be valid hexadecimal characters'
) #  Used to validate that hashes are hex characters

class JuraUser(models.Model):
    """User model for zero-knowledge authentication system."""

    auth_hash = models.CharField(
        max_length=HASH_LENGTH, primary_key=True,  validators=[hex_validator]
    )  #  Hash of username and passcode
    recover_hash = models.CharField(
        max_length=HASH_LENGTH, unique=True, blank=True, null=True, validators=[hex_validator]
    )  #  Hash of email + security questions
    encrypted_secret_key = models.BinaryField(max_length=MAX_KEY_SIZE, blank=True, null=True)
    # The user's secret encryption key encrypted with the recovery key
    # derived from security questions and email. Only stored for recovery users.
    recovery_enabled = models.BooleanField(default=False)  #  Did the user set up recovery?

    def __str__(self):
        return self.auth_hash[:8]  #  First 8 chars for readability