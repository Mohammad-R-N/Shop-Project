import re

def phone_number_validator(phone_number):
    pattern = r'^09\d{9}$'
    return bool(re.match(pattern, phone_number))
