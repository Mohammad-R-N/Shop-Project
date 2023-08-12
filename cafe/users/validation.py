
import re
from django.core.exceptions import ValidationError

def phone_number_validator(value):
    """
    Validates phone numbers in the 09XX, 00989XX, or +98XX format and replaces the +98 and 0098 parts with 0.
    """
    phone_regex = r'^(\+98|0098|0)?9\d{9}$'
    if not re.match(phone_regex, value):
        raise ValidationError("Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'.")
    formatted_phone_number = re.sub(r'^\+98|^0098', '0', value)
    return formatted_phone_number