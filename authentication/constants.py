"""
Cryptographic and field constants for Jura authentication system.
"""

# Hash constants
HASH_LENGTH = 64  # SHA-256 hex representation (256 bits / 8 * 2)

# Binary field limits for encrypted key
MAX_KEY_SIZE = 1024  # Maximum encrypted key size in bytes

# TOTP secret constants
TOTP_SECRET_LENGTH = 32  # Base32 TOTP secret (160 bits)

# Binary field limits for progress storage
MAX_PROGRESS_SIZE = 10000  # 10KB limit for progress data