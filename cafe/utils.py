from kavenegar import *

def send_OTP(phone_number,code):

    try:
        API_KEY = '35484F79694A68527A58302F43354176354C366A62552B37665942646F334439627179326F564E766E63413D'
        api = KavenegarAPI(f'https://api.kavenegar.com/v1/{API_KEY}/verify/lookup.json')
        params = {
            'sender': '',
            'receptor': phone_number,
            'token': code,
            'template': 'maktab'
        } 
        response = api.sms_send(params)
        print(response)
    except APIException as e: 
        print(e)
    except HTTPException as e: 
        print(e)