from django.test import TestCase
from django.core.exceptions import ValidationError
from users.models import CustomUser

class CustomUserModelTestCase(TestCase):

    def test_phone_number_field_validation(self):
        myuser = CustomUser(
            phone_number =  '123',
            password = "pass",
        )
        with self.assertRaises(ValidationError) as err:
            myuser.full_clean() #when i dont wanna validate data in forms and only if i wanna handle exceptions myself
        self.assertEqual(err.exception.message_dict['phone_number'], ["Phone number must be entered in the format: '09XXXXXXXXX', '00989XXXXXXXXX' or '+989XXXXXXXXX'."])
       