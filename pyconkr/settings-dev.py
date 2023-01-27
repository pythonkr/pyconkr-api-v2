import os

DEBUG = True

# RDS
DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        "NAME": os.getenv("AWS_RDS_DATABASE"),
        "USER": os.getenv("AWS_RDS_USER_ID"),
        "PASSWORD": os.getenv("AWS_RDS_PW"),
        "HOST": os.getenv("AWS_RDS_HOST"),
        "PORT": os.getenv("AWS_RDS_PORT"),
    }
}
