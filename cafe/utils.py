from kavenegar import *

def send_OTP(phone,code):

    try:
        api = KavenegarAPI('35484F79694A68527A58302F43354176354C366A62552B37665942646F334439627179326F564E766E63413D', timeout=20)
        params = {
            'sender': '',
            'receptor': phone,
            'message': f"your OTP code is {code}.",
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)