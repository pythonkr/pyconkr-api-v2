import base64


def get_basic_auth_token(username: str, password: str) -> str:
    userpass = username + ':' + password
    encoded_u = base64.b64encode(userpass.encode()).decode()

    return encoded_u
