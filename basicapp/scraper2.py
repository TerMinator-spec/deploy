
import json
import requests
import pyotp
from urllib import parse
import sys

class FyersApiClient:
    def __init__(self, fy_id, app_id_type, totp_key, pin, app_id, redirect_uri, app_type, app_id_hash):
        self.FY_ID = fy_id
        self.APP_ID_TYPE = app_id_type
        self.TOTP_KEY = totp_key
        self.PIN = pin
        self.APP_ID = app_id
        self.REDIRECT_URI = redirect_uri
        self.APP_TYPE = app_type
        self.APP_ID_HASH = app_id_hash

        self.BASE_URL = "https://api-t2.fyers.in/vagator/v2"
        self.BASE_URL_2 = "https://api.fyers.in/api/v2"
        self.URL_SEND_LOGIN_OTP = self.BASE_URL + "/send_login_otp"
        self.URL_VERIFY_TOTP = self.BASE_URL + "/verify_otp"
        self.URL_VERIFY_PIN = self.BASE_URL + "/verify_pin"
        self.URL_TOKEN = self.BASE_URL_2 + "/token"
        self.URL_VALIDATE_AUTH_CODE = self.BASE_URL_2 + "/validate-authcode"
        self.SUCCESS = 1
        self.ERROR = -1

    def send_login_otp(self):
        try:
            payload = {
                "fy_id": self.FY_ID,
                "app_id": self.APP_ID_TYPE
            }

            result_string = requests.post(url=self.URL_SEND_LOGIN_OTP, json=payload)
            if result_string.status_code != 200:
                return [self.ERROR, result_string.text]

            result = json.loads(result_string.text)
            request_key = result["request_key"]

            return [self.SUCCESS, request_key]

        except Exception as e:
            return [self.ERROR, e]

    def generate_totp(self):
        try:
            generated_totp = pyotp.TOTP(self.TOTP_KEY).now()
            return [self.SUCCESS, generated_totp]

        except Exception as e:
            return [self.ERROR, e]

    def verify_totp(self, request_key, totp):
        try:
            payload = {
                "request_key": request_key,
                "otp": totp
            }

            result_string = requests.post(url=self.URL_VERIFY_TOTP, json=payload)
            if result_string.status_code != 200:
                return [self.ERROR, result_string.text]

            result = json.loads(result_string.text)
            request_key = result["request_key"]

            return [self.SUCCESS, request_key]

        except Exception as e:
            return [self.ERROR, e]

    def verify_PIN(self, request_key, pin):
        try:
            payload = {
                "request_key": request_key,
                "identity_type": "pin",
                "identifier": pin
            }

            result_string = requests.post(url=self.URL_VERIFY_PIN, json=payload)
            if result_string.status_code != 200:
                return [self.ERROR, result_string.text]

            result = json.loads(result_string.text)
            access_token = result["data"]["access_token"]

            return [self.SUCCESS, access_token]

        except Exception as e:
            return [self.ERROR, e]

    def token(self, access_token):
        try:
            payload = {
                "fyers_id": self.FY_ID,
                "app_id": self.APP_ID,
                "redirect_uri": self.REDIRECT_URI,
                "appType": self.APP_TYPE,
                "code_challenge": "",
                "state": "sample_state",
                "scope": "",
                "nonce": "",
                "response_type": "code",
                "create_cookie": True
            }
            headers = {'Authorization': f'Bearer {access_token}'}

            result_string = requests.post(
                url=self.URL_TOKEN, json=payload, headers=headers
            )

            if result_string.status_code != 308:
                return [self.ERROR, result_string.text]

            result = json.loads(result_string.text)
            url = result["Url"]
            auth_code = parse.parse_qs(parse.urlparse(url).query)['auth_code'][0]

            return [self.SUCCESS, auth_code]

        except Exception as e:
            return [self.ERROR, e]

    def validate_authcode(self, auth_code):
        try:
            payload = {
                "grant_type": "authorization_code",
                "appIdHash": self.APP_ID_HASH,
                "code": auth_code,
            }

            result_string = requests.post(url=self.URL_VALIDATE_AUTH_CODE, json=payload)
            if result_string.status_code != 200:
                return [self.ERROR, result_string.text]

            result = json.loads(result_string.text)
            access_token = result["access_token"]

            return [self.SUCCESS, access_token]

        except Exception as e:
            return [self.ERROR, e]

    def get_access_token(self):
        # Step 1 - Retrieve request_key from send_login_otp API
        send_otp_result = self.send_login_otp()
        if send_otp_result[0] != self.SUCCESS:
            print(f"send_login_otp failure - {send_otp_result[1]}")
            sys.exit()
        else:
            print("send_login_otp success")

        # Step 2 - Generate totp
        generate_totp_result = self.generate_totp()
        if generate_totp_result[0] != self.SUCCESS:
            print(f"generate_totp failure - {generate_totp_result[1]}")
            sys.exit()
        else:
            print("generate_totp success")

        # Step 3 - Verify totp and get request key from verify_otp API
        request_key = send_otp_result[1]
        totp = generate_totp_result[1]
        verify_totp_result = self.verify_totp(request_key=request_key, totp=totp)
        if verify_totp_result[0] != self.SUCCESS:
            print(f"verify_totp_result failure - {verify_totp_result[1]}")
            sys.exit()
        else:
            print("verify_totp_result success")

        # Step 4 - Verify pin and send back access token
        request_key_2 = verify_totp_result[1]
        verify_pin_result = self.verify_PIN(request_key=request_key_2, pin=self.PIN)
        if verify_pin_result[0] != self.SUCCESS:
            print(f"verify_pin_result failure - {verify_pin_result[1]}")
            sys.exit()
        else:
            print("verify_pin_result success")

        # Step 5 - Get auth code for API V2 App from trade access token
        token_result = self.token(
            access_token=verify_pin_result[1]
        )
        if token_result[0] != self.SUCCESS:
            print(f"token_result failure - {token_result[1]}")
            sys.exit()
        else:
            print("token_result success")

        # Step 6 - Get API V2 access token from validating auth code
        auth_code = token_result[1]
        validate_authcode_result = self.validate_authcode(
            auth_code=auth_code
        )
        if token_result[0] != self.SUCCESS:
            print(f"validate_authcode failure - {validate_authcode_result[1]}")
            sys.exit()
        else:
            print("validate_authcode success")

        access_token = self.APP_ID + "-" + self.APP_TYPE + ":" + validate_authcode_result[1]

        return access_token

# Usage example:
if __name__ == "__main__":
    fy_id = "##########"
    app_id_type = "#"
    totp_key = "#################"
    pin = "####"
    app_id = "########"
    redirect_uri = "https://127.0.0.1/"
    app_type = "###"
    app_id_hash = "$$$$$$$$$$$$$$$$$$$$$$$$$$$$"

    fyers_api_client = FyersApiClient(fy_id, app_id_type, totp_key, pin, app_id, redirect_uri, app_type, app_id_hash)
    access_token = fyers_api_client.get_access_token()
    print(f"access_token - {access_token}")

    