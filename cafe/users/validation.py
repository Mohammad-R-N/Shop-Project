from django.core.validators import RegexValidator


phone_regex = RegexValidator(
    regex=r"^09\d{9}$",
    message="Phone number must be entered in the format: '09XXXXXXXXX'."
)
