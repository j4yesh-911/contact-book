class ContactExistsError(Exception):
    """Raised when duplicate contact is added"""


class InvalidPhoneError(Exception):
    """Raised when phone is not a valid 10-digit number"""
